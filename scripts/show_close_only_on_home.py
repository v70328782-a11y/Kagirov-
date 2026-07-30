from pathlib import Path

index_path = Path('index.html')
home_path = Path('home-workout.html')
index = index_path.read_text(encoding='utf-8')
home = home_path.read_text(encoding='utf-8')

index = index.replace(
    '.workout-platform-view.fullscreen .home-workout-close{display:none!important}',
    '.workout-platform-view.fullscreen.home-screen .home-workout-close{display:grid!important;place-items:center;opacity:1;transform:scale(1)}\n    .workout-platform-view.fullscreen:not(.home-screen) .home-workout-close{display:none!important}',
    1
)

old_listener = """        if (event.data?.type === 'kagirov-home-workout-expand') openFullscreen();
        if (event.data?.type === 'kagirov-home-workout-collapse') closeFullscreen();"""
new_listener = """        if (event.data?.type === 'kagirov-home-workout-expand') openFullscreen();
        if (event.data?.type === 'kagirov-home-workout-collapse') closeFullscreen();
        if (event.data?.type === 'kagirov-home-workout-screen') {
          platform.classList.toggle('home-screen', event.data.screen === 'home');
        }"""
if old_listener not in index:
    raise SystemExit('Parent message listener not found')
index = index.replace(old_listener, new_listener, 1)

old_open_fullscreen = """      function openFullscreen() {
        if (platform.classList.contains('fullscreen')) return;
        document.body.classList.add('home-workout-fullscreen');
        platform.classList.add('fullscreen');"""
new_open_fullscreen = """      function openFullscreen() {
        if (platform.classList.contains('fullscreen')) return;
        document.body.classList.add('home-workout-fullscreen');
        platform.classList.add('fullscreen');
        platform.classList.add('home-screen');"""
if old_open_fullscreen in index:
    index = index.replace(old_open_fullscreen, new_open_fullscreen, 1)

old_open_program = 'function openProgram(id){selectedLevel=levels[id]||levels.calibration;completedExercises=new Set();updateTheme();updateHeader();renderSections();updateProgress();configureTimer();homeScreen.classList.remove("active");programScreen.classList.add("active");scrollTo({top:0,behavior:"smooth"})}'
new_open_program = 'function openProgram(id){selectedLevel=levels[id]||levels.calibration;completedExercises=new Set();updateTheme();updateHeader();renderSections();updateProgress();configureTimer();homeScreen.classList.remove("active");programScreen.classList.add("active");window.parent.postMessage({type:"kagirov-home-workout-screen",screen:"program"},window.location.origin);scrollTo({top:0,behavior:"smooth"})}'
if old_open_program not in home:
    raise SystemExit('openProgram not found')
home = home.replace(old_open_program, new_open_program, 1)

old_close_program = 'function closeProgram(){stopTimer();programScreen.classList.remove("active");homeScreen.classList.add("active");scrollTo({top:0,behavior:"smooth"})}'
new_close_program = 'function closeProgram(){stopTimer();programScreen.classList.remove("active");homeScreen.classList.add("active");window.parent.postMessage({type:"kagirov-home-workout-screen",screen:"home"},window.location.origin);scrollTo({top:0,behavior:"smooth"})}'
if old_close_program not in home:
    raise SystemExit('closeProgram not found')
home = home.replace(old_close_program, new_close_program, 1)

index_path.write_text(index, encoding='utf-8')
home_path.write_text(home, encoding='utf-8')
