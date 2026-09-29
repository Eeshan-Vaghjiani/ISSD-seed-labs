"""Export Member 6 documents using the shared Member 5 renderer.

Run on Windows with Python 3.8+ and python-docx, not old guest Python:
    python Member6/tools/export_documents.py
"""
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[1]
renderer = ROOT.parent / "Member5" / "tools" / "export_documents.py"
namespace = runpy.run_path(str(renderer))
export = namespace["export"]
export.__globals__["ROOT"] = ROOT
export.__globals__["FOOTER"] = "ISSD | Member 6 | SEED Dirty COW Lab"
for name in namespace["DOCUMENTS"]:
    export(name)
