from pathlib import Path
import re

index_path = Path('index.html')
home_path = Path('home-workout.html')
index = index_path.read_text(encoding='utf-8')
home = home_path.read_text(encoding='utf-8')

start = index.find('    /* HOME WORKOUT FULLSCREEN MODE */')
end = index.find('\n  </style>', start)
if start < 0 or end < 0:
    raise SystemExit('Fullscreen CSS block not found')

css = '''    /* HOME WORKOUT FULLSCREEN MODE */
    body.home-workout-fullscreen { overflow: hidden; }

    .home-workout-close {
      display: none;
      position: fixed;
      top: max(12px, env(safe-area-inset-top));
      right: 12px;
      z-index: 1003;
      width: 46px;
      height: 46px;
      border: 1px solid rgba(103,77,52,.18);
      border-radius: 15px;
      color: var(--text);
      background: rgba(255,253,249,.97);
      box-shadow: 0 12px 34px rgba(91,61,35,.20);
      font-size: 23px;
      cursor: pointer;
      opacity: 0;
      transform: scale(.92);
      transition: opacity .2s ease .12s, transform .2s ease .12s;
    }

    .workout-platform-view.fullscreen {
      position: fixed;
      inset: 0;
      z-index: 1000;
      display: block !important;
      min-height: 100svh;
      padding: 0;
      background: #e7d3c0;
      animation: workoutPlatformOpen .42s cubic-bezier(.22,.78,.24,1) both;
    }

    .workout-platform-view.fullscreen .workout-platform-head { display: none; }
    .workout-platform-view.fullscreen .home-workout-close {
      display: grid;
      place-items: center;
      opacity: 1;
      transform: scale(1);
    }

    .workout-platform-view.fullscreen .workout-platform-frame {
      display: block !important;
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100svh;
      min-height: 100svh;
      border: 0;
      border-radius: 0;
      box-shadow: none;
      opacity: 1 !important;
      visibility: visible !important;
      filter: none !important;
      transform: translateZ(0);
      background: #e7d3c0;
      pointer-events: auto;
    }

    @keyframes workoutPlatformOpen {
      from { opacity: .25; transform: scale(.985) translateY(7px); }
      to { opacity: 1; transform: none; }
    }
'''
index = index[:start] + css + index[end:]

index = re.sub(
    r"      function openFullscreen\(\) \{.*?\n      \}",
    '''      function openFullscreen() {
        if (platform.classList.contains('fullscreen')) return;
        document.body.classList.add('home-workout-fullscreen');
        platform.classList.add('fullscreen');
        const frame = platform.querySelector('.workout-platform-frame');
        if (frame) {
          frame.style.opacity = '1';
          frame.style.visibility = 'visible';
          frame.style.filter = 'none';
          frame.style.pointerEvents = 'auto';
        }
        window.setTimeout(() => closeButton.focus({ preventScroll: true }), 120);
      }''',
    index,
    count=1,
    flags=re.S,
)

home = re.sub(
    r'function renderLevels\(\)\{.*?\n    \}\)\}',
    '''function renderLevels(){levelGrid.innerHTML=Object.values(levels).map(level=>`<button class="level-card" type="button" data-level="${level.id}" style="--level-color:${level.color};--level-soft:${level.soft}"><span class="level-number">${level.number}</span><div class="level-kicker">${level.short}</div><strong class="level-name">${level.name}</strong><div class="level-description">${level.description}</div><div class="level-meta"><span>${level.duration}</span><span>${level.work}/${level.rest}</span></div><span class="level-arrow">→</span></button>`).join("");levelGrid.querySelectorAll(".level-card").forEach(card=>card.addEventListener("click",()=>{
      const levelId=card.dataset.level;
      card.blur();
      openProgram(levelId);
      requestAnimationFrame(()=>window.parent.postMessage({type:"kagirov-home-workout-expand"},window.location.origin));
    }))}''',
    home,
    count=1,
    flags=re.S,
)

index_path.write_text(index, encoding='utf-8')
home_path.write_text(home, encoding='utf-8')
