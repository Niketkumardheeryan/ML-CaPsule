from pathlib import Path
import sys
sys.path.insert(0, r'C:\Users\lenovo\Downloads\ML-CaPsule\AI_Powered_Resume_Skill_Gap_Analyzer')
from utils.parser import extract_text_from_pdf

path = Path('sample_resume.pdf')
print('exists', path.exists(), 'path', path.resolve())
try:
    text = extract_text_from_pdf(path)
    print('EXTRACTED TEXT:')
    print(text[:1000])
except Exception as e:
    print('ERROR', type(e).__name__, str(e))
    import traceback
    traceback.print_exc()
