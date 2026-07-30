from pathlib import Path

index_path = Path('index.html')
child_path = Path('home-workout.html')
index = index_path.read_text(encoding='utf-8')
child = child_path.read_text(encoding='utf-8')

index_css = r'''

    /* HOME WORKOUT FULLSCREEN MODE */
    body.home-workout-fullscreen { overflow: hidden; }

    .home-workout-close {
      display: none;
      position: fixed;
      top: max(12px, env(safe-area-inset-top));
      right: 12px;
      z-index: 1002;
      width: 46px;
      height: 46px;
      border: 1px solid rgba(103,77,52,.18);
      border-radius: 15px;
      color: var(--text);
      background: rgba(255,253,249,.94);
      box-shadow: 0 12px 34px rgba(91,61,35,.20);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      font-size: 23px;
      cursor: pointer;
    }

    .workout-platform-view.fullscreen {
      position: fixed;
      inset: 0;
      z-index: 1000;
      display: block !important;
      min-height: 100svh;
      padding: 0;
      background: #e7d3c0;
    }

    .workout-platform-view.fullscreen .workout-platform-head { display: none; }
    .workout-platform-view.fullscreen .home-workout-close { display: grid; place-items: center; }

    .workout-platform-view.fullscreen .workout-platform-frame {
      width: 100%;
      height: 100svh;
      min-height: 100svh;
      border: 0;
      border-radius: 0;
      box-shadow: none;
    }
'''

if '/* HOME WORKOUT FULLSCREEN MODE */' not in index:
    index = index.replace('\n  </style>', index_css + '\n  </style>', 1)

if 'id="closeHomeWorkoutFullscreen"' not in index:
    marker = '        <iframe\n          class="workout-platform-frame"'
    button = '        <button class="home-workout-close" id="closeHomeWorkoutFullscreen" type="button" aria-label="Свернуть домашнюю тренировку">×</button>\n\n'
    if marker not in index:
        raise SystemExit('iframe marker not found')
    index = index.replace(marker, button + marker, 1)

index_js = r'''

  <script>
    (() => {
      "use strict";
      const platform = document.querySelector('[data-view="home-workout"]');
      const closeButton = document.getElementById('closeHomeWorkoutFullscreen');
      if (!platform || !closeButton) return;

      function openFullscreen() {
        platform.classList.add('fullscreen');
        document.body.classList.add('home-workout-fullscreen');
        closeButton.focus({ preventScroll: true });
      }

      function closeFullscreen() {
        platform.classList.remove('fullscreen');
        document.body.classList.remove('home-workout-fullscreen');
      }

      window.addEventListener('message', event => {
        if (event.origin !== window.location.origin) return;
        if (event.data?.type === 'kagirov-home-workout-expand') openFullscreen();
        if (event.data?.type === 'kagirov-home-workout-collapse') closeFullscreen();
      });

      closeButton.addEventListener('click', closeFullscreen);
      document.querySelectorAll('.nav-btn').forEach(button => {
        button.addEventListener('click', () => {
          if (button.dataset.viewTarget !== 'home-workout') closeFullscreen();
        });
      });
      document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && platform.classList.contains('fullscreen')) closeFullscreen();
      });
    })();
  </script>
'''

if 'kagirov-home-workout-expand' not in index:
    index = index.replace('\n</body>', index_js + '\n</body>', 1)

child_css = r'''

    /* TAP HERO TO OPEN FULLSCREEN */
    #homeScreen .hero {
      cursor: pointer;
      touch-action: pan-y;
    }
    #homeScreen .hero::selection { background: transparent; }
    #homeScreen .hero:focus-visible {
      outline: 4px solid rgba(131,93,69,.24);
      outline-offset: 4px;
    }
'''
if '/* TAP HERO TO OPEN FULLSCREEN */' not in child:
    child = child.replace('\n  </style>', child_css + '\n  </style>', 1)

child_js = r'''

  <script>
    (() => {
      "use strict";
      const hero = document.querySelector('#homeScreen .hero');
      if (!hero) return;
      hero.setAttribute('role', 'button');
      hero.setAttribute('tabindex', '0');
      hero.setAttribute('aria-label', 'Открыть домашнюю тренировку на весь экран');

      let startPoint = null;
      hero.addEventListener('pointerdown', event => {
        startPoint = { x: event.clientX, y: event.clientY, id: event.pointerId };
      });
      hero.addEventListener('pointerup', event => {
        if (!startPoint || startPoint.id !== event.pointerId) return;
        const moved = Math.hypot(event.clientX - startPoint.x, event.clientY - startPoint.y);
        startPoint = null;
        if (moved > 10) return;
        window.parent.postMessage({ type: 'kagirov-home-workout-expand' }, window.location.origin);
      });
      hero.addEventListener('pointercancel', () => { startPoint = null; });
      hero.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          window.parent.postMessage({ type: 'kagirov-home-workout-expand' }, window.location.origin);
        }
      });
    })();
  </script>
'''
if 'Открыть домашнюю тренировку на весь экран' not in child:
    child = child.replace('\n</body>', child_js + '\n</body>', 1)

index_path.write_text(index, encoding='utf-8')
child_path.write_text(child, encoding='utf-8')
