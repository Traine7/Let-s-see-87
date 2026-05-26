from dataclasses import dataclass, asdict
import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "branch_registry.json"

@dataclass
class Branch:
    name: str
    purpose: str
    status: str
    next_action: str

DEFAULT_BRANCHES = [
    Branch("Story of Pi", "Manuscript + coding curriculum + GUI/game narrative", "active seed", "Normalize chapter registry and map scenes to screens"),
    Branch("GUI/UX", "Accessible app/game interface for Supreme Brain and CodeQuest", "active seed", "Create screen map and component list"),
    Branch("Leadership Doctrine", "Thesis and strategic leadership archive", "active seed", "Create chapter outline and source map"),
    Branch("Real Estate/Housing", "VA, land, build, accessibility, dreams board", "active seed", "Create property evaluation template"),
    Branch("Finance/FNA", "Debt efficiency, payoff, mortgage/refinance strategy", "active seed", "Create debt registry and scenario calculator"),
    Branch("Language Scroll", "Spanish, French, Bemba immersion system", "active seed", "Build comparative lesson tracker"),
    Branch("AI Automation", "Multi-AI orchestration and business automation", "active seed", "Define roles and workflow routing"),
]

def save_defaults():
    DATA_PATH.write_text(json.dumps([asdict(b) for b in DEFAULT_BRANCHES], indent=2), encoding="utf-8")


def load_branches():
    if not DATA_PATH.exists():
        save_defaults()
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def print_dashboard():
    print("SUPREME BRAIN DASHBOARD")
    print("=" * 28)
    for i, branch in enumerate(load_branches(), 1):
        print(f"{i}. {branch['name']} [{branch['status']}]")
        print(f"   Purpose: {branch['purpose']}")
        print(f"   Next: {branch['next_action']}\n")

if __name__ == "__main__":
    print_dashboard()
