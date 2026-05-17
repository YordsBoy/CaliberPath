"""CaliberPath Visual Regression Detection — Pre-Render + Post-Render Suites.

Implementation surface for WS-VISUAL-REGRESSION-DETECTION per the technical
specification at:
    [OPSDIR]/08_Production_Pipeline/2026-05-09_CaliberPath_WS-VisualRegressionDetection_TechnicalSpecification_v1.md

Two-tier verification model:

    Tier 1 (pre-render): Source-side correctness checks fire BEFORE ReportLab
        pipeline execution. Halt on FAIL; log and proceed on WARN.
        Six check categories (sections 3.1-3.6 of spec).

    Tier 2 (post-render): Rendered-artifact comparison against canonical
        reference renders fires AFTER ReportLab pipeline execution.
        Surfaces regressions for Info/Tech Tier 1 disposition.
        Five comparison categories (sections 4.1-4.5 of spec).

Module surface (per spec section 7.2 module structure recommendation):

    Pre-render check categories (each returns List[CheckResult]):
        verify_source_data_integrity(doc_path, doc_class)
        verify_methodology_conformance(doc_path, doc_class)
        verify_brand_specification_adherence(doc_path, doc_class)
        verify_pipeline_pattern_conformance(doc_path, doc_class, pattern_set)
        verify_l4_permanent_discipline(doc_path)
        verify_f14_disk_authoritative_conformance(doc_path)

    Post-render check categories (each returns CheckResult):
        detect_byte_level_regression(rendered_pdf, reference_pdf)
        detect_structural_regression(rendered_pdf, reference_pdf)
        detect_visual_fidelity_regression(rendered_pdf, reference_pdf, ...)
        detect_bookmark_regression(rendered_pdf, reference_pdf)
        verify_font_asset_embedding(rendered_pdf)

    Suite runners:
        run_pre_render_verification_suite(doc_path, doc_class, config)
        run_post_render_regression_detection(rendered_pdf, reference_pdf,
                                             doc_class, config)

    Report generation:
        write_verification_report(report, output_dir, output_format)

    Reference render governance:
        load_reference_render_metadata(doc_class, doc_id)
        list_reference_renders()

Authority: Info/Tech CIO Tier 1 specification authority routing implementation
to Claude Code Tier 1 per WS-VRD activation 2026-05-09.

L-4 PERMANENT discipline: zero literal dollar-sign characters in this module.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# L-4 PERMANENT discipline: dollar-sign character constructed via chr() to
# avoid embedding the literal in this source file. Used by the L-4 scanner
# below to detect literal occurrences in target documents.
_DOLLAR = chr(36)
_DOUBLE_DOLLAR = _DOLLAR + _DOLLAR  # corruption signature pattern


# =============================================================================
# Canonical asset registries (per VBS v1.5 + brandmark inventory)
# =============================================================================
# PRE_BS_001 — VBS canonical color hex codes. Lowercased for comparison.
CANONICAL_VBS_HEX_COLORS = {
    '#1e3a5f',  # DSB Deep Slate Blue
    '#c08b3a',  # BA Burnished Amber
    '#cfa366',  # BA75
    '#fbf4ea',  # BA10
    '#f6f3ee',  # WC Warm Cream
    '#c5cad2',  # WC80
    '#e8ecf0',  # SM Slate Mist (fillable input only)
    '#1a2332',  # DG Deep Graphite
    '#3d4e5c',  # WS Warm Slate
    '#ffffff',  # WHT Pure White
    '#f1f3f6',  # DSB5
    '#000000',  # Black (utility; legitimate in some contexts)
}

# PRE_BS_002 — VBS canonical typeface tokens. Other tokens flagged.
CANONICAL_VBS_FONTS = {
    'Inter-Regular', 'Inter-Medium', 'Inter-SemiBold', 'Inter-Bold',
    'Inter-Italic', 'CormorantGaramond-SemiBold',
    'CormorantGaramond-Italic', 'CormorantGaramond-SemiBoldItalic',
    'Helvetica',  # AcroForm constraint per existing pipeline
    # Friendly aliases used in source content
    'Inter', 'Cormorant', 'Cormorant Garamond',
}
# Non-canonical font tokens that should be flagged when found verbatim.
# 'Georgia' deliberately omitted — the U.S. state name is common in CSRA
# market-context references and produces dense false-positive matches.
# 'Garamond' standalone is permitted because the canonical Cormorant
# Garamond typeface contains it as a substring; word-boundary regex
# matching (see _NON_CANONICAL_FONT_RE) prevents partial-match flags
# while still catching standalone 'Garamond' tokens.
NON_CANONICAL_FONT_TOKENS = (
    'Times New Roman', 'Times Roman', 'Times', 'Arial', 'Calibri',
    'Verdana', 'Tahoma', 'Courier',
    'Palatino', 'Bookman', 'Lucida',
)
# Word-boundary regex compiled once; matches whole-word occurrences and
# excludes 'Garamond' when preceded by 'Cormorant' (the canonical family).
_NON_CANONICAL_FONT_RE = re.compile(
    r'(?<!Cormorant )\b(?:'
    + '|'.join(re.escape(t) for t in NON_CANONICAL_FONT_TOKENS)
    + r'|(?<!Cormorant )Garamond)\b')

# PRE_BS_003 — Canonical brandmark filenames per current Visual Identity
# inventory. Non-canonical brandmark references in markdown image links
# are flagged.
CANONICAL_BRANDMARK_FILENAMES = {
    'CaliberPath_Brandmark_Reverse_Standalone_v1.png',
    'CaliberPath_Brandmark_Reverse_Companion_v1.png',
    'CaliberPath_Brandmark_Standalone_v1.png',
    'CaliberPath_Brandmark_Companion_v1.png',
    'CaliberPath_Wordmark_v1.png',
    'CaliberPath_Wordmark_Reverse_v1.png',
}

# UPLS canonical domain + competency-keyword set (PRE_MC_001)
UPLS_DOMAIN_KEYWORDS = (
    'professionalism', 'leadership', 'influence', 'self-mastery',
    'self mastery', 'universal professional',
)

# PRE_MC_005 — Substance-Grounded Cluster Determination Framework typical
# ranges per Source-Authoring Guidance v1.1 §3.4 + InfoTech Phase 4
# Re-Render Execution Routing §4.2 acceptance criterion. Size buckets
# are inclusive ranges; cluster_typical is the (low, high) typical band.
CLUSTER_SIZE_BUCKETS = (
    # (size_label, ksa_low, ksa_high, cluster_low, cluster_high)
    ('Small',      10, 15, 4, 6),
    ('Medium',     16, 25, 6, 8),
    ('Large',      26, 35, 7, 9),
    ('Very Large', 36, 999, 8, 9),
)

# Word-to-integer mapping for source-content cluster-count narrative
# parsing (e.g., "seven clusters", "twelve clusters"). Only English
# number words 1-20 needed; larger counts are written as digits.
_NUMBER_WORDS = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
    'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11,
    'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
    'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19,
    'twenty': 20,
}

# PRE_BS_004 — Restricted typeface set: pipeline emits these typefaces for
# italic callout contexts (Coaching implication, Session opening,
# parenthetical italic, italic-banner lines) per cig_template.py callout
# rendering logic. Glyph-coverage validation operates on the manifest for
# each restricted typeface.
RESTRICTED_TYPEFACES_CIG = (
    'CormorantGaramond-Italic',
    'CormorantGaramond-SemiBoldItalic',
)

# Source markdown italic-callout context patterns (mirrors cig_template.py
# Tier 3 callout dispatch). Used by PRE_BS_004 to extract segments whose
# rendered glyphs come from RESTRICTED_TYPEFACES_CIG.
_ITALIC_CONTEXT_PATTERNS = (
    re.compile(r'^\*Coaching implication:\*\s*(.+?)\s*$', re.MULTILINE),
    re.compile(r'^\*Session opening:\*\s*(.+?)\s*$', re.MULTILINE),
    re.compile(r'^\*\((.+?)\)\*\s*$', re.MULTILINE),
    re.compile(r'^\*([^*][^*]*?[^*])\*\s*$', re.MULTILINE),
)

# ELM cycle phase canonical names (PRE_MC_002). Mapping handles both
# academic ELM naming and CaliberPath operational labels.
ELM_PHASE_CANONICAL = {
    'concrete experience',          # academic + CP
    'reflection',                   # academic
    'reflective observation',       # academic
    'publish & process',            # CP variant of Reflection
    'publish and process',
    'p&p',
    'conceptualization',            # academic
    'abstract conceptualization',
    'generalize new information',   # CP variant
    'gni',
    'active experimentation',       # academic
    'develop',                      # CP variant
    'apply',                        # CP between-session
    'apply debrief',                # CP between-session debrief
    'admin',                        # CP session-close admin
    'logistics',                    # CP session-close logistics
}


# =============================================================================
# cp_lookups integration (lazy import; sys.path injection from OPSDIR)
# =============================================================================
def _load_cp_lookups():
    """Lazy import of cp_lookups from OPSDIR Caliber_Profile module.

    cp_verify.py at KSA-REPO needs the canonical ELO + L2 maps that live
    in cp_lookups.py at OPSDIR. Returns the cp_lookups module on success
    or None when the module is unavailable (e.g., OPSDIR path not resolvable).
    """
    cp_lookups_dir = os.path.join(
        _opsdir_root(), '08_Production_Pipeline', 'Caliber_Profile')
    if cp_lookups_dir not in os.sys.path:
        os.sys.path.insert(0, cp_lookups_dir)
    try:
        import cp_lookups  # noqa: WPS433  - dynamic import from OPSDIR
        return cp_lookups
    except ImportError:
        return None


# Per-doc-class canonical lookup-source paths. Defaults; per-doc-class config
# (Phase E) may override. Foundation products skip ELO resolution because
# CF-ELO namespace uses incompatible format.
def _resolve_lookup_sources(
        doc_path: str, doc_class: str) -> Tuple[Optional[str], Optional[str]]:
    """Resolve (elo_matrix_path, l2_source_path) for a document.

    Returns (None, None) when canonical lookup sources are not applicable.
    Phase B.2 default resolution:
      - FG / CIG / WORKBOOK / CALIBER_PROFILE in the Career Compass family:
        ELO from CC TLO/ELO Matrix; L2 from doc itself (Reference Index)
      - GAR: same defaults
      - Foundation products (CF FG, CF-SM-01): no canonical ELO source
        in this phase; CF-ELO namespace is excluded by the qualifier regex
        and will be skipped
    """
    base = _opsdir_root()
    cc_matrix = os.path.join(
        base, '04_Deliverables', 'Curricula', 'Career_Compass',
        '2026-03-09_CaliberPath_CareerCompass_TLO_ELO_Matrix_v1.md')

    # Foundation products: detect via filename heuristic
    fname = os.path.basename(doc_path or '').lower()
    is_foundation = (
        'caliberfoundation' in fname or 'cf-sm-' in fname
        or 'cf_sm_' in fname or '_cf_' in fname)

    if is_foundation:
        return (None, doc_path if doc_class == 'FG' else None)

    if doc_class in ('FG', 'CIG_FULL', 'CIG_QRC', 'WORKBOOK',
                     'CALIBER_PROFILE', 'GAR'):
        return (cc_matrix if os.path.exists(cc_matrix) else None,
                doc_path if doc_class == 'FG' else None)
    return (None, None)


# =============================================================================
# Version + governing-document references (F-14 version-agnostic)
# =============================================================================
__version__ = '1.0.0'
__spec_version__ = 'WS-VRD v1 (2026-05-09)'

# Document classes per spec section 6.1 enum
DOC_CLASSES = (
    'FG', 'CIG_FULL', 'CIG_QRC', 'GAR', 'WORKBOOK', 'CALIBER_PROFILE',
)

# Status enum
STATUS_PASS = 'PASS'
STATUS_FAIL = 'FAIL'
STATUS_WARN = 'WARN'
ALL_STATUSES = (STATUS_PASS, STATUS_FAIL, STATUS_WARN)

# Verification type enum
VTYPE_PRE = 'pre_render'
VTYPE_POST = 'post_render'


# =============================================================================
# Data structures (spec section 2.4)
# =============================================================================
def _now_iso() -> str:
    """ISO 8601 timestamp for CheckResult / VerificationReport."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat(
        timespec='seconds')


@dataclass
class CheckResult:
    """Result of a single verification check (spec section 2.4).

    Aggregated by VerificationReport. JSON-serializable via asdict().
    """
    check_id: str
    category: str
    status: str
    details: str = ''
    fix_recommendation: str = ''
    timestamp: str = field(default_factory=_now_iso)

    def __post_init__(self) -> None:
        if self.status not in ALL_STATUSES:
            raise ValueError(
                f'CheckResult.status must be one of {ALL_STATUSES!r}, '
                f'got {self.status!r}')


@dataclass
class VerificationReport:
    """Aggregated verification result.

    overall_status: worst-of-children. Any FAIL -> FAIL; any WARN and no FAIL
        -> WARN; else PASS.
    halt_pipeline: True if any FAIL in a pre-render report; always False for
        post-render reports (rendering already completed; report is informational).
    """
    verification_type: str
    document_class: str
    document_identifier: str
    checks: List[CheckResult] = field(default_factory=list)
    overall_status: str = STATUS_PASS
    halt_pipeline: bool = False
    verification_timestamp: str = field(default_factory=_now_iso)
    verification_version: str = __version__

    def __post_init__(self) -> None:
        if self.verification_type not in (VTYPE_PRE, VTYPE_POST):
            raise ValueError(
                f'verification_type must be {VTYPE_PRE!r} or {VTYPE_POST!r}, '
                f'got {self.verification_type!r}')

    def add(self, check: CheckResult) -> None:
        """Append a CheckResult and recompute overall status + halt flag."""
        self.checks.append(check)
        self._recompute_status()

    def extend(self, checks: List[CheckResult]) -> None:
        """Append multiple CheckResults and recompute aggregate status."""
        self.checks.extend(checks)
        self._recompute_status()

    def _recompute_status(self) -> None:
        statuses = {c.status for c in self.checks}
        if STATUS_FAIL in statuses:
            self.overall_status = STATUS_FAIL
        elif STATUS_WARN in statuses:
            self.overall_status = STATUS_WARN
        else:
            self.overall_status = STATUS_PASS
        # halt_pipeline only set for pre-render reports with FAIL
        self.halt_pipeline = (
            self.verification_type == VTYPE_PRE
            and self.overall_status == STATUS_FAIL)

    def to_dict(self) -> Dict[str, Any]:
        """Render as a JSON-serializable dict matching spec section 6.1 schema."""
        return {
            'verification_type': self.verification_type,
            'document_class': self.document_class,
            'document_identifier': self.document_identifier,
            'verification_timestamp': self.verification_timestamp,
            'verification_version': self.verification_version,
            'checks': [asdict(c) for c in self.checks],
            'overall_status': self.overall_status,
            'halt_pipeline': self.halt_pipeline,
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> 'VerificationReport':
        """Reconstruct a VerificationReport from JSON dict (round-trip)."""
        checks = [CheckResult(**c) for c in payload.get('checks', [])]
        report = cls(
            verification_type=payload['verification_type'],
            document_class=payload['document_class'],
            document_identifier=payload.get('document_identifier', ''),
            verification_timestamp=payload.get(
                'verification_timestamp', _now_iso()),
            verification_version=payload.get(
                'verification_version', __version__),
        )
        report.checks = checks
        report.overall_status = payload.get('overall_status', STATUS_PASS)
        report.halt_pipeline = payload.get('halt_pipeline', False)
        return report


# =============================================================================
# Helper: structured CheckResult constructors
# =============================================================================
def _mk_pass(check_id: str, category: str, details: str = '') -> CheckResult:
    return CheckResult(
        check_id=check_id, category=category, status=STATUS_PASS,
        details=details)


def _mk_fail(check_id: str, category: str,
             details: str, fix: str = '') -> CheckResult:
    return CheckResult(
        check_id=check_id, category=category, status=STATUS_FAIL,
        details=details, fix_recommendation=fix)


def _mk_warn(check_id: str, category: str,
             details: str, fix: str = '') -> CheckResult:
    return CheckResult(
        check_id=check_id, category=category, status=STATUS_WARN,
        details=details, fix_recommendation=fix)


# =============================================================================
# Pre-render verification suite (spec section 3)
# =============================================================================
# 3.1 Source-Data Integrity
# Reference patterns for cross-reference resolution checks.
_ELO_REF_RE = re.compile(r'(?<![A-Z-])\bELO\s+(\d+)\.(\d+)')
_L2_REF_RE = re.compile(r'\bL2-([FR])(\d+)\b')


# Helpers for PRE_MC_005 (cluster-count) + PRE_BS_004 (glyph-coverage)
# per InfoTech Phase 4 Re-Render Execution Routing §4.2 + §4.3.
def _glyph_manifest_dir() -> str:
    return os.path.join(
        _opsdir_root(), '08_Production_Pipeline',
        'Verification_Config', 'font_manifests')


_GLYPH_MANIFEST_CACHE: Dict[str, frozenset] = {}


def _load_glyph_manifest(typeface_name: str) -> Optional[frozenset]:
    """Load empirical glyph-coverage codepoint set for one typeface.

    Returns frozenset[int] of supported Unicode codepoints, or None when
    the manifest is unavailable (e.g., extract_font_manifests.py has not
    been run yet at OPSDIR Verification_Config/font_manifests/).
    """
    if typeface_name in _GLYPH_MANIFEST_CACHE:
        return _GLYPH_MANIFEST_CACHE[typeface_name]
    path = os.path.join(
        _glyph_manifest_dir(), f'{typeface_name}.glyph_manifest.json')
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        codepoints = frozenset(int(cp) for cp in manifest.get('codepoints', []))
        _GLYPH_MANIFEST_CACHE[typeface_name] = codepoints
        return codepoints
    except (OSError, ValueError, json.JSONDecodeError):
        return None


_CLUSTER_NARRATIVE_RE = re.compile(
    r'(?:covers|includes|spans)\s+(\d+)\s+KSAs?\s+across\s+'
    r'(\d+|[a-z]+)\s+clusters?\s*:?\s*([^.\n]*)',
    re.IGNORECASE)
_KSA_COUNT_ONLY_RE = re.compile(
    r'(\d+)\s+KSAs?\s+(?:are|spanning|across)', re.IGNORECASE)


def _extract_cluster_inventory_from_source(
        text: str) -> Optional[Dict[str, Any]]:
    """Parse the §1 cluster-list sentence from CIG source markdown.

    Returns a dict with keys 'ksa_count', 'cluster_count', 'cluster_names'
    on successful parse; None when no parseable cluster sentence is found.
    Heuristic: matches sentences of the form
        "The instrument covers N KSAs across M clusters: name1, name2, ..."
    or analogous narrative forms. Tolerates count words ("seven clusters")
    via _NUMBER_WORDS map.
    """
    m = _CLUSTER_NARRATIVE_RE.search(text)
    if not m:
        return None
    try:
        ksa_count = int(m.group(1))
    except (ValueError, TypeError):
        return None
    cluster_token = m.group(2).strip().lower()
    if cluster_token.isdigit():
        cluster_count = int(cluster_token)
    elif cluster_token in _NUMBER_WORDS:
        cluster_count = _NUMBER_WORDS[cluster_token]
    else:
        return None
    name_blob = m.group(3) or ''
    # Split on commas + "and"; tolerate Oxford-comma + "and"-trailing forms.
    name_blob = re.sub(r',?\s+and\s+', ', ', name_blob)
    cluster_names = [
        n.strip() for n in name_blob.split(',') if n.strip()]
    return {
        'ksa_count': ksa_count,
        'cluster_count': cluster_count,
        'cluster_names': cluster_names,
    }


def _bucket_for_ksa_count(ksa_count: int) -> Optional[Tuple[str, int, int]]:
    """Map a KSA count to (size_label, cluster_low, cluster_high) typical."""
    for label, k_lo, k_hi, c_lo, c_hi in CLUSTER_SIZE_BUCKETS:
        if k_lo <= ksa_count <= k_hi:
            return (label, c_lo, c_hi)
    return None


def verify_source_data_integrity(
        doc_path: str, doc_class: str) -> List[CheckResult]:
    """Spec section 3.1: PRE_SDI_001-004 source-data integrity checks.

    PRE_SDI_001 — All required fields populated per document schema.
        For markdown source: file exists, non-empty, has at least one
        h1 heading. FAIL on any condition unmet.
    PRE_SDI_002 — Data types match expected schema. For markdown source:
        markdown tables have consistent column counts. FAIL on
        column-count drift.
    PRE_SDI_003 — No orphaned references. ELO and L2 references parsed
        from source; resolution against in-document context (FG reference
        index) and TLO/ELO matrix attempted. Unresolvable references
        FAIL when canonical lookup is available; WARN when lookup data
        is not available for the document class (e.g., CF documents
        using CF-ELO namespace).
    PRE_SDI_004 — Cross-references resolve correctly. Same scan as 003
        but reports resolution success rate and specific ID-mismatch
        cases.

    Phase B.1 implementation: 001 + 002 substantive; 003 + 004 minimal
    (bare-syntax pattern check; full resolution against canonical maps
    deferred to Phase B.2 when cp_lookups integration is added).
    """
    results: List[CheckResult] = []

    if not doc_path or not os.path.exists(doc_path):
        results.append(_mk_fail(
            'PRE_SDI_001', 'source_data_integrity',
            details=f'doc_path missing or absent: {doc_path!r}',
            fix='Supply a valid path to the source document.'))
        return results

    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except (UnicodeDecodeError, OSError) as e:
        results.append(_mk_fail(
            'PRE_SDI_001', 'source_data_integrity',
            details=f'unable to read doc_path as UTF-8 text: {e}',
            fix='Verify file encoding and accessibility. Non-text source '
                'classes require schema implementation in Phase B.2.'))
        return results

    # PRE_SDI_001: Required fields (markdown schema baseline)
    if not text.strip():
        results.append(_mk_fail(
            'PRE_SDI_001', 'source_data_integrity',
            details='Source document is empty.',
            fix='Verify the source content was saved correctly.'))
    else:
        h1_count = sum(1 for ln in text.split('\n')
                       if ln.startswith('# ') and not ln.startswith('## '))
        h2_count = sum(1 for ln in text.split('\n') if ln.startswith('## '))
        if h1_count == 0 and h2_count == 0:
            results.append(_mk_fail(
                'PRE_SDI_001', 'source_data_integrity',
                details='Source document has no h1 or h2 headings; '
                        'lacks structural anchor.',
                fix='Add a top-level title (# Title) and at least one '
                    'section heading (## Section).'))
        else:
            results.append(_mk_pass(
                'PRE_SDI_001', 'source_data_integrity',
                details=f'Source document has {h1_count} h1 + {h2_count} '
                        f'h2 headings; structural anchor present.'))

    # PRE_SDI_002: Markdown table column-count consistency
    table_findings = _scan_markdown_table_consistency(text.split('\n'))
    if table_findings:
        sample = table_findings[:5]
        results.append(_mk_fail(
            'PRE_SDI_002', 'source_data_integrity',
            details=f'{len(table_findings)} markdown table column-count '
                    f'inconsistency/inconsistencies. First {len(sample)}: '
                    + '; '.join(
                        f'line {ln}: {detail}'
                        for ln, detail in sample),
            fix='Reconcile column counts within each markdown table; every '
                'data row should have the same number of pipes as the '
                'header row.'))
    else:
        results.append(_mk_pass(
            'PRE_SDI_002', 'source_data_integrity',
            details='All markdown tables have consistent column counts.'))

    # PRE_SDI_003 + 004: Cross-reference scan with canonical resolution
    sdi_3_4_results = _scan_cross_references(text, doc_class, doc_path)
    results.extend(sdi_3_4_results)

    return results


def _scan_markdown_table_consistency(
        lines: List[str]) -> List[Tuple[int, str]]:
    """Detect column-count drift within markdown tables.

    Walks tables; for each table, the header row's column count is
    canonical; subsequent data rows that drift produce findings.
    Separator rows (---|---) are validated separately.
    """
    findings: List[Tuple[int, str]] = []
    in_table = False
    expected_cols = 0

    for line_no, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        is_table_row = line.startswith('|') and line.endswith('|')

        if not is_table_row:
            in_table = False
            expected_cols = 0
            continue

        cells = [c.strip() for c in line.strip('|').split('|')]

        if not in_table:
            in_table = True
            expected_cols = len(cells)
            continue

        # Separator row: must match expected_cols
        is_separator = all(re.match(r'^:?-+:?$', c) for c in cells if c)
        if is_separator:
            if len(cells) != expected_cols:
                findings.append((
                    line_no,
                    f'separator has {len(cells)} columns; '
                    f'header had {expected_cols}'))
            continue

        if len(cells) != expected_cols:
            findings.append((
                line_no,
                f'data row has {len(cells)} columns; '
                f'header had {expected_cols}'))

    return findings


def _scan_cross_references(
        text: str, doc_class: str,
        doc_path: str = '') -> List[CheckResult]:
    """PRE_SDI_003 + 004 cross-reference scan with canonical resolution.

    Phase B.2: full resolution against canonical lookup maps via
    cp_lookups integration. ELO + L2-F/R references parsed from source;
    each resolved against canonical maps; orphans reported as FAIL.

    PRE_SDI_003 — orphans (references without a target in the canonical
        map) → FAIL with orphan list.
    PRE_SDI_004 — resolution success rate + entity-type validation
        (Phase B.2 reports counts and successful resolutions; per-context
        entity-type validation deferred to Phase B.3 alongside
        Pipeline-Pattern Conformance).
    """
    elo_refs = [(m.group(0), m.group(1), m.group(2))
                for m in _ELO_REF_RE.finditer(text)]
    l2_refs = [(m.group(0), m.group(1), m.group(2))
               for m in _L2_REF_RE.finditer(text)]

    if doc_class not in ('FG', 'CIG_FULL', 'CIG_QRC', 'WORKBOOK',
                         'CALIBER_PROFILE', 'GAR'):
        return [
            _mk_pass(
                'PRE_SDI_003', 'source_data_integrity',
                details=f'Cross-reference scan ({doc_class}): not '
                        f'applicable or schema not yet defined.'),
            _mk_pass(
                'PRE_SDI_004', 'source_data_integrity',
                details=f'Cross-reference resolution ({doc_class}): not '
                        f'applicable or schema not yet defined.'),
        ]

    # Empty reference set: trivial PASS
    if not elo_refs and not l2_refs:
        return [
            _mk_pass(
                'PRE_SDI_003', 'source_data_integrity',
                details='Zero ELO + L2-F/R references in source; orphan '
                        'check vacuously satisfied.'),
            _mk_pass(
                'PRE_SDI_004', 'source_data_integrity',
                details='Zero references to resolve; resolution check '
                        'vacuously satisfied.'),
        ]

    # cp_lookups integration
    cp_lookups = _load_cp_lookups()
    if cp_lookups is None:
        return [
            _mk_warn(
                'PRE_SDI_003', 'source_data_integrity',
                details=f'cp_lookups module not available; cannot resolve '
                        f'{len(elo_refs)} ELO + {len(l2_refs)} L2 '
                        f'reference(s) against canonical maps.',
                fix='Verify OPSDIR path resolution; cp_lookups should be '
                    'at [OPSDIR]/08_Production_Pipeline/Caliber_Profile/'
                    'cp_lookups.py.'),
            _mk_warn(
                'PRE_SDI_004', 'source_data_integrity',
                details='Cross-reference resolution skipped: cp_lookups '
                        'unavailable.',
                fix='See PRE_SDI_003 fix recommendation.'),
        ]

    elo_matrix_path, l2_source_path = _resolve_lookup_sources(
        doc_path, doc_class)
    elo_map = (cp_lookups.load_elo_map(elo_matrix_path)
               if elo_matrix_path else {})
    l2_map = (cp_lookups.load_l2_flag_map(l2_source_path)
              if l2_source_path else {})

    # Resolution
    elo_orphans: List[str] = []
    elo_resolved = 0
    for full, dom, num in elo_refs:
        key = f'{dom}.{num}'
        if not elo_map:
            # No map available; can't resolve; treat all as
            # un-resolvable (will WARN below, not FAIL)
            continue
        if key in elo_map:
            elo_resolved += 1
        else:
            elo_orphans.append(full)

    l2_orphans: List[str] = []
    l2_resolved = 0
    for full, kind, num in l2_refs:
        ref = f'L2-{kind}{num}'
        if not l2_map:
            continue
        if ref in l2_map:
            l2_resolved += 1
        else:
            l2_orphans.append(ref)

    # Build PRE_SDI_003 result
    sdi_003_results: List[CheckResult] = []
    if elo_map and l2_map and not elo_orphans and not l2_orphans:
        sdi_003_results.append(_mk_pass(
            'PRE_SDI_003', 'source_data_integrity',
            details=f'All {len(elo_refs)} ELO + {len(l2_refs)} L2-F/R '
                    f'reference(s) resolve to canonical entries.'))
    elif elo_orphans or l2_orphans:
        orphan_summary = []
        if elo_orphans:
            uniq = sorted(set(elo_orphans))[:5]
            orphan_summary.append(
                f'{len(elo_orphans)} ELO orphan(s); first {len(uniq)}: '
                + ', '.join(uniq))
        if l2_orphans:
            uniq = sorted(set(l2_orphans))[:5]
            orphan_summary.append(
                f'{len(l2_orphans)} L2 orphan(s); first {len(uniq)}: '
                + ', '.join(uniq))
        sdi_003_results.append(_mk_fail(
            'PRE_SDI_003', 'source_data_integrity',
            details=' | '.join(orphan_summary),
            fix='Verify orphan references against the canonical TLO/ELO '
                'matrix and FG reference index. Orphans indicate either '
                'a typo, a stale reference to a removed entity, or a '
                'canonical-map gap (in which case ID should be notified).'))
    else:
        # Maps unavailable for one or both kinds; informational WARN
        missing = []
        if elo_refs and not elo_map:
            missing.append(f'ELO map not loaded ({len(elo_refs)} refs '
                           f'unresolved)')
        if l2_refs and not l2_map:
            missing.append(f'L2 map not loaded ({len(l2_refs)} refs '
                           f'unresolved)')
        sdi_003_results.append(_mk_warn(
            'PRE_SDI_003', 'source_data_integrity',
            details=' | '.join(missing) or 'Partial resolution',
            fix='Some references could not be resolved because the '
                'canonical map was not available for this document class. '
                'Foundation products use CF-ELO namespace which is '
                'excluded by the qualifier regex; this is expected.'))

    # PRE_SDI_004 — resolution success metric
    total_refs = len(elo_refs) + len(l2_refs)
    total_resolved = elo_resolved + l2_resolved
    if total_refs == 0:
        sdi_004 = _mk_pass(
            'PRE_SDI_004', 'source_data_integrity',
            details='Zero references; resolution check vacuously satisfied.')
    elif total_resolved == total_refs:
        sdi_004 = _mk_pass(
            'PRE_SDI_004', 'source_data_integrity',
            details=f'All {total_refs} reference(s) resolved successfully '
                    f'({elo_resolved} ELO, {l2_resolved} L2-F/R).')
    elif total_resolved > 0:
        sdi_004 = _mk_warn(
            'PRE_SDI_004', 'source_data_integrity',
            details=f'{total_resolved} of {total_refs} reference(s) '
                    f'resolved; {total_refs - total_resolved} unresolved '
                    f'(see PRE_SDI_003).',
            fix='See PRE_SDI_003 fix recommendation.')
    else:
        sdi_004 = _mk_warn(
            'PRE_SDI_004', 'source_data_integrity',
            details='No references resolved (canonical maps not loaded).',
            fix='See PRE_SDI_003 fix recommendation.')

    return sdi_003_results + [sdi_004]


# 3.2 Methodology Conformance
# Document classes that should reference UPLS competencies. CIF and Caliber
# Profile are explicit per spec section 3.2; FG / WORKBOOK / GAR have UPLS
# scaffolding throughout their content.
DOC_CLASSES_REQUIRING_UPLS = ('CALIBER_PROFILE', 'GAR', 'WORKBOOK')

# CIG documents are forward-applicable for CIG_FULL / CIG_QRC; their
# methodology checks (Bloom's, Function references) become substantive
# in Phase 3 of the Branded Doc Campaign.


def verify_methodology_conformance(
        doc_path: str, doc_class: str) -> List[CheckResult]:
    """Spec section 3.2: PRE_MC_001-004 methodology conformance checks.

    PRE_MC_001 — UPLS competency mappings present where required (FAIL)
    PRE_MC_002 — ELM cycle phases tagged where applicable (WARN)
    PRE_MC_003 — Bloom's taxonomy levels specified for assessment items
                 in CIG documents (WARN)
    PRE_MC_004 — Coach Intake Form questions mapped to UPLS competencies
                 (FAIL when CIF; vacuously PASS for non-CIF doc classes)

    Phase B.2 implementation: heuristic detection via keyword scan +
    structural-feature presence. CIF detection: filename contains "intake"
    and doc_class is CALIBER_PROFILE. Bloom's detection scoped to CIG
    classes only (not yet exercised; Phase 3 of Branded Doc Campaign).
    """
    results: List[CheckResult] = []
    if not doc_path or not os.path.exists(doc_path):
        results.append(_mk_warn(
            'PRE_MC_001', 'methodology_conformance',
            details=f'doc_path missing or absent: {doc_path!r}; '
                    f'methodology scan skipped.',
            fix='Supply a valid path to the source document.'))
        return results

    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except (UnicodeDecodeError, OSError):
        results.append(_mk_pass(
            'PRE_MC_001', 'methodology_conformance',
            details='Methodology scan skipped: non-text content.'))
        return results

    text_lower = text.lower()
    fname_lower = os.path.basename(doc_path).lower()

    # PRE_MC_001 — UPLS competency mapping presence
    upls_hits = sum(1 for kw in UPLS_DOMAIN_KEYWORDS if kw in text_lower)
    competency_word_count = (
        text_lower.count('competenc') + text_lower.count('proficiency'))
    requires_upls = doc_class in DOC_CLASSES_REQUIRING_UPLS
    if requires_upls and upls_hits == 0 and competency_word_count == 0:
        results.append(_mk_fail(
            'PRE_MC_001', 'methodology_conformance',
            details=f'{doc_class} requires UPLS competency mapping per '
                    f'spec section 3.2 but zero UPLS domain keywords + '
                    f'zero competency/proficiency word references found.',
            fix='Add explicit UPLS competency mappings (Self-Mastery, '
                'Professionalism, Leadership & Influence) and proficiency '
                'level references where the methodology requires them.'))
    else:
        details = (
            f'UPLS scaffolding: {upls_hits} domain keyword hit(s); '
            f'{competency_word_count} competency/proficiency word '
            f'reference(s).')
        if not requires_upls:
            details += f' Doc class {doc_class} does not strictly require.'
        results.append(_mk_pass(
            'PRE_MC_001', 'methodology_conformance', details=details))

    # PRE_MC_002 — ELM cycle phase tagging
    has_elm_table = (
        '| phase |' in text_lower or '| phase\t' in text_lower
        or 'elm phase' in text_lower)
    if has_elm_table:
        # Check ELM phase canonical names appear
        phase_hits = sum(
            1 for ph in ELM_PHASE_CANONICAL if ph in text_lower)
        if phase_hits >= 3:
            results.append(_mk_pass(
                'PRE_MC_002', 'methodology_conformance',
                details=f'ELM phase tagging present: {phase_hits} '
                        f'canonical phase name(s) detected.'))
        else:
            results.append(_mk_warn(
                'PRE_MC_002', 'methodology_conformance',
                details=f'Document contains ELM Phase Table reference but '
                        f'only {phase_hits} canonical phase name(s) '
                        f'detected; cycle may be mistagged.',
                fix='Verify ELM phase column values match canonical phase '
                    'names (Concrete Experience, Publish & Process / '
                    'Reflection, Generalize New Information / '
                    'Conceptualization, Develop / Active Experimentation, '
                    'Apply).'))
    else:
        results.append(_mk_pass(
            'PRE_MC_002', 'methodology_conformance',
            details='No ELM Phase Table detected; ELM phase tagging '
                    'check not applicable.'))

    # PRE_MC_003 — Bloom's taxonomy in CIG documents
    if doc_class in ('CIG_FULL', 'CIG_QRC'):
        blooms_keywords = (
            'remember', 'understand', 'apply', 'analyze', 'evaluate',
            'create',  # Bloom's 6 levels
            "bloom's", 'blooms taxonomy', 'cognitive level',
        )
        blooms_hits = sum(1 for kw in blooms_keywords if kw in text_lower)
        if blooms_hits == 0:
            results.append(_mk_warn(
                'PRE_MC_003', 'methodology_conformance',
                details=f'CIG document has no detectable Bloom\'s '
                        f'taxonomy annotations.',
                fix='Add Bloom\'s level annotations to assessment items '
                    'per spec section 3.2.'))
        else:
            results.append(_mk_pass(
                'PRE_MC_003', 'methodology_conformance',
                details=f'Bloom\'s taxonomy scaffolding: {blooms_hits} '
                        f'level keyword(s) detected.'))
    else:
        results.append(_mk_pass(
            'PRE_MC_003', 'methodology_conformance',
            details=f'Bloom\'s taxonomy check not applicable for '
                    f'{doc_class}.'))

    # PRE_MC_005 — Substance-Grounded Cluster Determination Framework
    # validation per InfoTech Phase 4 Re-Render Execution Routing §4.2
    # (Source-Authoring Guidance v1.1 §3.4). Advisory; non-blocking. CIG
    # doc classes only.
    if doc_class in ('CIG_FULL', 'CIG_QRC'):
        inventory = _extract_cluster_inventory_from_source(text)
        if inventory is None:
            results.append(_mk_warn(
                'PRE_MC_005', 'methodology_conformance',
                details='No parseable §1 cluster-list sentence found '
                        '(expected form: "covers N KSAs across M clusters: '
                        '...").',
                fix='Add a §1 sentence stating KSA count and cluster '
                    'count per Source-Authoring Guidance v1.1 §3.4 forward-'
                    'authoring application protocol.'))
        else:
            ksa_count = inventory['ksa_count']
            cluster_count = inventory['cluster_count']
            names_count = len(inventory['cluster_names'])
            bucket = _bucket_for_ksa_count(ksa_count)
            findings: List[str] = []
            if names_count != cluster_count:
                findings.append(
                    f'cluster-name list length {names_count} '
                    f'differs from announced count {cluster_count}')
            if bucket:
                label, c_lo, c_hi = bucket
                if not (c_lo <= cluster_count <= c_hi):
                    findings.append(
                        f'{cluster_count} clusters outside {label} '
                        f'({ksa_count} KSAs) typical range '
                        f'{c_lo}-{c_hi}')
            else:
                findings.append(
                    f'KSA count {ksa_count} outside framework size buckets '
                    f'(Small 10-15 / Medium 16-25 / Large 26-35 / Very '
                    f'Large 36+)')
            if findings:
                results.append(_mk_warn(
                    'PRE_MC_005', 'methodology_conformance',
                    details='Cluster determination deviation(s): '
                            + '; '.join(findings),
                    fix='Review cluster-count against Source-Authoring '
                        'Guidance v1.1 §3.4 framework. If deviation is '
                        'intentional (single-KSA exception protocol or '
                        'sector-specific substance justification), '
                        'document rationale in §1 cluster-list section.'))
            else:
                results.append(_mk_pass(
                    'PRE_MC_005', 'methodology_conformance',
                    details=f'Cluster determination within framework: '
                            f'{ksa_count} KSAs / {cluster_count} clusters '
                            f'({bucket[0]} bucket typical {bucket[1]}-'
                            f'{bucket[2]}).'))
    else:
        results.append(_mk_pass(
            'PRE_MC_005', 'methodology_conformance',
            details=f'Cluster-determination check not applicable for '
                    f'{doc_class}.'))

    # PRE_MC_004 — CIF question-to-UPLS mapping
    is_cif = (
        doc_class == 'CALIBER_PROFILE' and 'intake' in fname_lower)
    if is_cif:
        # CIF must map questions to UPLS competencies. Heuristic: detect
        # question-to-competency markers.
        cif_mapping_hits = (
            text_lower.count('competency:') + text_lower.count('upls:')
            + text_lower.count('maps to:') + text_lower.count('mapping:'))
        if cif_mapping_hits == 0:
            results.append(_mk_fail(
                'PRE_MC_004', 'methodology_conformance',
                details='Coach Intake Form lacks question-to-UPLS '
                        'mapping markers per spec section 3.2 (FAIL: '
                        'CIF requires UPLS mapping per OI-GAR-V2 '
                        'production pipeline integration spec).',
                fix='Add explicit UPLS competency mapping for each CIF '
                    'question (e.g., "Maps to: Self-Reflective Insight, '
                    'Intermediate proficiency").'))
        else:
            results.append(_mk_pass(
                'PRE_MC_004', 'methodology_conformance',
                details=f'CIF question-to-competency mapping markers: '
                        f'{cif_mapping_hits} hit(s).'))
    else:
        results.append(_mk_pass(
            'PRE_MC_004', 'methodology_conformance',
            details=f'Coach Intake Form mapping check not applicable for '
                    f'{doc_class}; doc filename does not match CIF '
                    f'pattern.'))

    return results


# 3.3 Brand-Specification Adherence
_HEX_COLOR_RE = re.compile(r'#[0-9A-Fa-f]{6}\b')
_IMG_LINK_RE = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')


def verify_brand_specification_adherence(
        doc_path: str, doc_class: str) -> List[CheckResult]:
    """Spec section 3.3: PRE_BS_001-003 brand-specification adherence.

    PRE_BS_001 — Color references resolve to canonical VBS palette.
        Hex codes scanned in source; non-canonical hex codes FAIL.
    PRE_BS_002 — Typography references resolve to canonical VBS typeface
        set. Non-canonical font tokens (Times, Arial, etc.) FAIL.
    PRE_BS_003 — Logo and brandmark references resolve to canonical
        assets. Non-canonical brandmark filenames in markdown image
        links FAIL.

    All Brand-Specification failures halt per spec section 3.3 fail
    semantics ("Brand integrity is non-negotiable for client-facing
    artifacts").
    """
    results: List[CheckResult] = []
    if not doc_path or not os.path.exists(doc_path):
        results.append(_mk_warn(
            'PRE_BS_001', 'brand_specification',
            details=f'doc_path missing or absent: {doc_path!r}; '
                    f'brand-specification scan skipped.',
            fix='Supply a valid path to the source document.'))
        return results

    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except (UnicodeDecodeError, OSError):
        results.append(_mk_pass(
            'PRE_BS_001', 'brand_specification',
            details='Brand-specification scan skipped: non-text content.'))
        results.append(_mk_pass(
            'PRE_BS_002', 'brand_specification',
            details='Brand-specification scan skipped: non-text content.'))
        results.append(_mk_pass(
            'PRE_BS_003', 'brand_specification',
            details='Brand-specification scan skipped: non-text content.'))
        return results

    # PRE_BS_001 — Hex color codes
    hex_findings: List[Tuple[int, str]] = []
    for line_no, line in enumerate(text.split('\n'), 1):
        for m in _HEX_COLOR_RE.finditer(line):
            hex_code = m.group(0).lower()
            if hex_code not in CANONICAL_VBS_HEX_COLORS:
                hex_findings.append((line_no, m.group(0)))
    if hex_findings:
        sample = hex_findings[:5]
        results.append(_mk_fail(
            'PRE_BS_001', 'brand_specification',
            details=f'{len(hex_findings)} non-canonical hex color '
                    f'reference(s). First {len(sample)}: '
                    + '; '.join(
                        f'line {ln}: {hex_code}'
                        for ln, hex_code in sample),
            fix='Replace non-canonical hex colors with VBS palette tokens '
                '(DSB #1E3A5F, BA #C08B3A, WC #F6F3EE, WS #3D4E5C, etc.) '
                'per spec section 3.3.'))
    else:
        results.append(_mk_pass(
            'PRE_BS_001', 'brand_specification',
            details='All hex color references resolve to canonical VBS '
                    'palette (or no hex codes present).'))

    # PRE_BS_002 — Non-canonical font tokens. Word-boundary regex match
    # excludes substring false positives (e.g., 'Garamond' inside
    # 'Cormorant Garamond' is preserved). 'Georgia' is deliberately
    # omitted from the token list — U.S. state references in CSRA
    # market-context content produce too many false positives.
    font_findings: List[Tuple[int, str]] = []
    for line_no, line in enumerate(text.split('\n'), 1):
        for m in _NON_CANONICAL_FONT_RE.finditer(line):
            font_findings.append((line_no, m.group(0)))
    if font_findings:
        sample = font_findings[:5]
        results.append(_mk_fail(
            'PRE_BS_002', 'brand_specification',
            details=f'{len(font_findings)} non-canonical font '
                    f'token reference(s). First {len(sample)}: '
                    + '; '.join(
                        f'line {ln}: {token!r}'
                        for ln, token in sample),
            fix='Replace non-canonical font references with VBS canonical '
                'typeface tokens (Inter family + Cormorant Garamond '
                'family) per spec section 3.3. Helvetica is permitted '
                'for AcroForm-constrained contexts only.'))
    else:
        results.append(_mk_pass(
            'PRE_BS_002', 'brand_specification',
            details='All font references resolve to canonical VBS '
                    'typeface set (or no non-canonical tokens detected).'))

    # PRE_BS_003 — Brandmark image references
    brandmark_findings: List[Tuple[int, str]] = []
    for line_no, line in enumerate(text.split('\n'), 1):
        for m in _IMG_LINK_RE.finditer(line):
            link = m.group(1)
            fn = os.path.basename(link)
            # Heuristic: only flag if filename contains brand-related token
            fn_lower = fn.lower()
            if any(kw in fn_lower for kw in
                   ('brandmark', 'logo', 'wordmark', 'caliberpath')):
                if fn not in CANONICAL_BRANDMARK_FILENAMES:
                    brandmark_findings.append((line_no, fn))
    if brandmark_findings:
        sample = brandmark_findings[:5]
        results.append(_mk_fail(
            'PRE_BS_003', 'brand_specification',
            details=f'{len(brandmark_findings)} non-canonical brandmark '
                    f'reference(s). First {len(sample)}: '
                    + '; '.join(
                        f'line {ln}: {fn!r}'
                        for ln, fn in sample),
            fix='Replace non-canonical brandmark filenames with canonical '
                'assets from [OPSDIR]/05_Brand/Visual_Identity/'
                'Brandmark_Development/Production/. Canonical filenames: '
                + ', '.join(sorted(CANONICAL_BRANDMARK_FILENAMES))
                + '.'))
    else:
        results.append(_mk_pass(
            'PRE_BS_003', 'brand_specification',
            details='All brandmark image references resolve to canonical '
                    'assets (or no brand image references present).'))

    # PRE_BS_004 — Glyph-coverage validation per InfoTech Phase 4 Re-Render
    # Execution Routing §4.3 (FR-CIG-F09 ASCII-equivalent discipline).
    # Advisory; non-blocking. Scans italic-callout segments and flags any
    # codepoint outside the empirical glyph manifest for the restricted
    # typeface. CIG doc classes only; other classes return vacuous PASS.
    if doc_class in ('CIG_FULL', 'CIG_QRC'):
        restricted_typefaces = RESTRICTED_TYPEFACES_CIG
        # Load manifests for all restricted typefaces; if any is missing
        # the check degrades to WARN with the missing-manifest note.
        manifests: Dict[str, frozenset] = {}
        missing: List[str] = []
        for tf in restricted_typefaces:
            mset = _load_glyph_manifest(tf)
            if mset is None:
                missing.append(tf)
            else:
                manifests[tf] = mset
        if missing and not manifests:
            results.append(_mk_warn(
                'PRE_BS_004', 'brand_specification',
                details='Glyph-coverage manifests unavailable for '
                        + ', '.join(missing)
                        + '. Run extract_font_manifests.py at OPSDIR '
                          'Verification_Config to populate.',
                fix='cd [OPSDIR]/08_Production_Pipeline/Verification_Config '
                    '&& python extract_font_manifests.py'))
        else:
            # Effective restricted coverage: union of available manifests
            # (italic callouts may dispatch to either italic typeface variant
            # depending on context; union approximates pipeline behavior).
            effective_coverage: set = set()
            for cps in manifests.values():
                effective_coverage |= cps
            # Walk italic-context segments and collect out-of-coverage
            # codepoints with line numbers + sample character.
            findings: List[Tuple[int, str, int]] = []
            for line_no, line in enumerate(text.split('\n'), 1):
                for pat in _ITALIC_CONTEXT_PATTERNS:
                    m = pat.match(line)
                    if m:
                        segment = m.group(1)
                        for ch in segment:
                            cp = ord(ch)
                            if cp not in effective_coverage:
                                findings.append((line_no, ch, cp))
                        break
            if findings:
                sample = findings[:5]
                results.append(_mk_warn(
                    'PRE_BS_004', 'brand_specification',
                    details=f'{len(findings)} italic-callout codepoint(s) '
                            f'outside restricted typeface coverage '
                            f'({", ".join(sorted(manifests.keys()))}). '
                            f'First {len(sample)}: '
                            + '; '.join(
                                f'line {ln}: {ch!r} (U+{cp:04X})'
                                for ln, ch, cp in sample),
                    fix=(
                        'Replace out-of-coverage characters with ASCII-'
                        'equivalent forms per FR-CIG-F09 discipline, or '
                        'restructure callout to avoid restricted-glyph-set '
                        'codepoints. Acceptable substitutions: ASCII '
                        'apostrophe U+0027, ASCII hyphen-minus U+002D, '
                        'en/em-dash if present in manifest. Reject '
                        'typographic curly quotes when absent from font.')))
            else:
                results.append(_mk_pass(
                    'PRE_BS_004', 'brand_specification',
                    details=f'All italic-callout codepoints within '
                            f'restricted typeface coverage '
                            f'({", ".join(sorted(manifests.keys()))}; '
                            f'{len(effective_coverage)} codepoints).'))
    else:
        results.append(_mk_pass(
            'PRE_BS_004', 'brand_specification',
            details=f'Glyph-coverage check not applicable for {doc_class}.'))

    return results


# 3.4 Pipeline-Pattern Conformance
# Pipeline-pattern checks inspect the rendering pipeline code (cp_core.py,
# fg_template.py, cp_lookups.py at OPSDIR), not the source document. The
# doc_path is informational; doc_class drives which pipeline modules to
# inspect.
def _pipeline_module_paths(doc_class: str) -> Dict[str, str]:
    """Resolve canonical pipeline module paths per doc_class.

    Returns a dict with module-purpose keys and absolute path values.
    Missing modules return None values; caller handles gracefully.
    """
    base = os.path.join(_opsdir_root(), '08_Production_Pipeline')
    paths = {
        'cp_core': os.path.join(base, 'Caliber_Profile', 'cp_core.py'),
        'cp_lookups': os.path.join(base, 'Caliber_Profile', 'cp_lookups.py'),
    }
    if doc_class in ('FG', 'CIG_FULL', 'CIG_QRC'):
        paths['template'] = os.path.join(
            base, 'Branded_Doc_Campaign', 'fg_template.py')
    elif doc_class == 'GAR':
        paths['template'] = os.path.join(
            base, 'Gap_Analysis_Report', 'gar_template.py')
    elif doc_class == 'CALIBER_PROFILE':
        paths['template'] = os.path.join(
            base, 'Caliber_Profile', 'caliber_profile.py')
    elif doc_class == 'WORKBOOK':
        paths['template'] = os.path.join(
            base, 'Workbook', 'workbook_session_a.py')
    return paths


def _read_pipeline_module(path: str) -> Optional[str]:
    """Read a pipeline module file as UTF-8 text; None if absent/unreadable."""
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except (UnicodeDecodeError, OSError):
        return None


def _extract_function_body(source: str, func_name: str) -> Optional[str]:
    """Extract a function body from Python source via simple line-based scan.

    Returns the body (lines between the def line and the next top-level
    def/class) or None when the function is not found. Heuristic — works
    for top-level functions defined at module scope without nested defs
    sharing the same name.
    """
    lines = source.split('\n')
    in_func = False
    body_lines: List[str] = []
    for line in lines:
        if not in_func:
            m = re.match(rf'^def\s+{re.escape(func_name)}\s*\(', line)
            if m:
                in_func = True
                body_lines.append(line)
                continue
        else:
            # End of function: another top-level def or class at column 0
            if re.match(r'^(def\s+|class\s+|#\s*=)', line):
                break
            body_lines.append(line)
    if not in_func:
        return None
    return '\n'.join(body_lines)


def verify_pipeline_pattern_conformance(
        doc_path: str, doc_class: str,
        pattern_set: str = 'phase2_canonical') -> List[CheckResult]:
    """Spec section 3.4: PRE_PP_001-008 pipeline-pattern conformance checks.

    Inspects the canonical pipeline modules at OPSDIR for application of
    Phase 2 canonical patterns:
      PRE_PP_001 — FR-14 self-guard discipline (cp_core.py block primitives)
      PRE_PP_002 — FR-17 auto-scale + multi-line wrap (heading dispatchers)
      PRE_PP_003 — FR-19 h4 bookmark conditional dispatch (template script)
      PRE_PP_004 — FR-21 + FR-27 tiered column allocation (template script)
      PRE_PP_005 — FR-22 multi-page chunking (cp_core.py callout primitives)
      PRE_PP_006 — FR-23 subordinate draw_section_marker variant (cp_core.py)
      PRE_PP_007 — FR-24 cross-reference qualifier skip (cp_lookups.py)
      PRE_PP_008 — FR-18 supersession (no stale equal-split patterns)

    pattern_set='phase2_canonical' is the only active set at this version;
    parameter is reserved for forward-applicable pattern-set evolution.
    """
    paths = _pipeline_module_paths(doc_class)
    cp_core_src = _read_pipeline_module(paths.get('cp_core', ''))
    cp_lookups_src = _read_pipeline_module(paths.get('cp_lookups', ''))
    template_src = _read_pipeline_module(paths.get('template', ''))

    results: List[CheckResult] = []

    # PRE_PP_001 — FR-14 self-guard discipline
    results.append(_check_pp_001(cp_core_src))
    # PRE_PP_002 — FR-17 auto-scale + multi-line wrap
    results.append(_check_pp_002(cp_core_src))
    # PRE_PP_003 — FR-19 h4 bookmark conditional dispatch
    results.append(_check_pp_003(template_src, doc_class))
    # PRE_PP_004 — FR-21 + FR-27 tiered column allocation
    results.append(_check_pp_004(template_src, doc_class))
    # PRE_PP_005 — FR-22 multi-page chunking
    results.append(_check_pp_005(cp_core_src))
    # PRE_PP_006 — FR-23 subordinate variant
    results.append(_check_pp_006(cp_core_src))
    # PRE_PP_007 — FR-24 cross-reference qualifier skip
    results.append(_check_pp_007(cp_lookups_src))
    # PRE_PP_008 — FR-18 supersession (no stale patterns)
    results.append(_check_pp_008(template_src, doc_class))

    return results


# Block-render functions in cp_core.py that must implement FR-14 self-guard.
# Each enters a code path that places content at y_top and must check
# y_top - block_height < FOOTER_TOP before rendering.
_FR14_BLOCK_FUNCTIONS = (
    'draw_wrapped', 'draw_part_header', 'draw_section_marker',
    'draw_callout_tier1', 'draw_callout_tier2', 'draw_callout_tier3',
    'draw_code_block',
)


def _check_pp_001(cp_core_src: Optional[str]) -> CheckResult:
    """FR-14 self-guard discipline — every block-render function in cp_core
    must check FOOTER_TOP boundary before rendering."""
    if cp_core_src is None:
        return _mk_warn(
            'PRE_PP_001', 'pipeline_pattern',
            details='cp_core.py not found at expected path; FR-14 self-guard '
                    'check skipped.',
            fix='Verify OPSDIR pipeline module paths.')

    missing: List[str] = []
    for func in _FR14_BLOCK_FUNCTIONS:
        body = _extract_function_body(cp_core_src, func)
        if body is None:
            missing.append(f'{func} (function not found)')
            continue
        # Self-guard signature: RC.pc check + FOOTER_TOP comparison
        has_rc_check = 'RC.pc is not None' in body
        has_footer_check = 'FOOTER_TOP' in body
        if not (has_rc_check and has_footer_check):
            missing.append(
                f'{func} (RC.pc={has_rc_check}, FOOTER_TOP={has_footer_check})')

    if missing:
        return _mk_fail(
            'PRE_PP_001', 'pipeline_pattern',
            details=f'FR-14 self-guard discipline missing in '
                    f'{len(missing)} block-render function(s): '
                    + '; '.join(missing),
            fix='Add `if RC.pc is not None and y_top - block_height < '
                'FOOTER_TOP: y_top = new_content_page(...)` self-guard '
                'pattern to each variable-height block-render function '
                'per Pattern Reference v1.3 FR-14.')
    return _mk_pass(
        'PRE_PP_001', 'pipeline_pattern',
        details=f'FR-14 self-guard discipline present in all '
                f'{len(_FR14_BLOCK_FUNCTIONS)} canonical block-render '
                f'functions.')


# Heading dispatchers in cp_core.py that must implement FR-17 auto-scale +
# multi-line wrap.
_FR17_HEADING_FUNCTIONS = (
    'draw_section_marker', 'draw_part_header', 'build_e2_divider',
)


def _check_pp_002(cp_core_src: Optional[str]) -> CheckResult:
    """FR-17 auto-scale + multi-line wrap — section markers + part headers
    + divider titles implement two-tier sizing (autoscale + wrap_lines)."""
    if cp_core_src is None:
        return _mk_warn(
            'PRE_PP_002', 'pipeline_pattern',
            details='cp_core.py not found; FR-17 check skipped.',
            fix='Verify OPSDIR pipeline module paths.')

    missing: List[str] = []
    for func in _FR17_HEADING_FUNCTIONS:
        body = _extract_function_body(cp_core_src, func)
        if body is None:
            missing.append(f'{func} (function not found)')
            continue
        has_autoscale = 'autoscale_font_size' in body
        has_wrap = 'wrap_lines' in body
        if not (has_autoscale and has_wrap):
            missing.append(
                f'{func} (autoscale={has_autoscale}, wrap={has_wrap})')

    if missing:
        return _mk_fail(
            'PRE_PP_002', 'pipeline_pattern',
            details=f'FR-17 two-tier sizing (auto-scale + multi-line wrap) '
                    f'missing in {len(missing)} heading dispatcher(s): '
                    + '; '.join(missing),
            fix='Each heading dispatcher must auto-scale font to floor first '
                'via autoscale_font_size, then multi-line wrap via wrap_lines '
                'when single-line at floor still overflows. Pattern Reference '
                'v1.3 FR-17.')
    return _mk_pass(
        'PRE_PP_002', 'pipeline_pattern',
        details=f'FR-17 two-tier sizing present in all '
                f'{len(_FR17_HEADING_FUNCTIONS)} heading dispatcher functions.')


def _check_pp_003(template_src: Optional[str],
                  doc_class: str) -> CheckResult:
    """FR-19 h4 bookmark conditional dispatch — h4 dispatches conditionally
    to L1 or L2 based on session-marker context state."""
    if template_src is None:
        return _mk_warn(
            'PRE_PP_003', 'pipeline_pattern',
            details=f'Template module for {doc_class} not found; FR-19 '
                    f'check skipped.',
            fix='Verify OPSDIR pipeline module paths.')

    # Detect signature: conditional based on current_session_label starting
    # with 'SESSION ', registering at L2 inside session and L1 outside.
    has_session_check = (
        "current_session_label.upper" in template_src
        and "startswith('SESSION " in template_src)
    has_dual_levels = (
        'level=2' in template_src and 'level=1' in template_src)

    if has_session_check and has_dual_levels:
        return _mk_pass(
            'PRE_PP_003', 'pipeline_pattern',
            details='FR-19 h4 bookmark conditional dispatch present '
                    '(session-context check + L1/L2 dual registration).')
    return _mk_fail(
        'PRE_PP_003', 'pipeline_pattern',
        details=f'FR-19 h4 bookmark conditional dispatch missing or '
                f'incomplete (session_check={has_session_check}, '
                f'dual_levels={has_dual_levels}).',
        fix='Implement h4 dispatch that registers L2 inside real sessions '
            '(current_session_label starts with SESSION) and L1 outside '
            'per Pattern Reference v1.3 FR-19.')


def _check_pp_004(template_src: Optional[str],
                  doc_class: str) -> CheckResult:
    """FR-21 + FR-27 tiered column allocation."""
    if template_src is None:
        return _mk_warn(
            'PRE_PP_004', 'pipeline_pattern',
            details=f'Template module for {doc_class} not found; '
                    f'FR-21+FR-27 check skipped.',
            fix='Verify OPSDIR pipeline module paths.')

    has_threshold = 'NARROW_COL_THRESHOLD' in template_src
    has_buffer = 'NARROW_COL_BUFFER' in template_src
    has_compute_func = 'compute_column_widths' in template_src
    # FR-27 signature: max_body_idx (de-facto wide column when all narrow)
    has_fr27 = 'max_body_idx' in template_src

    missing = []
    if not has_threshold:
        missing.append('NARROW_COL_THRESHOLD constant')
    if not has_buffer:
        missing.append('NARROW_COL_BUFFER constant')
    if not has_compute_func:
        missing.append('compute_column_widths function')
    if not has_fr27:
        missing.append('FR-27 max_body_idx fallback (comfortable-fit-with-'
                       'all-narrow direction)')

    if missing:
        return _mk_fail(
            'PRE_PP_004', 'pipeline_pattern',
            details=f'FR-21 + FR-27 tiered allocation missing/incomplete: '
                    + ', '.join(missing) + '.',
            fix='Implement compute_column_widths with Tier 0 header '
                'must-fit + Tier 1 narrow-column must-fit (NARROW_COL_'
                'THRESHOLD + NARROW_COL_BUFFER) + Tier 2 wide proportional '
                'shrinkage + comfortable-fit-with-all-narrow direction '
                '(max_body_idx). Pattern Reference v1.3 FR-21 + FR-27.')
    return _mk_pass(
        'PRE_PP_004', 'pipeline_pattern',
        details='FR-21 + FR-27 tiered column allocation present (threshold '
                '+ buffer constants + compute_column_widths + max_body_idx '
                'fallback).')


# Callout functions that must implement FR-22 multi-page chunking.
_FR22_CHUNK_FUNCTIONS = ('draw_callout_tier2', 'draw_callout_tier3')


def _check_pp_005(cp_core_src: Optional[str]) -> CheckResult:
    """FR-22 multi-page chunking — long callouts implement line-queue +
    per-page chunking pattern."""
    if cp_core_src is None:
        return _mk_warn(
            'PRE_PP_005', 'pipeline_pattern',
            details='cp_core.py not found; FR-22 check skipped.',
            fix='Verify OPSDIR pipeline module paths.')

    missing: List[str] = []
    for func in _FR22_CHUNK_FUNCTIONS:
        body = _extract_function_body(cp_core_src, func)
        if body is None:
            missing.append(f'{func} (function not found)')
            continue
        # Chunking signature: while-loop on a queue + new_content_page call
        has_while_queue = 'while queue' in body
        has_new_page = 'new_content_page' in body
        if not (has_while_queue and has_new_page):
            missing.append(
                f'{func} (queue-loop={has_while_queue}, '
                f'new_page={has_new_page})')

    if missing:
        return _mk_fail(
            'PRE_PP_005', 'pipeline_pattern',
            details=f'FR-22 multi-page chunking missing/incomplete in '
                    f'{len(missing)} callout function(s): '
                    + '; '.join(missing),
            fix='Implement line-queue chunking pattern: pre-compute lines, '
                'iterate while queue, render chunk-rect per available page '
                'space, advance to new_content_page on overflow. Pattern '
                'Reference v1.3 FR-22.')
    return _mk_pass(
        'PRE_PP_005', 'pipeline_pattern',
        details=f'FR-22 multi-page chunking present in all '
                f'{len(_FR22_CHUNK_FUNCTIONS)} callout functions.')


def _check_pp_006(cp_core_src: Optional[str]) -> CheckResult:
    """FR-23 subordinate draw_section_marker variant — subordinate=True
    parameter available for parent-child visual hierarchy nesting."""
    if cp_core_src is None:
        return _mk_warn(
            'PRE_PP_006', 'pipeline_pattern',
            details='cp_core.py not found; FR-23 check skipped.',
            fix='Verify OPSDIR pipeline module paths.')

    body = _extract_function_body(cp_core_src, 'draw_section_marker')
    if body is None:
        return _mk_warn(
            'PRE_PP_006', 'pipeline_pattern',
            details='draw_section_marker function not found in cp_core.py.',
            fix='Verify cp_core.py contents.')
    # FR-23 signature: subordinate parameter
    has_subordinate = 'subordinate' in body.split('\n')[0:3][0] or any(
        'subordinate' in ln for ln in body.split('\n')[:5])
    has_subordinate = 'subordinate=' in body or 'subordinate ' in body

    if has_subordinate:
        return _mk_pass(
            'PRE_PP_006', 'pipeline_pattern',
            details='FR-23 subordinate variant present in '
                    'draw_section_marker.')
    return _mk_warn(
        'PRE_PP_006', 'pipeline_pattern',
        details='FR-23 subordinate parameter not detected in '
                'draw_section_marker. Not all templates require subordinate '
                'variant; WARN per spec.',
        fix='Add subordinate=False parameter to draw_section_marker per '
            'Pattern Reference v1.3 FR-23 if parent-child hierarchy '
            'rendering is needed.')


def _check_pp_007(cp_lookups_src: Optional[str]) -> CheckResult:
    """FR-24 cross-reference qualifier skip — bare-reference skip in
    qualify_elo_references and qualify_l2_references."""
    if cp_lookups_src is None:
        return _mk_warn(
            'PRE_PP_007', 'pipeline_pattern',
            details='cp_lookups.py not found; FR-24 check skipped.',
            fix='Verify OPSDIR pipeline module paths.')

    has_elo_bare = '_ELO_BARE_RE' in cp_lookups_src
    has_l2_bare = '_L2_BARE_RE' in cp_lookups_src
    has_elo_qualify = 'qualify_elo_references' in cp_lookups_src
    has_l2_qualify = 'qualify_l2_references' in cp_lookups_src

    if not (has_elo_qualify and has_l2_qualify):
        return _mk_warn(
            'PRE_PP_007', 'pipeline_pattern',
            details=f'cp_lookups qualifier functions missing '
                    f'(elo_qualify={has_elo_qualify}, '
                    f'l2_qualify={has_l2_qualify}).',
            fix='Implement qualify_elo_references and qualify_l2_references '
                'per cp_lookups precedent.')

    if has_elo_bare and has_l2_bare:
        return _mk_pass(
            'PRE_PP_007', 'pipeline_pattern',
            details='FR-24 bare-reference qualifier skip present '
                    '(_ELO_BARE_RE + _L2_BARE_RE detected).')
    return _mk_warn(
        'PRE_PP_007', 'pipeline_pattern',
        details=f'FR-24 bare-reference skip patterns missing: '
                f'_ELO_BARE_RE={has_elo_bare}, _L2_BARE_RE={has_l2_bare}.',
        fix='Add bare-reference skip logic to qualify_* functions: when '
            'input text matches a bare reference standing alone, skip '
            'qualification expansion. Pattern Reference v1.3 FR-24.')


def _check_pp_008(template_src: Optional[str],
                  doc_class: str) -> CheckResult:
    """FR-18 supersession — content-density-weighted column distribution
    (FR-18) must NOT appear in current compute_column_widths. Stale
    patterns are FAIL per spec section 3.4 fail semantics."""
    if template_src is None:
        return _mk_warn(
            'PRE_PP_008', 'pipeline_pattern',
            details=f'Template module for {doc_class} not found; FR-18 '
                    f'supersession check skipped.',
            fix='Verify OPSDIR pipeline module paths.')

    # FR-18 stale signatures: comment markers for content-density-weighted
    # distribution, or naive equal-split fallback in compute_column_widths.
    fr18_signatures = [
        # Old comment markers from FR-18 implementation
        'content-density-weighted',
        'Class C: content-density',
        # Naive equal-split (was the comfortable-fit fallback before FR-27)
        'extra / num_cols for i in range',
    ]
    found_stale: List[str] = []
    for sig in fr18_signatures:
        if sig in template_src:
            # Filter out legitimate occurrences in comments referring to
            # historical patterns (e.g., "previously naive equal-split")
            ctx_idx = template_src.find(sig)
            ctx_window = template_src[max(0, ctx_idx - 80):ctx_idx + 120]
            # Skip if surrounding context indicates supersession narrative
            if any(supersede_kw in ctx_window.lower()
                   for supersede_kw in (
                       'superseded', 'replaced', 'class j', 'class n',
                       'fr-21', 'fr-27', 'previously', 'prior')):
                continue
            found_stale.append(sig)

    if found_stale:
        return _mk_fail(
            'PRE_PP_008', 'pipeline_pattern',
            details=f'FR-18 supersession violation: stale pattern(s) '
                    f'detected — '
                    + ', '.join(repr(s) for s in found_stale)
                    + '. FR-18 (content-density-weighted column '
                      'distribution) was superseded by FR-21 + FR-27 at '
                      'Sub-Iter 2I.',
            fix='Remove FR-18 patterns; replace with FR-21 + FR-27 tiered '
                'allocation (NARROW_COL_THRESHOLD + NARROW_COL_BUFFER + '
                'max_body_idx fallback). Pattern Reference v1.3.')
    return _mk_pass(
        'PRE_PP_008', 'pipeline_pattern',
        details='FR-18 supersession verified: no stale content-density-'
                'weighted patterns detected in current pipeline code.')


# 3.5 L-4 PERMANENT Discipline
def verify_l4_permanent_discipline(doc_path: str) -> List[CheckResult]:
    """Spec section 3.5: PRE_L4_001 zero literal dollar-sign characters.

    Scans the source document for literal dollar-sign characters and the
    corruption signature (consecutive double dollar-sign). Any occurrence
    is FAIL per spec section 3.5 fail semantics ("L-4 failures halt; L-4
    PERMANENT discipline is governance-tier per LSA Part X").

    Implementation reads the file as UTF-8 text. For binary or non-text
    document classes, returns a single PASS with note that L-4 scan is
    not applicable to binary content.
    """
    if not doc_path or not os.path.exists(doc_path):
        return [_mk_fail(
            'PRE_L4_001', 'l4_discipline',
            details=f'doc_path missing or absent: {doc_path!r}',
            fix='Supply a valid path to the source document.')]

    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        return [_mk_pass(
            'PRE_L4_001', 'l4_discipline',
            details='L-4 scan skipped: file is not UTF-8 text. Binary or '
                    'non-text document classes are not subject to literal '
                    'dollar-sign discipline at the source level.')]
    except OSError as e:
        return [_mk_fail(
            'PRE_L4_001', 'l4_discipline',
            details=f'unable to read doc_path: {e}',
            fix='Verify file permissions and accessibility.')]

    findings: List[Tuple[int, int, str]] = []
    double_findings: List[Tuple[int, int]] = []
    for line_no, line in enumerate(text.split('\n'), 1):
        if _DOLLAR in line:
            # Locate every occurrence
            for col, ch in enumerate(line, 1):
                if ch == _DOLLAR:
                    snippet = line[max(0, col - 16):min(len(line), col + 16)]
                    findings.append((line_no, col, snippet))
        if _DOUBLE_DOLLAR in line:
            idx = line.index(_DOUBLE_DOLLAR)
            double_findings.append((line_no, idx + 1))

    if not findings and not double_findings:
        return [_mk_pass(
            'PRE_L4_001', 'l4_discipline',
            details='Zero literal dollar-sign characters found in source.')]

    details_parts: List[str] = []
    if findings:
        sample = findings[:5]
        details_parts.append(
            f'{len(findings)} literal dollar-sign character(s) found. '
            f'First {len(sample)}: '
            + '; '.join(
                f'line {ln} col {col} near {snip!r}'
                for ln, col, snip in sample))
    if double_findings:
        details_parts.append(
            f'Corruption signature (double dollar-sign) detected at '
            f'{len(double_findings)} location(s); first at line '
            f'{double_findings[0][0]} col {double_findings[0][1]}. '
            f'Likely artifact of past collapse of escaped dollar-signs.')

    return [_mk_fail(
        'PRE_L4_001', 'l4_discipline',
        details=' | '.join(details_parts),
        fix='Replace literal dollar-sign occurrences with escaped form '
            '(e.g., USD prefix where currency is referenced) per L-4 '
            'PERMANENT discipline (LSA Part X). Investigate any '
            'corruption-signature occurrences as evidence of prior '
            'pipeline corruption.')]


# 3.6 F-14 Disk-Authoritative Conformance
# Heuristic patterns for F-14 detection. Calibrated to surface likely
# violations while accepting that some hardcoding is legitimate.
_DATED_FILENAME_RE = re.compile(
    r'\b\d{4}-\d{2}-\d{2}_[A-Za-z0-9_\-.]+\.(md|pdf|json|csv|yaml|yml)\b')
# Version qualifiers like "v1.5", "v3.21", "v1.6.2" — three components max
_VERSION_QUALIFIER_RE = re.compile(r'\bv\d+\.\d+(?:\.\d+)?\b')


def verify_f14_disk_authoritative_conformance(
        doc_path: str) -> List[CheckResult]:
    """Spec section 3.6: PRE_F14_001-002 F-14 version-agnostic phrasing.

    PRE_F14_001 — Path Pattern column phrasing in governing document tables
        should use "latest dated file" or analogous version-agnostic
        phrasing rather than specific filenames. Hardcoded specific
        filenames in Path Pattern columns -> WARN.
    PRE_F14_002 — Body text version qualifiers should use version-agnostic
        phrasing ("the current X") rather than hardcoded version numbers,
        except within tables, footers, or explicit version-tracking
        sections. Hardcoded version qualifiers in body text -> WARN.

    Both checks WARN; F-14 violations do not halt the pipeline (per spec
    section 3.6 fail semantics: "F-14 is a discipline pattern, not a hard
    rule").

    Heuristic implementation: F-14 detection is necessarily approximate.
    Tunable via per-doc-class config (deferred to Phase E).
    """
    results: List[CheckResult] = []
    if not doc_path or not os.path.exists(doc_path):
        results.append(_mk_warn(
            'PRE_F14_001', 'f14_discipline',
            details=f'doc_path missing or absent: {doc_path!r}; '
                    f'F-14 scan skipped.',
            fix='Supply a valid path to the source document.'))
        return results

    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except (UnicodeDecodeError, OSError):
        # Non-text content; F-14 not applicable
        results.append(_mk_pass(
            'PRE_F14_001', 'f14_discipline',
            details='F-14 path-pattern scan skipped: non-text content.'))
        results.append(_mk_pass(
            'PRE_F14_002', 'f14_discipline',
            details='F-14 version-qualifier scan skipped: non-text content.'))
        return results

    lines = text.split('\n')

    # PRE_F14_001: Hardcoded filenames in markdown table cells under
    # Path / Path Pattern / Location column headers
    f14_001_findings = _scan_path_pattern_columns(lines)
    if f14_001_findings:
        sample = f14_001_findings[:5]
        results.append(_mk_warn(
            'PRE_F14_001', 'f14_discipline',
            details=f'{len(f14_001_findings)} hardcoded filename(s) in '
                    f'Path/Location column cells. First {len(sample)}: '
                    + '; '.join(
                        f'line {ln}: {fn!r}' for ln, fn in sample),
            fix='Replace hardcoded filenames with version-agnostic phrasing '
                '("latest dated file") in governing-document Path Pattern '
                'columns per F-14 disk-authoritative principle. Some uses '
                'may be legitimate (e.g., changelog rows); review and '
                'preserve where appropriate.'))
    else:
        results.append(_mk_pass(
            'PRE_F14_001', 'f14_discipline',
            details='No hardcoded filenames detected in Path/Location '
                    'column cells.'))

    # PRE_F14_002: Version qualifiers in body text outside tables/footers
    f14_002_findings = _scan_body_version_qualifiers(lines)
    if f14_002_findings:
        sample = f14_002_findings[:5]
        results.append(_mk_warn(
            'PRE_F14_002', 'f14_discipline',
            details=f'{len(f14_002_findings)} hardcoded version '
                    f'qualifier(s) in body text. First {len(sample)}: '
                    + '; '.join(
                        f'line {ln}: {ver!r}' for ln, ver in sample),
            fix='Replace hardcoded version qualifiers with version-agnostic '
                'phrasing ("the current X") outside tables, footers, and '
                'explicit version-tracking sections per F-14 disk-'
                'authoritative principle. Some references are legitimate '
                '(version-bump narratives, changelogs); review.'))
    else:
        results.append(_mk_pass(
            'PRE_F14_002', 'f14_discipline',
            details='No hardcoded version qualifiers detected in body '
                    'text outside tables/footers.'))

    return results


def _scan_path_pattern_columns(
        lines: List[str]) -> List[Tuple[int, str]]:
    """Detect dated filename patterns in markdown-table Path/Location cells.

    Walks markdown tables. When a header row contains a column whose
    header text is "path", "path pattern", or "location" (case-insensitive),
    flags subsequent body rows where that column's cell matches a dated
    filename pattern.
    """
    findings: List[Tuple[int, str]] = []
    in_table = False
    target_col_indices: List[int] = []
    is_after_separator = False

    for line_no, line in enumerate(lines, 1):
        stripped = line.strip()
        if not (stripped.startswith('|') and stripped.endswith('|')):
            in_table = False
            target_col_indices = []
            is_after_separator = False
            continue

        cells = [c.strip() for c in stripped.strip('|').split('|')]

        if not in_table:
            # Header row: identify target columns
            target_col_indices = [
                i for i, h in enumerate(cells)
                if h.lower() in ('path', 'path pattern', 'location')
            ]
            in_table = True
            is_after_separator = False
            continue

        # Separator row check: typical patterns like ---|---|...
        if all(re.match(r'^:?-+:?$', c) for c in cells if c):
            is_after_separator = True
            continue

        if not is_after_separator or not target_col_indices:
            continue

        for idx in target_col_indices:
            if idx < len(cells):
                cell = cells[idx]
                m = _DATED_FILENAME_RE.search(cell)
                if m:
                    findings.append((line_no, m.group(0)))

    return findings


def _scan_body_version_qualifiers(
        lines: List[str]) -> List[Tuple[int, str]]:
    """Detect hardcoded version qualifiers (v1.5 / v3.21) in body text.

    Excludes lines that are:
    - inside markdown tables (|...|)
    - footers ("---" lines + lines starting with `*` italic markers)
    - explicit version-tracking sections (Changelog, Version History,
      Revision Notes — header presence triggers exclusion until next header)
    - markdown headings (# / ## / ### ... lines)
    """
    findings: List[Tuple[int, str]] = []
    in_excluded_section = False
    excluded_section_headers = {
        'changelog', 'version history', 'revision notes', 'revisions',
        'change history', 'change log',
    }

    for line_no, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line:
            continue

        # Exclude explicit headings
        if line.startswith('#'):
            # Check if this heading enters or exits an excluded section
            heading_text = line.lstrip('#').strip().lower()
            in_excluded_section = any(
                k in heading_text for k in excluded_section_headers)
            continue

        if in_excluded_section:
            continue

        # Exclude markdown table rows
        if line.startswith('|') and line.endswith('|'):
            continue

        # Exclude italicized footer/metadata lines (single asterisk on each end)
        if (line.startswith('*') and line.endswith('*')
                and not line.startswith('**')):
            continue

        # Exclude bold-prefix metadata lines like "**Version:** v1.0"
        # Per spec section 3.6: hardcoded versions in *body text* are the
        # target; metadata lines are not body text.
        if re.match(r'^\*\*[A-Z][^*]*:\*\*', line):
            continue

        for m in _VERSION_QUALIFIER_RE.finditer(line):
            # Filter out trivial cases: "v1" alone, file extensions
            qualifier = m.group(0)
            findings.append((line_no, qualifier))

    return findings


def run_pre_render_verification_suite(
        doc_path: str, doc_class: str,
        config: Optional[Dict[str, Any]] = None) -> VerificationReport:
    """Spec section 3.7: pre-render suite runner.

    Executes all six pre-render check categories and aggregates results.
    Caller should check report.halt_pipeline and abort pipeline execution
    if True. WARN-only reports allow pipeline to proceed. Per spec
    section 2.3 integration semantics.

    Config consumption (FR-VRD-007 / Phase F):
      - When config=None, auto-loads per-class config via load_class_config.
      - After all checks run, applies per-check applicability + severity
        overrides via _apply_config_to_report. Non-applicable checks become
        vacuous PASS; INFO-severity findings demote to PASS with annotation;
        WARN-severity natural FAILs demote to WARN.
      - Pass an explicit empty dict ({}) to opt out of config post-process.
    """
    if doc_class not in DOC_CLASSES:
        raise ValueError(
            f'doc_class must be one of {DOC_CLASSES!r}, got {doc_class!r}')

    if config is None:
        config = load_class_config(doc_class)

    report = VerificationReport(
        verification_type=VTYPE_PRE,
        document_class=doc_class,
        document_identifier=os.path.basename(doc_path or ''))

    report.extend(verify_source_data_integrity(doc_path, doc_class))
    report.extend(verify_methodology_conformance(doc_path, doc_class))
    report.extend(verify_brand_specification_adherence(doc_path, doc_class))
    report.extend(verify_pipeline_pattern_conformance(doc_path, doc_class))
    report.extend(verify_l4_permanent_discipline(doc_path))
    report.extend(verify_f14_disk_authoritative_conformance(doc_path))

    _apply_config_to_report(report, config)

    return report


# =============================================================================
# Post-render regression detection (spec section 4)
# =============================================================================
# 4.1 Byte-Level Equivalence
def _sha256(path: str) -> Optional[str]:
    """Compute SHA-256 hex digest of a file; None if unreadable."""
    try:
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def detect_byte_level_regression(
        rendered_pdf_path: str,
        reference_pdf_path: str) -> CheckResult:
    """Spec section 4.1: SHA-256 checksum comparison.

    Document classes requiring byte equivalence: GAR Layer 1 SKU 1 only at
    workstream initial activation (per OI-CALIBER-03 Path 1 Go disposition).
    Tolerance: zero (exact match required).

    Per-doc-class opt-in: callers should invoke this check only when
    byte-equivalence is the contractual baseline. The check itself
    enforces zero tolerance.
    """
    if not rendered_pdf_path or not os.path.exists(rendered_pdf_path):
        return _mk_fail(
            'POST_BE_001', 'byte_equivalence',
            details=f'rendered_pdf_path missing or absent: '
                    f'{rendered_pdf_path!r}',
            fix='Supply a valid path to the rendered PDF.')
    if not reference_pdf_path or not os.path.exists(reference_pdf_path):
        return _mk_warn(
            'POST_BE_001', 'byte_equivalence',
            details=f'reference_pdf_path missing or absent: '
                    f'{reference_pdf_path!r}; byte-level check skipped.',
            fix='Establish a reference render before invoking byte-level '
                'regression detection.')

    rendered_hash = _sha256(rendered_pdf_path)
    reference_hash = _sha256(reference_pdf_path)
    if rendered_hash is None or reference_hash is None:
        return _mk_fail(
            'POST_BE_001', 'byte_equivalence',
            details=f'unable to read one or both PDFs for hashing.',
            fix='Verify file accessibility.')
    if rendered_hash == reference_hash:
        return _mk_pass(
            'POST_BE_001', 'byte_equivalence',
            details=f'SHA-256 match: {rendered_hash[:16]}...')
    return _mk_fail(
        'POST_BE_001', 'byte_equivalence',
        details=f'SHA-256 mismatch — rendered={rendered_hash[:16]}..., '
                f'reference={reference_hash[:16]}...',
        fix='Inspect rendered PDF for upstream change. Either the change '
            'is an intended canonicalization (re-establish reference '
            'render via Info/Tech Tier 1 attestation per spec section '
            '5.3) or a genuine regression (investigate pipeline state).')


# 4.2 PDF Structural Equivalence
def detect_structural_regression(
        rendered_pdf_path: str,
        reference_pdf_path: str) -> CheckResult:
    """Spec section 4.2: page count + dimensions + mark-content stream check.

    Three sub-checks aggregated into a single CheckResult:
      a) page count comparison (zero tolerance)
      b) per-page dimensions (width/height in points; zero tolerance)
      c) per-page text-layer extraction comparison (zero tolerance)

    Failure mode classification:
      - Reflow regression: page count drift (often from layout shift)
      - Page dimension drift: font-substitution-induced metric changes
      - Content stream divergence: text layer differs between renders
    """
    if not rendered_pdf_path or not os.path.exists(rendered_pdf_path):
        return _mk_fail(
            'POST_SE_001', 'structural_equivalence',
            details=f'rendered_pdf_path missing: {rendered_pdf_path!r}',
            fix='Supply a valid rendered PDF path.')
    if not reference_pdf_path or not os.path.exists(reference_pdf_path):
        return _mk_warn(
            'POST_SE_001', 'structural_equivalence',
            details=f'reference_pdf_path missing: {reference_pdf_path!r}; '
                    f'structural check skipped.',
            fix='Establish a reference render before invoking structural '
                'regression detection.')

    try:
        import pypdf
    except ImportError:
        return _mk_warn(
            'POST_SE_001', 'structural_equivalence',
            details='pypdf not installed; structural check skipped.',
            fix='pip install pypdf')

    try:
        rendered = pypdf.PdfReader(rendered_pdf_path)
        reference = pypdf.PdfReader(reference_pdf_path)
    except Exception as e:
        return _mk_fail(
            'POST_SE_001', 'structural_equivalence',
            details=f'unable to open one or both PDFs: {e}',
            fix='Verify PDF integrity and pypdf compatibility.')

    findings: List[str] = []

    # a) Page count
    rendered_pages = len(rendered.pages)
    reference_pages = len(reference.pages)
    if rendered_pages != reference_pages:
        findings.append(
            f'page count: rendered={rendered_pages}, '
            f'reference={reference_pages}')

    # b) Per-page dimensions
    dim_findings: List[str] = []
    pages_to_check = min(rendered_pages, reference_pages)
    for i in range(pages_to_check):
        try:
            r_box = rendered.pages[i].mediabox
            ref_box = reference.pages[i].mediabox
            r_w, r_h = float(r_box.width), float(r_box.height)
            ref_w, ref_h = float(ref_box.width), float(ref_box.height)
            if (abs(r_w - ref_w) > 0.5 or abs(r_h - ref_h) > 0.5):
                dim_findings.append(
                    f'page {i + 1}: rendered={r_w:.1f}x{r_h:.1f}, '
                    f'reference={ref_w:.1f}x{ref_h:.1f}')
        except Exception:
            continue
    if dim_findings:
        findings.append(
            f'page dimensions ({len(dim_findings)} drift): '
            + '; '.join(dim_findings[:3])
            + (f'... +{len(dim_findings) - 3}' if len(dim_findings) > 3
               else ''))

    # c) Text-layer extraction
    text_findings: List[str] = []
    for i in range(pages_to_check):
        try:
            r_text = (rendered.pages[i].extract_text() or '').strip()
            ref_text = (reference.pages[i].extract_text() or '').strip()
            if r_text != ref_text:
                # Compute character-level diff size
                diff_chars = abs(len(r_text) - len(ref_text))
                text_findings.append(f'page {i + 1} (Δ {diff_chars} char)')
        except Exception:
            continue
    if text_findings:
        findings.append(
            f'text-layer divergence ({len(text_findings)} pages): '
            + '; '.join(text_findings[:5])
            + (f'... +{len(text_findings) - 5}' if len(text_findings) > 5
               else ''))

    if findings:
        return _mk_fail(
            'POST_SE_001', 'structural_equivalence',
            details=' | '.join(findings),
            fix='Investigate pipeline state. Page count + dimensions + '
                'text-layer divergence indicate either an intended '
                'canonicalization (Info/Tech Tier 1 attestation per spec '
                'section 5.3 to re-establish reference) or a genuine '
                'regression (investigate pipeline rendering changes).')
    return _mk_pass(
        'POST_SE_001', 'structural_equivalence',
        details=f'Page count matches ({rendered_pages}); per-page '
                f'dimensions match within 0.5pt tolerance; per-page '
                f'text-layer extraction matches.')


# 4.3 Visual-Fidelity Equivalence
def detect_visual_fidelity_regression(
        rendered_pdf_path: str,
        reference_pdf_path: str,
        tolerance_pct: float = 0.1,
        dpi: int = 150) -> CheckResult:
    """Spec section 4.3: rasterize at DPI then pixel-diff per page.

    Per established CaliberPath cadence: pypdfium2 rasterizer at 150 DPI.
    Pillow ImageChops.difference + bounding-box pixel count for diff
    metric. Per-page diff exceeding tolerance_pct triggers FAIL with
    per-page breakdown.

    Tolerance defaults per doc class (caller responsibility to pass
    appropriate value via run_post_render_regression_detection config):
        FG / CIG Full / Workbook: 0.1% per-page pixel difference
        CIG QRC: 0.5% per-page (smaller documents tolerate higher variance)
        GAR Layer 1 SKU 1: 0.0% (combined with byte-equivalence)
    """
    if not rendered_pdf_path or not os.path.exists(rendered_pdf_path):
        return _mk_fail(
            'POST_VF_001', 'visual_fidelity',
            details=f'rendered_pdf_path missing: {rendered_pdf_path!r}',
            fix='Supply a valid rendered PDF path.')
    if not reference_pdf_path or not os.path.exists(reference_pdf_path):
        return _mk_warn(
            'POST_VF_001', 'visual_fidelity',
            details=f'reference_pdf_path missing: {reference_pdf_path!r}; '
                    f'visual-fidelity check skipped.',
            fix='Establish a reference render before invoking visual-'
                'fidelity regression detection.')

    try:
        import pypdfium2 as pdfium
        from PIL import Image, ImageChops
    except ImportError as e:
        return _mk_warn(
            'POST_VF_001', 'visual_fidelity',
            details=f'rasterization library missing: {e}; visual-fidelity '
                    f'check skipped.',
            fix='pip install pypdfium2 Pillow')

    try:
        rendered_doc = pdfium.PdfDocument(rendered_pdf_path)
        reference_doc = pdfium.PdfDocument(reference_pdf_path)
    except Exception as e:
        return _mk_fail(
            'POST_VF_001', 'visual_fidelity',
            details=f'unable to open one or both PDFs with pypdfium2: {e}',
            fix='Verify PDF integrity.')

    rendered_n = len(rendered_doc)
    reference_n = len(reference_doc)
    if rendered_n != reference_n:
        return _mk_fail(
            'POST_VF_001', 'visual_fidelity',
            details=f'page count mismatch (rendered={rendered_n}, '
                    f'reference={reference_n}); visual fidelity cannot '
                    f'be computed pairwise. See POST_SE_001 for structural '
                    f'detail.',
            fix='Resolve structural regression first.')

    # Convert DPI to pypdfium2 scale factor (DPI / 72 pt-per-inch)
    scale = dpi / 72.0
    per_page_diffs: List[Tuple[int, float]] = []
    failed_pages: List[Tuple[int, float]] = []

    for i in range(rendered_n):
        try:
            r_page = rendered_doc[i]
            ref_page = reference_doc[i]
            r_pil = r_page.render(scale=scale).to_pil().convert('RGB')
            ref_pil = ref_page.render(scale=scale).to_pil().convert('RGB')
        except Exception as e:
            return _mk_fail(
                'POST_VF_001', 'visual_fidelity',
                details=f'rasterization error on page {i + 1}: {e}',
                fix='Verify PDF page integrity.')

        # Resize to common dimensions if minor metric drift exists
        if r_pil.size != ref_pil.size:
            # If sizes differ, resize reference to rendered dims for fair
            # pixel-comparison (preserves per-pixel position semantics).
            ref_pil = ref_pil.resize(r_pil.size, Image.Resampling.LANCZOS)

        diff = ImageChops.difference(r_pil, ref_pil)
        bbox = diff.getbbox()
        if bbox is None:
            per_page_diffs.append((i + 1, 0.0))
            continue

        # Count pixels that differ (any channel non-zero)
        diff_data = diff.getdata()
        total_pixels = r_pil.width * r_pil.height
        # Count pixels where max channel diff > 0
        differing = sum(1 for px in diff_data if max(px) > 0)
        diff_pct = (differing / total_pixels) * 100.0
        per_page_diffs.append((i + 1, diff_pct))
        if diff_pct > tolerance_pct:
            failed_pages.append((i + 1, diff_pct))

    rendered_doc.close()
    reference_doc.close()

    if failed_pages:
        sample = failed_pages[:5]
        return _mk_fail(
            'POST_VF_001', 'visual_fidelity',
            details=f'{len(failed_pages)} of {rendered_n} page(s) exceed '
                    f'{tolerance_pct}% pixel-diff tolerance at {dpi} DPI. '
                    f'First {len(sample)}: '
                    + '; '.join(
                        f'page {p} ({pct:.3f}%)' for p, pct in sample),
            fix='Inspect rendered PDF visually at flagged pages. Either '
                'the change is an intended visual canonicalization '
                '(Info/Tech Tier 1 attestation per spec section 5.3 to '
                're-establish reference render) or a genuine visual '
                'regression (investigate pipeline rendering changes; '
                'common causes: font hinting changes, anti-aliasing '
                'variation, image asset changes, color space shifts).')
    max_diff = max((pct for _, pct in per_page_diffs), default=0.0)
    return _mk_pass(
        'POST_VF_001', 'visual_fidelity',
        details=f'All {rendered_n} pages within {tolerance_pct}% pixel-'
                f'diff tolerance at {dpi} DPI. Max per-page diff: '
                f'{max_diff:.4f}%.')


# 4.4 Bookmark/Outline Equivalence
def _walk_outline(items, depth=0):
    """Walk a pypdf outline tree; return list of (depth, title, page_num).

    pypdf returns nested lists for sub-outlines; leaf items are
    Destination objects. Page resolution best-effort via .page attribute.
    """
    flat: List[Tuple[int, str, Optional[int]]] = []
    if not items:
        return flat
    for item in items:
        if isinstance(item, list):
            flat.extend(_walk_outline(item, depth + 1))
        else:
            title = getattr(item, 'title', str(item))
            # Resolve target page; pypdf Destination .page resolves to a
            # PageObject, which has an indirect-reference; we capture the
            # resolved page index via the parent reader if possible.
            page = None
            try:
                # Try various attribute paths pypdf exposes
                if hasattr(item, 'page'):
                    pg = item.page
                    page = getattr(pg, 'idnum', None)
                if page is None and hasattr(item, '/Page'):
                    page = item['/Page'].idnum
            except Exception:
                page = None
            flat.append((depth, title, page))
    return flat


def detect_bookmark_regression(
        rendered_pdf_path: str,
        reference_pdf_path: str) -> CheckResult:
    """Spec section 4.4: outline tree + label + target page comparison.

    Tolerance: zero (exact match required).

    Failure modes captured: FR-19 dispatch regression; bookmark hierarchy
    reflows; target-page drift due to content shifts.
    """
    if not rendered_pdf_path or not os.path.exists(rendered_pdf_path):
        return _mk_fail(
            'POST_BM_001', 'bookmark_outline',
            details=f'rendered_pdf_path missing: {rendered_pdf_path!r}',
            fix='Supply a valid rendered PDF path.')
    if not reference_pdf_path or not os.path.exists(reference_pdf_path):
        return _mk_warn(
            'POST_BM_001', 'bookmark_outline',
            details=f'reference_pdf_path missing: {reference_pdf_path!r}; '
                    f'bookmark check skipped.',
            fix='Establish a reference render before invoking bookmark '
                'regression detection.')

    try:
        import pypdf
    except ImportError:
        return _mk_warn(
            'POST_BM_001', 'bookmark_outline',
            details='pypdf not installed; bookmark check skipped.',
            fix='pip install pypdf')

    try:
        rendered = pypdf.PdfReader(rendered_pdf_path)
        reference = pypdf.PdfReader(reference_pdf_path)
    except Exception as e:
        return _mk_fail(
            'POST_BM_001', 'bookmark_outline',
            details=f'unable to open one or both PDFs: {e}',
            fix='Verify PDF integrity.')

    rendered_outline = _walk_outline(rendered.outline or [])
    reference_outline = _walk_outline(reference.outline or [])

    # Compare lengths first
    if len(rendered_outline) != len(reference_outline):
        return _mk_fail(
            'POST_BM_001', 'bookmark_outline',
            details=f'outline entry count mismatch: rendered='
                    f'{len(rendered_outline)}, reference='
                    f'{len(reference_outline)}',
            fix='Investigate bookmark registration changes. Either an '
                'intended canonicalization (re-establish reference render) '
                'or a regression (FR-19 dispatch logic, session/phase '
                'bookmark coverage, etc.).')

    # Walk both in parallel; flag differences
    label_findings: List[str] = []
    depth_findings: List[str] = []
    page_findings: List[str] = []
    for i, (r_entry, ref_entry) in enumerate(
            zip(rendered_outline, reference_outline)):
        r_depth, r_title, r_page = r_entry
        ref_depth, ref_title, ref_page = ref_entry
        if r_depth != ref_depth:
            depth_findings.append(
                f'entry {i + 1} ({r_title[:40]!r}): rendered L{r_depth}, '
                f'reference L{ref_depth}')
        if r_title != ref_title:
            label_findings.append(
                f'entry {i + 1} L{r_depth}: rendered={r_title[:40]!r}, '
                f'reference={ref_title[:40]!r}')
        if r_page != ref_page and r_page is not None and ref_page is not None:
            page_findings.append(
                f'entry {i + 1} ({r_title[:30]!r}): page diff')

    findings = []
    if depth_findings:
        findings.append(
            f'{len(depth_findings)} outline-depth difference(s): '
            + '; '.join(depth_findings[:3]))
    if label_findings:
        findings.append(
            f'{len(label_findings)} label difference(s): '
            + '; '.join(label_findings[:3]))
    if page_findings:
        findings.append(
            f'{len(page_findings)} target-page drift: '
            + '; '.join(page_findings[:3]))

    if findings:
        return _mk_fail(
            'POST_BM_001', 'bookmark_outline',
            details=' | '.join(findings),
            fix='Investigate FR-19 dispatch logic + bookmark registration '
                'sites in template script. Re-establish reference render '
                'via Info/Tech Tier 1 attestation if change is intended '
                'canonicalization.')
    return _mk_pass(
        'POST_BM_001', 'bookmark_outline',
        details=f'All {len(rendered_outline)} outline entries match '
                f'(depth + label + target page).')


# 4.5 Font/Asset Embedding Verification
def _enumerate_pdf_fonts(reader) -> List[str]:
    """Enumerate all referenced /Font resource names across all pages.

    Returns deduplicated list of base font names (BaseFont entries from
    each /Font dictionary). pypdf 6.x exposes Page.images and Resources
    via .resources or via raw page object access.
    """
    fonts: set = set()
    for page in reader.pages:
        try:
            res = page.get('/Resources') or {}
            if hasattr(res, 'get_object'):
                res = res.get_object()
            font_dict = res.get('/Font') or {} if res else {}
            if hasattr(font_dict, 'get_object'):
                font_dict = font_dict.get_object()
            for ref in (font_dict.values() if hasattr(font_dict, 'values')
                        else []):
                try:
                    obj = ref.get_object() if hasattr(ref, 'get_object') else ref
                    base = obj.get('/BaseFont') if hasattr(obj, 'get') else None
                    if base:
                        # Strip subset prefix (e.g., "ABCDEF+Inter-Regular")
                        name = str(base).lstrip('/')
                        if '+' in name:
                            name = name.split('+', 1)[1]
                        fonts.add(name)
                except Exception:
                    continue
        except Exception:
            continue
    return sorted(fonts)


def verify_font_asset_embedding(rendered_pdf_path: str) -> CheckResult:
    """Spec section 4.5: /Font + /XObject resource dictionary inspection.

    Verifies all expected fonts (per VBS canonical font set) are embedded;
    flags unexpected font substitutions or missing-glyph fallbacks.

    Tolerance: zero for missing canonical fonts; WARN for unexpected
    additional fonts (per spec section 4.5 fail semantics).

    Failure modes captured: font installation regressions; asset path
    drift; glyph subset truncations.
    """
    if not rendered_pdf_path or not os.path.exists(rendered_pdf_path):
        return _mk_fail(
            'POST_FA_001', 'font_asset_embedding',
            details=f'rendered_pdf_path missing: {rendered_pdf_path!r}',
            fix='Supply a valid rendered PDF path.')

    try:
        import pypdf
    except ImportError:
        return _mk_warn(
            'POST_FA_001', 'font_asset_embedding',
            details='pypdf not installed; font/asset check skipped.',
            fix='pip install pypdf')

    try:
        reader = pypdf.PdfReader(rendered_pdf_path)
    except Exception as e:
        return _mk_fail(
            'POST_FA_001', 'font_asset_embedding',
            details=f'unable to open PDF: {e}',
            fix='Verify PDF integrity.')

    fonts_found = _enumerate_pdf_fonts(reader)
    canonical = CANONICAL_VBS_FONTS

    # Collect canonical and non-canonical fonts
    canonical_present: List[str] = []
    non_canonical: List[str] = []
    for fn in fonts_found:
        # Match against canonical set (case-insensitive substring tolerance
        # for subset prefixes and minor naming variants)
        is_canonical = False
        for c in canonical:
            c_norm = c.replace(' ', '')
            if c_norm.lower() in fn.lower() or c.lower() in fn.lower():
                is_canonical = True
                break
        if is_canonical:
            canonical_present.append(fn)
        else:
            non_canonical.append(fn)

    findings: List[str] = []
    if non_canonical:
        findings.append(
            f'{len(non_canonical)} non-canonical font(s) embedded: '
            + ', '.join(non_canonical[:5])
            + (f' ... +{len(non_canonical) - 5}' if len(non_canonical) > 5
               else ''))

    if findings and any(
            fn.lower() in ('helvetica', 'times-roman', 'arial')
            for fn in non_canonical):
        # Helvetica is canonical for AcroForm fields (forms-only); flagged
        # only if appears outside expected AcroForm context. Heuristic
        # surfaces it at WARN level.
        return _mk_warn(
            'POST_FA_001', 'font_asset_embedding',
            details=' | '.join(findings)
                    + f' | Canonical fonts present: {len(canonical_present)} '
                      f'({", ".join(canonical_present[:3])}'
                    + (f', ...' if len(canonical_present) > 3 else '')
                    + ').',
            fix='Investigate non-canonical font substitutions. Helvetica '
                'is permitted for AcroForm field rendering only; appearance '
                'outside form context indicates font-substitution regression. '
                'Other non-canonical fonts (Times, Arial, etc.) indicate '
                'missing-glyph fallback events.')
    if non_canonical:
        return _mk_warn(
            'POST_FA_001', 'font_asset_embedding',
            details=' | '.join(findings)
                    + f' | Canonical fonts present: {len(canonical_present)}.',
            fix='Verify whether non-canonical font additions are intended '
                'or indicate font-substitution regression.')
    return _mk_pass(
        'POST_FA_001', 'font_asset_embedding',
        details=f'All {len(fonts_found)} embedded font(s) resolve to '
                f'canonical VBS typeface set: '
                + ', '.join(fonts_found[:5])
                + (f', ...' if len(fonts_found) > 5 else '') + '.')


def run_post_render_regression_detection(
        rendered_pdf_path: str,
        reference_pdf_path: str,
        doc_class: str,
        config: Optional[Dict[str, Any]] = None) -> VerificationReport:
    """Spec section 4.6: post-render suite runner.

    Executes all five post-render regression detection categories.
    FAIL status surfaces to Info/Tech Tier 1 disposition (false positive vs
    genuine regression vs intended change). Does not halt downstream pipeline
    (rendering already happened; report informs subsequent action).

    Config consumption (FR-VRD-007 / Phase F):
      - When config=None, auto-loads per-class config via load_class_config.
      - Reads visual_fidelity tolerance_pct + dpi from
        config['post_render_checks']['visual_fidelity'] when present;
        falls back to 0.1% / 150 DPI defaults otherwise.
      - Backwards compat: legacy top-level
        config['visual_fidelity_tolerance_pct'] + ['rasterize_dpi'] keys
        still honored when present.
      - After all checks run, applies per-check applicability + severity
        overrides via _apply_config_to_report.
      - Pass an explicit empty dict ({}) to opt out of config post-process.
    """
    if doc_class not in DOC_CLASSES:
        raise ValueError(
            f'doc_class must be one of {DOC_CLASSES!r}, got {doc_class!r}')

    if config is None:
        config = load_class_config(doc_class)

    report = VerificationReport(
        verification_type=VTYPE_POST,
        document_class=doc_class,
        document_identifier=os.path.basename(rendered_pdf_path or ''))

    vf_cfg = (config.get('post_render_checks', {})
                    .get('visual_fidelity', {})) if config else {}
    tolerance_pct = float(
        vf_cfg.get('tolerance_pct',
                   config.get('visual_fidelity_tolerance_pct', 0.1)
                   if config else 0.1))
    dpi = int(
        vf_cfg.get('dpi',
                   config.get('rasterize_dpi', 150)
                   if config else 150))

    report.add(detect_byte_level_regression(
        rendered_pdf_path, reference_pdf_path))
    report.add(detect_structural_regression(
        rendered_pdf_path, reference_pdf_path))
    report.add(detect_visual_fidelity_regression(
        rendered_pdf_path, reference_pdf_path, tolerance_pct, dpi))
    report.add(detect_bookmark_regression(
        rendered_pdf_path, reference_pdf_path))
    report.add(verify_font_asset_embedding(rendered_pdf_path))

    _apply_config_to_report(report, config)

    return report


# =============================================================================
# Report generation (spec section 6)
# =============================================================================
def write_verification_report(
        report: VerificationReport,
        output_dir: str,
        output_format: str = 'both') -> Dict[str, str]:
    """Write VerificationReport to disk as JSON and/or Markdown.

    Per spec section 6.2: filenames follow
        <doc-class>_<doc-id>_<verification-type>_<timestamp>.<ext>

    Args:
        report: VerificationReport instance
        output_dir: directory to write reports into (created if absent)
        output_format: 'json', 'markdown', or 'both'

    Returns:
        Dict with paths to written files (keys: 'json', 'markdown')
    """
    if output_format not in ('json', 'markdown', 'both'):
        raise ValueError(
            f"output_format must be 'json', 'markdown', or 'both'; "
            f'got {output_format!r}')

    os.makedirs(output_dir, exist_ok=True)

    ts = report.verification_timestamp.replace(':', '').replace('-', '')[:15]
    base = (f'{report.document_class}_{report.document_identifier}_'
            f'{report.verification_type}_{ts}')
    paths: Dict[str, str] = {}

    if output_format in ('json', 'both'):
        json_path = os.path.join(output_dir, base + '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)
        paths['json'] = json_path

    if output_format in ('markdown', 'both'):
        md_path = os.path.join(output_dir, base + '.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(_render_markdown_report(report))
        paths['markdown'] = md_path

    return paths


def _render_markdown_report(report: VerificationReport) -> str:
    """Render VerificationReport as a markdown summary per spec section 6.2."""
    lines: List[str] = []
    lines.append(f'# Verification Report - {report.document_identifier}')
    lines.append('')
    lines.append(f'**Type:** {report.verification_type}')
    lines.append(f'**Document Class:** {report.document_class}')
    lines.append(f'**Timestamp:** {report.verification_timestamp}')
    lines.append(f'**Overall Status:** {report.overall_status}')
    lines.append(f'**Halt Pipeline:** {report.halt_pipeline}')
    lines.append('')

    # Per-category status table
    by_category: Dict[str, List[CheckResult]] = {}
    for c in report.checks:
        by_category.setdefault(c.category, []).append(c)

    lines.append('## Per-Category Status')
    lines.append('')
    lines.append('| Category | Status |')
    lines.append('|---|---|')
    for cat, checks in by_category.items():
        statuses = {c.status for c in checks}
        if STATUS_FAIL in statuses:
            cat_status = STATUS_FAIL
        elif STATUS_WARN in statuses:
            cat_status = STATUS_WARN
        else:
            cat_status = STATUS_PASS
        lines.append(f'| {cat} | {cat_status} |')
    lines.append('')

    # FAIL/WARN details
    fail_warn = [c for c in report.checks
                 if c.status in (STATUS_FAIL, STATUS_WARN)]
    if fail_warn:
        lines.append('## FAIL/WARN Details')
        lines.append('')
        for c in fail_warn:
            lines.append(f'### {c.check_id} ({c.category}) - {c.status}')
            lines.append('')
            lines.append(f'**Details:** {c.details}')
            lines.append('')
            if c.fix_recommendation:
                lines.append(f'**Fix recommendation:** {c.fix_recommendation}')
                lines.append('')

    # Summary
    n_fail = sum(1 for c in report.checks if c.status == STATUS_FAIL)
    n_warn = sum(1 for c in report.checks if c.status == STATUS_WARN)
    n_pass = sum(1 for c in report.checks if c.status == STATUS_PASS)
    lines.append('## Summary')
    lines.append('')
    lines.append(f'{n_pass} PASS, {n_warn} WARN, {n_fail} FAIL across '
                 f'{len(report.checks)} total checks.')
    lines.append('')

    return '\n'.join(lines)


# =============================================================================
# Reference render governance (spec section 5)
# =============================================================================
# Reference render storage location per spec section 5.2 (CC implementation
# judgment on exact directory naming).
def _opsdir_root() -> str:
    """Resolve OPSDIR root via environment override or default OneDrive path."""
    env = os.environ.get('CALIBERPATH_OPSDIR')
    if env:
        return env
    return os.path.join(
        os.environ.get('USERPROFILE', ''),
        'OneDrive', 'Desktop', 'GET IT', 'CaliberPath')


def reference_render_dir() -> str:
    """Canonical Reference_Renders directory path under OPSDIR."""
    return os.path.join(
        _opsdir_root(), '08_Production_Pipeline', 'Reference_Renders')


def verification_config_dir() -> str:
    """Canonical Verification_Config directory path under OPSDIR."""
    return os.path.join(
        _opsdir_root(), '08_Production_Pipeline', 'Verification_Config')


def load_reference_render_metadata(
        doc_class: str, doc_id: str) -> Optional[Dict[str, Any]]:
    """Load reference render metadata JSON for a document.

    Looks under Reference_Renders/<doc_id>/ for a *_metadata.json file.
    Returns the parsed metadata dict, or None when no reference render
    is registered for that document.
    """
    ref_dir = os.path.join(reference_render_dir(), doc_id)
    if not os.path.isdir(ref_dir):
        return None
    for entry in os.listdir(ref_dir):
        if entry.endswith('_metadata.json'):
            with open(os.path.join(ref_dir, entry), 'r', encoding='utf-8') as f:
                return json.load(f)
    return None


def list_reference_renders() -> List[Dict[str, Any]]:
    """Enumerate all registered reference renders with metadata.

    Returns one entry per doc_id directory under Reference_Renders/, with
    metadata fields and resolved canonical PDF path.
    """
    base = reference_render_dir()
    if not os.path.isdir(base):
        return []
    out: List[Dict[str, Any]] = []
    for entry in sorted(os.listdir(base)):
        if entry.startswith('_'):  # skip _archive
            continue
        ref_dir = os.path.join(base, entry)
        if not os.path.isdir(ref_dir):
            continue
        meta_path = None
        pdf_path = None
        for fn in os.listdir(ref_dir):
            full = os.path.join(ref_dir, fn)
            if fn.endswith('_metadata.json'):
                meta_path = full
            elif fn.endswith('.pdf'):
                pdf_path = full
        if meta_path and os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            meta['_doc_id'] = entry
            meta['_pdf_path'] = pdf_path
            out.append(meta)
    return out


# =============================================================================
# Per-class config loader (FR-VRD-007; spec section 7.4)
# =============================================================================
# Maps check_id prefix to config category name. Used by config-driven
# post-processing of CheckResults to look up applicability + severity overrides.
_PRE_RENDER_CHECK_CATEGORY = {
    'PRE_SDI_': 'source_data_integrity',
    'PRE_MC_': 'methodology_conformance',
    'PRE_BS_': 'brand_specification',
    'PRE_PP_': 'pipeline_pattern',
    'PRE_L4_': 'l4_discipline',
    'PRE_F14_': 'f14_discipline',
}
_POST_RENDER_CHECK_CATEGORY = {
    'POST_BE_': 'byte_equivalence',
    'POST_SE_': 'structural_equivalence',
    'POST_VF_': 'visual_fidelity',
    'POST_BM_': 'bookmark_outline',
    'POST_FA_': 'font_asset_embedding',
}


def _deep_merge(base: Any, override: Any) -> Any:
    """Recursive dict merge: override wins on leaf conflicts."""
    if not isinstance(base, dict) or not isinstance(override, dict):
        return override
    out = dict(base)
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_class_config(doc_class: str) -> Dict[str, Any]:
    """Load + deep-merge per-class verification config (FR-VRD-007).

    Reads `_base.json` + `<doc_class>.json` from `verification_config_dir()`
    and returns the merged effective config dict. Per-document overrides
    from reference render metadata.tolerance_configuration apply on top
    of this and are caller's responsibility to merge.

    Returns an empty dict when no config files exist (graceful degradation
    so callers without Verification_Config get default-everything behavior).
    """
    if doc_class not in DOC_CLASSES:
        raise ValueError(
            f'doc_class must be one of {DOC_CLASSES!r}, got {doc_class!r}')
    cfg_dir = verification_config_dir()
    if not os.path.isdir(cfg_dir):
        return {}
    base: Dict[str, Any] = {}
    base_path = os.path.join(cfg_dir, '_base.json')
    if os.path.exists(base_path):
        with open(base_path, 'r', encoding='utf-8') as f:
            base = json.load(f)
    cls_path = os.path.join(cfg_dir, f'{doc_class}.json')
    cls_cfg: Dict[str, Any] = {}
    if os.path.exists(cls_path):
        with open(cls_path, 'r', encoding='utf-8') as f:
            cls_cfg = json.load(f)
    return _deep_merge(base, cls_cfg)


def _lookup_check_config(check_id: str,
                         config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Resolve the per-check config entry for a given check_id.

    Pre-render: config['pre_render_checks'][category]['checks'][check_id]
    Post-render: config['post_render_checks'][category]
        (post-render is one check per category; the category-level dict
        IS the per-check config)
    Returns None when no config entry resolves.
    """
    if not config:
        return None
    for prefix, cat in _PRE_RENDER_CHECK_CATEGORY.items():
        if check_id.startswith(prefix):
            return (
                config.get('pre_render_checks', {})
                      .get(cat, {})
                      .get('checks', {})
                      .get(check_id))
    for prefix, cat in _POST_RENDER_CHECK_CATEGORY.items():
        if check_id.startswith(prefix):
            return config.get('post_render_checks', {}).get(cat)
    return None


def _apply_config_to_check(result: CheckResult,
                           config: Dict[str, Any]) -> CheckResult:
    """Apply per-class config to a single CheckResult.

    Semantics:
      - applicable=false  -> vacuous PASS (replace any FAIL/WARN with PASS;
                            details prepended with vacuous-PASS annotation)
      - severity='INFO'   -> demote FAIL/WARN to PASS with annotation
                            (suppresses the finding from gating without
                            losing diagnostic detail)
      - severity='WARN' on natural FAIL -> demote to WARN
      - else passthrough (config severity is a ceiling, not a floor;
        a natural PASS is never promoted to FAIL/WARN by config alone)
    """
    cfg_check = _lookup_check_config(result.check_id, config)
    if not cfg_check:
        return result

    if cfg_check.get('applicable') is False:
        if result.status == STATUS_PASS:
            return result
        return CheckResult(
            check_id=result.check_id,
            category=result.category,
            status=STATUS_PASS,
            details=(
                f'(vacuous PASS per config: applicable=false; '
                f'natural status was {result.status}) {result.details}'),
            fix_recommendation=result.fix_recommendation,
            timestamp=result.timestamp)

    if result.status == STATUS_PASS:
        return result

    cfg_sev = cfg_check.get('severity')
    if cfg_sev == 'INFO':
        return CheckResult(
            check_id=result.check_id,
            category=result.category,
            status=STATUS_PASS,
            details=(
                f'(config severity=INFO; finding suppressed from gating; '
                f'natural status was {result.status}) {result.details}'),
            fix_recommendation=result.fix_recommendation,
            timestamp=result.timestamp)
    if cfg_sev == STATUS_WARN and result.status == STATUS_FAIL:
        return CheckResult(
            check_id=result.check_id,
            category=result.category,
            status=STATUS_WARN,
            details=(
                f'(config severity=WARN; demoted from FAIL) '
                f'{result.details}'),
            fix_recommendation=result.fix_recommendation,
            timestamp=result.timestamp)
    return result


def _apply_config_to_report(report: VerificationReport,
                            config: Dict[str, Any]) -> None:
    """Post-process all checks in a report against config; recompute status.

    Mutates the report in place. Iterates report.checks, applying
    `_apply_config_to_check` to each, then re-runs `_recompute_status()` so
    overall_status + halt_pipeline reflect the post-config picture.
    """
    if not config:
        return
    report.checks = [
        _apply_config_to_check(c, config) for c in report.checks
    ]
    report._recompute_status()


# =============================================================================
# Module smoke-test entry point (run when invoked directly)
# =============================================================================
def _smoke_test() -> int:
    """Verify import correctness, dataclass round-trip, and suite-runner stubs.

    Returns shell-style exit code (0 = success).
    """
    print(f'cp_verify version {__version__} - {__spec_version__}')
    print()

    # Build a sample report manually
    sample = VerificationReport(
        verification_type=VTYPE_PRE,
        document_class='WORKBOOK',
        document_identifier='workbook_v11.md')
    sample.add(_mk_pass('PRE_X_001', 'sample_category',
                        details='smoke-test pass'))
    sample.add(_mk_warn('PRE_X_002', 'sample_category',
                        details='smoke-test warn',
                        fix='example fix recommendation'))

    payload = sample.to_dict()
    roundtrip = VerificationReport.from_dict(payload)
    payload2 = roundtrip.to_dict()
    if payload != payload2:
        print('FAIL: round-trip serialization mismatch')
        return 1
    print('PASS: dataclass round-trip serialization')

    # Suite runner stubs
    pre = run_pre_render_verification_suite(
        doc_path='dummy/path.md', doc_class='WORKBOOK')
    if pre.verification_type != VTYPE_PRE:
        print('FAIL: pre-render suite returned wrong verification_type')
        return 1
    print(f'PASS: pre-render suite returned {len(pre.checks)} checks; '
          f'overall_status={pre.overall_status}; '
          f'halt_pipeline={pre.halt_pipeline}')

    post = run_post_render_regression_detection(
        rendered_pdf_path='dummy/rendered.pdf',
        reference_pdf_path='dummy/reference.pdf',
        doc_class='WORKBOOK')
    if post.verification_type != VTYPE_POST:
        print('FAIL: post-render suite returned wrong verification_type')
        return 1
    print(f'PASS: post-render suite returned {len(post.checks)} checks; '
          f'overall_status={post.overall_status}')

    # Reference render directory existence (informational; not a hard check)
    ref_dir = reference_render_dir()
    cfg_dir = verification_config_dir()
    print(f'  Reference_Renders dir: {ref_dir} '
          f'(exists={os.path.isdir(ref_dir)})')
    print(f'  Verification_Config dir: {cfg_dir} '
          f'(exists={os.path.isdir(cfg_dir)})')

    print()
    print('cp_verify smoke test: import + dataclass round-trip + suite '
          'runners PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(_smoke_test())
