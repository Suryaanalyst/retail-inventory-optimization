from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

folders = [
    "data/raw",
    "data/processed",
    "sql",
    "powerbi",
    "reports",
    "outputs",
]

for folder in folders:
    (PROJECT_ROOT / folder).mkdir(
        parents=True, exist_ok=True
    )

print("Project folders created successfully!")

