"""Update the standalone chart from data/sales.json without dependencies."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / "data/sales.json").read_text(encoding="utf-8"))
ids = [row["id"] for row in data]
if len(ids) != len(set(ids)):
    raise ValueError("Duplicate apartment identifiers")
payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
chart = root / "index.html"
source = chart.read_text(encoding="utf-8")
updated, count = re.subn(
    r"const data=.*?;\nconst board=",
    lambda _: "const data=" + payload + ";\nconst board=",
    source,
    count=1,
    flags=re.S,
)
if count != 1:
    raise ValueError("Embedded data block not found")
chart.write_text(updated, encoding="utf-8")
print(f"Embedded {len(data)} apartment records")
