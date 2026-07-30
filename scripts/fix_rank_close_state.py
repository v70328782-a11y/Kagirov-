from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old = '''      function openFullscreen() {
        if (platform.classList.contains('fullscreen')) return;
        document.body.classList.add('home-workout-fullscreen');
        platform.classList.add('fullscreen');
        platform.classList.add('home-screen');
        const frame = platform.querySelector('.workout-platform-frame');'''

new = '''      function openFullscreen(screen) {
        if (screen === 'program') platform.classList.remove('home-screen');
        if (screen === 'home') platform.classList.add('home-screen');
        if (platform.classList.contains('fullscreen')) return;
        document.body.classList.add('home-workout-fullscreen');
        platform.classList.add('fullscreen');
        const frame = platform.querySelector('.workout-platform-frame');'''

if old not in text:
    raise SystemExit('openFullscreen block not found')
text = text.replace(old, new, 1)

old_handler = '''        if (event.data?.type === 'kagirov-home-workout-expand') {
          platform.classList.toggle('home-screen', event.data?.screen !== 'program');
          openFullscreen();
        }'''
new_handler = '''        if (event.data?.type === 'kagirov-home-workout-expand') {
          openFullscreen(event.data?.screen || 'home');
        }'''

if old_handler not in text:
    raise SystemExit('expand handler not found')
text = text.replace(old_handler, new_handler, 1)

path.write_text(text, encoding='utf-8')
