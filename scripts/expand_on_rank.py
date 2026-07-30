from pathlib import Path

path = Path('home-workout.html')
text = path.read_text(encoding='utf-8')
old = 'card.addEventListener("click", () => openProgram(card.dataset.level));'
new = '''card.addEventListener("click", () => {
          try {
            window.parent.postMessage({ type: "kagirov-home-workout-fullscreen" }, window.location.origin);
          } catch (_) {}
          openProgram(card.dataset.level);
        });'''
if old not in text:
    raise SystemExit('Rank click handler not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
