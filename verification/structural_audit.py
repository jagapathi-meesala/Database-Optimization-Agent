from pathlib import Path
import re, yaml

ROOT = Path(__file__).resolve().parents[1]

def audit():
    manifest = yaml.safe_load((ROOT / "agent.yaml").read_text())
    assert manifest["spec_version"] == "0.1.0"
    assert re.fullmatch(r"[a-z][a-z0-9-]*", manifest["name"])
    assert re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", str(manifest["version"]))
    assert isinstance(manifest["skills"], list)
    assert isinstance(manifest["tools"], list)
    for skill in manifest["skills"]:
        assert (ROOT / "skills" / skill / "SKILL.md").exists()
    for tool in manifest["tools"]:
        assert (ROOT / "tools" / f"{tool}.yaml").exists()
    text = (ROOT / "EXPLAINABILITY.md").read_text()
    for heading in ["## Inputs and Data Sources", "## Decision and Reasoning", "## Limits and Constraints"]:
        assert heading in text
    assert "## Inputs\n" not in text
    assert "## Decision\n" not in text
    assert "## Limits\n" not in text
    return True

if __name__ == "__main__":
    audit()
    print("Structural audit passed.")
