"""Write the Hugging Face and Kaggle mirror files from site/data/protologue.json.

Run after build.py. Output:
  mirror/hf/data/terms.jsonl, mirror/hf/data/categories.jsonl  (same schema as the HF dataset)
  mirror/kaggle/  (the four site/data exports + dataset-metadata.json for the Kaggle CLI)
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "site" / "data"
OUT = ROOT / "mirror"
KAGGLE_ID = "protologue/protologue"


def main():
    d = json.loads((SRC / "protologue.json").read_text(encoding="utf-8"))
    cats = {c["id"]: c for c in d["categories"]}

    hf = OUT / "hf" / "data"
    hf.mkdir(parents=True, exist_ok=True)
    with open(hf / "terms.jsonl", "w", encoding="utf-8") as f:
        for t in d["terms"]:
            row = {
                "id": t["code"], "slug": t["id"], "term": t["term"], "aliases": t["aliases"],
                "category": cats.get(t["category"], {}).get("name", t["category"]),
                "definition": t["definition"], "description": t["description"], "example": t["example"],
                "broader": t["broader"], "narrower": t["narrower"], "related": t["related"],
                "introduced": t["introduced"], "sources": t["sources"], "url": t["url"], "citation": t["citation"],
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    with open(hf / "categories.jsonl", "w", encoding="utf-8") as f:
        for c in d["categories"]:
            row = {
                "id": c["id"], "name": c["name"], "description": c["description"],
                "url": f"https://protologue.com/c/{c['id']}/",
                "terms": [t["term"] for t in d["terms"] if t["category"] == c["id"]],
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    kg = OUT / "kaggle"
    kg.mkdir(parents=True, exist_ok=True)
    for name in ("protologue.json", "protologue.csv", "protologue.skos.jsonld", "protologue.ttl"):
        shutil.copy(SRC / name, kg / name)
    (kg / "dataset-metadata.json").write_text(json.dumps({"id": KAGGLE_ID, "licenses": [{"name": "CC-BY-4.0"}]}, indent=2))

    print(f"{len(d['terms'])} terms, {len(d['categories'])} categories, version {d.get('version')} -> {OUT}")


if __name__ == "__main__":
    main()
