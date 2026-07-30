from pathlib import Path

home_path = Path('home-workout.html')
index_path = Path('index.html')
home = home_path.read_text(encoding='utf-8')
index = index_path.read_text(encoding='utf-8')

old = '''      openProgram(levelId);
      requestAnimationFrame(()=>window.parent.postMessage({type:"kagirov-home-workout-expand"},window.location.origin));'''
new = '''      window.parent.postMessage({type:"kagirov-home-workout-screen",screen:"program"},window.location.origin);
      openProgram(levelId);
      requestAnimationFrame(()=>window.parent.postMessage({type:"kagirov-home-workout-expand",screen:"program"},window.location.origin));'''
if old not in home:
    raise SystemExit('rank handler not found')
home = home.replace(old, new, 1)

old_parent = '''        if (event.data?.type === 'kagirov-home-workout-expand') openFullscreen();'''
new_parent = '''        if (event.data?.type === 'kagirov-home-workout-expand') {
          platform.classList.toggle('home-screen', event.data?.screen !== 'program');
          openFullscreen();
        }'''
if old_parent not in index:
    raise SystemExit('parent expand handler not found')
index = index.replace(old_parent, new_parent, 1)

home_path.write_text(home, encoding='utf-8')
index_path.write_text(index, encoding='utf-8')
