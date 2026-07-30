from pathlib import Path

index_path = Path('index.html')
home_path = Path('home-workout.html')
index = index_path.read_text(encoding='utf-8')
home = home_path.read_text(encoding='utf-8')

# Hide the old close button permanently.
index = index.replace(
    '.workout-platform-view.fullscreen .home-workout-close{display:grid;place-items:center;opacity:1;transform:scale(1)}',
    '.workout-platform-view.fullscreen .home-workout-close{display:none!important}'
)

# Replace fullscreen controller so it notifies the iframe and does not focus the cross.
old_open = '''      function openFullscreen() {
        if (platform.classList.contains('fullscreen')) return;
        document.body.classList.add('home-workout-fullscreen');
        platform.classList.add('fullscreen');
        const frame = platform.querySelector('.workout-platform-frame');
        if (frame) {
          frame.style.opacity = '1';
          frame.style.visibility = 'visible';
        }
        window.setTimeout(() => closeButton.focus({ preventScroll: true }), 180);
      }'''
new_open = '''      function sendFullscreenState(isFullscreen) {
        const frame = platform.querySelector('.workout-platform-frame');
        try {
          frame?.contentWindow?.postMessage({
            type: 'kagirov-home-workout-fullscreen-state',
            fullscreen: isFullscreen
          }, window.location.origin);
        } catch (error) {}
      }

      function openFullscreen() {
        if (platform.classList.contains('fullscreen')) return;
        document.body.classList.add('home-workout-fullscreen');
        platform.classList.add('fullscreen');
        const frame = platform.querySelector('.workout-platform-frame');
        if (frame) {
          frame.style.opacity = '1';
          frame.style.visibility = 'visible';
        }
        window.setTimeout(() => sendFullscreenState(true), 80);
      }'''
if old_open in index:
    index = index.replace(old_open, new_open, 1)
else:
    # Support the compact current variant.
    marker = "      function openFullscreen() {"
    start = index.find(marker)
    if start < 0:
        raise SystemExit('openFullscreen not found')
    end = index.find("\n      function closeFullscreen()", start)
    if end < 0:
        raise SystemExit('closeFullscreen not found')
    index = index[:start] + new_open + index[end:]

old_close = '''      function closeFullscreen() {
        platform.classList.remove('fullscreen');
        document.body.classList.remove('home-workout-fullscreen');
      }'''
new_close = '''      function closeFullscreen() {
        platform.classList.remove('fullscreen');
        document.body.classList.remove('home-workout-fullscreen');
        sendFullscreenState(false);
      }'''
if old_close not in index:
    raise SystemExit('closeFullscreen block not found')
index = index.replace(old_close, new_close, 1)

# Add a fullscreen-only back arrow to the embedded platform.
style_marker = '</style>'
back_css = '''
    .fullscreen-exit-back {
      display: none;
      position: fixed;
      top: calc(12px + var(--safe-top));
      left: 12px;
      z-index: 120;
      width: 46px;
      height: 46px;
      border: 1px solid rgba(101,67,47,.15);
      border-radius: 15px;
      color: var(--accent-dark);
      background: rgba(255,253,249,.96);
      box-shadow: var(--shadow-sm);
      font-size: 23px;
      font-weight: 850;
      cursor: pointer;
    }
    body.parent-fullscreen #homeScreen.active .fullscreen-exit-back {
      display: flex;
      align-items: center;
      justify-content: center;
    }
'''
if 'fullscreen-exit-back' not in home:
    home = home.replace(style_marker, back_css + '\n  </style>', 1)

body_marker = '<main class="app">'
back_button = '''<button id="fullscreenExitBack" class="fullscreen-exit-back" type="button" aria-label="Вернуться в основной сайт">←</button>\n  '''
if 'id="fullscreenExitBack"' not in home:
    home = home.replace(body_marker, back_button + body_marker, 1)

# Add child-side fullscreen state and collapse behavior.
script_insert = '''
  <script>
    (() => {
      "use strict";
      const exitBack = document.getElementById("fullscreenExitBack");

      window.addEventListener("message", event => {
        if (event.origin !== window.location.origin) return;
        if (event.data?.type !== "kagirov-home-workout-fullscreen-state") return;
        document.body.classList.toggle("parent-fullscreen", Boolean(event.data.fullscreen));
      });

      exitBack?.addEventListener("click", () => {
        window.parent.postMessage({ type: "kagirov-home-workout-collapse" }, window.location.origin);
      });
    })();
  </script>
'''
if 'kagirov-home-workout-fullscreen-state' not in home:
    home = home.replace('</body>', script_insert + '\n</body>', 1)

index_path.write_text(index, encoding='utf-8')
home_path.write_text(home, encoding='utf-8')
