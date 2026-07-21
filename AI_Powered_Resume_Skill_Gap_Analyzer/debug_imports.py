from pathlib import Path
import sys
sys.path.insert(0, r'C:\Users\lenovo\Downloads\ML-CaPsule\AI_Powered_Resume_Skill_Gap_Analyzer')
import inspect
import utils.parser as parser
print('parser file:', parser.__file__)
print('parse_resume source:')
print(inspect.getsource(parser.parse_resume))
print('------')
print('extract_text_from_pdf source:')
print(inspect.getsource(parser.extract_text_from_pdf))
