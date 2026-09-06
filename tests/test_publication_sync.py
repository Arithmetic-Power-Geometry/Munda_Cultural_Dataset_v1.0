import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_publication_metrics_match_canonical_repository_state():
    pub = load("publication/generated/release_metrics.json")
    mmsc = load("data/source_census/mmsc_index.json")
    audit = load("data/source_bundles/encyclopaedia_mundarica/completeness_audit.json")
    modules = load("data/module_registry.json")
    coverage = load("data/coverage_matrix.json")

    assert pub["sources_discovered"] == mmsc["metrics"]["sources_discovered"]
    assert pub["canonical_master_records"] == mmsc["metrics"]["canonical_master_records"]
    assert pub["additional_federated_discoveries"] == mmsc["metrics"]["additional_federated_discoveries"]
    assert pub["still_to_acquire_additional_discoveries"] == mmsc["metrics"]["still_to_acquire_additional_discoveries"]
    assert pub["mundarica_expected_volumes"] == audit["expected_volumes"]
    assert pub["mundarica_verified_complete_volumes"] == sum(bool(v.get("verified_complete")) for v in audit["volumes"])
    assert pub["mundarica_page_accounting_complete_volumes"] == sum(bool(v.get("page_accounting_complete")) for v in audit["volumes"])
    assert pub["registered_streamlit_modules"] == len(modules["modules"])
    assert pub["coverage_matrix_rows"] == len(coverage["rows"])
    assert pub["absolute_source_completeness_claimed"] is False
    assert pub["ocr_treated_as_verified_transcription"] is False


def test_manuscript_uses_generated_metrics_and_truthful_completion_language():
    tex = (ROOT / "publication/main.tex").read_text(encoding="utf-8")
    macros = (ROOT / "publication/generated/release_metrics.tex").read_text(encoding="utf-8")
    assert "\\input{generated/release_metrics.tex}" in tex
    assert "\\MLHKPSourcesDiscovered" in tex
    assert "\\MLHKPMundaricaVerified" in tex
    assert "never presented as future-proof or metaphysically complete" in tex
    assert "OCR is never promoted to verified transcription" in tex
    assert "\\newcommand{\\MLHKPMundaricaVerified}{0}" in macros


def test_manuscript_caption_and_citation_order_contract():
    tex = (ROOT / "publication/main.tex").read_text(encoding="utf-8")
    assert tex.index("Table~\\ref{tab:release}") < tex.index("\\begin{table}")
    assert tex.index("Algorithm~\\ref{alg:census}") < tex.index("\\begin{algorithm}")
    assert tex.index("Algorithm~\\ref{alg:audit}") < tex.rindex("\\begin{algorithm}")
    table = tex[tex.index("\\begin{table}"):tex.index("\\end{table}")]
    algorithm = tex[tex.index("\\begin{algorithm}"):tex.index("\\end{algorithm}")]
    assert table.index("\\caption") < table.index("\\begin{tabular}")
    assert algorithm.index("\\caption") < algorithm.index("\\begin{algorithmic}")


def test_foundational_bibliography_entries_are_not_placeholders():
    bib = (ROOT / "publication/references.bib").read_text(encoding="utf-8")
    assert "10.1038/sdata.2016.18" in bib
    assert "10.5334/dsj-2020-043" in bib
    assert "TODO" not in bib
