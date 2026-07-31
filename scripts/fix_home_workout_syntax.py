from pathlib import Path

path = Path('home-workout.html')
text = path.read_text(encoding='utf-8')

bad = 'function updateProgress({const total='
good = 'function updateProgress(){const total='

if bad not in text:
    raise SystemExit('Expected malformed updateProgress function was not found')

text = text.replace(bad, good, 1)

required = [
    'function updateProgress(){const total=',
    'function humanPlanFor(sectionId,index,exercise)',
    'Как проходить тренировку',
    'Сколько сделать',
    'Кардио по минутам'
]
for marker in required:
    if marker not in text:
        raise SystemExit(f'Missing marker: {marker}')

path.write_text(text, encoding='utf-8')
