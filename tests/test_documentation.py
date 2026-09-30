from pathlib import Path
from verification.structural_audit import audit

def test_required_root_documents_exist():
    root = Path(__file__).resolve().parents[1]
    for name in [
        "agent.yaml", "SOUL.md", "AGENTS.md", "DUTIES.md", "RULES.md",
        "EXPLAINABILITY.md", "README.md", ".env.example", "requirements.txt"
    ]:
        assert (root / name).exists()

def test_explainability_structure():
    assert audit() is True
