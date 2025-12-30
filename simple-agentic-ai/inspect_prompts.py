import importlib, inspect, io, os
m = importlib.import_module('prompts')
print('module file:', getattr(m,'__file__',None))
print('full dir:', dir(m))
print('exported (no _):', [n for n in dir(m) if not n.startswith('_')])
print('SYSTEM_PROMPT present:', hasattr(m,'SYSTEM_PROMPT'))
print('SYSTEM_PROMPT repr:', repr(getattr(m,'SYSTEM_PROMPT',None)))
fn = os.path.join(os.path.dirname(__file__), 'prompts.py')
print('\n--- prompts.py raw content ---')
with open(fn, 'r', encoding='utf-8') as f:
	print(f.read())
