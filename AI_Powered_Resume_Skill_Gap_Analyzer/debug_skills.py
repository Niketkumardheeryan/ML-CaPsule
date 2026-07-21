from pathlib import Path
import sys
sys.path.insert(0, r'C:\Users\lenovo\Downloads\ML-CaPsule\AI_Powered_Resume_Skill_Gap_Analyzer')
import utils.skill_extractor as se
from importlib import reload
reload(se)
print('module file:', se.__file__)
print('cwd:', Path.cwd())
repo_root = Path(se.__file__).resolve().parents[1]
print('repo_root:', repo_root)
print('repo assets exists:', (repo_root / 'assets' / 'skills_db.json').exists())
print('cwd assets exists:', (Path.cwd() / 'assets' / 'skills_db.json').exists())
print('\nCandidates tried (first 40):')
# replicate candidate generation for printout
requested = Path('assets/skills_db.json')
candidates = []
if requested.is_absolute():
    candidates.append(requested)

candidates.append(repo_root / requested)
candidates.append(Path.cwd() / requested)
for parent in repo_root.parents:
    candidates.append(parent / requested)

# glob
for p in Path(repo_root).glob('**/skills_db.json'):
    candidates.append(p)

for c in candidates[:40]:
    print(c, '- exists:', Path(c).exists())

try:
    se.load_skills_db()
    print('\nload_skills_db succeeded')
except Exception as e:
    print('\nload_skills_db raised:', type(e).__name__, e)
    import traceback
    traceback.print_exc()
