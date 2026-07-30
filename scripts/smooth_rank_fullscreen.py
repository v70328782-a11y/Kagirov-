from pathlib import Path

child_path = Path('home-workout.html')
index_path = Path('index.html')
child = child_path.read_text(encoding='utf-8')
index = index_path.read_text(encoding='utf-8')

old_handler = 'levelGrid.querySelectorAll(".level-card").forEach(card=>card.addEventListener("click",()=>openProgram(card.dataset.level)))'
new_handler = '''levelGrid.querySelectorAll(".level-card").forEach(card=>card.addEventListener("click",()=>{
      try{window.parent.postMessage({type:"kagirov-home-workout-expand"},window.location.origin)}catch(error){}
      const levelId=card.dataset.level;
      setTimeout(()=>openProgram(levelId),520);
    }))'''
if old_handler in child:
    child = child.replace(old_handler, new_handler, 1)
elif 'setTimeout(()=>openProgram(levelId),520)' not in child:
    raise SystemExit('Rank click handler marker not found')

child = child.replace('.screen{display:none;animation:screenIn .4s ease}', '.screen{display:none;animation:screenIn .9s cubic-bezier(.16,1,.3,1)}', 1)
child = child.replace('from{opacity:0;transform:translateY(12px)}', 'from{opacity:0;transform:translateY(24px) scale(.985);filter:blur(5px)}', 1)
child = child.replace('to{opacity:1;transform:none}', 'to{opacity:1;transform:none;filter:blur(0)}', 1)
child_path.write_text(child, encoding='utf-8')

# Slow, premium fullscreen expansion for the embedded platform.
if '/* HOME WORKOUT ULTRA SMOOTH */' not in index:
    smooth_css = '''

    /* HOME WORKOUT ULTRA SMOOTH */
    .workout-platform-view,
    .workout-platform-head,
    .workout-platform-frame,
    .home-workout-close,
    .topbar,
    .bottom-nav {
      transition:
        opacity 1.05s cubic-bezier(.16,1,.3,1),
        transform 1.12s cubic-bezier(.16,1,.3,1),
        inset 1.12s cubic-bezier(.16,1,.3,1),
        width 1.12s cubic-bezier(.16,1,.3,1),
        height 1.12s cubic-bezier(.16,1,.3,1),
        border-radius 1.12s cubic-bezier(.16,1,.3,1),
        box-shadow 1.12s cubic-bezier(.16,1,.3,1);
    }

    .workout-platform-view::before {
      content: "";
      position: fixed;
      inset: 0;
      z-index: 998;
      pointer-events: none;
      background: rgba(91,61,35,.16);
      backdrop-filter: blur(0);
      opacity: 0;
      transition: opacity 1.05s cubic-bezier(.16,1,.3,1), backdrop-filter 1.05s cubic-bezier(.16,1,.3,1);
    }

    body.home-workout-fullscreen .workout-platform-view::before {
      opacity: 1;
      backdrop-filter: blur(9px);
    }

    body.home-workout-fullscreen .workout-platform-frame {
      animation: homeWorkoutExpand 1.12s cubic-bezier(.16,1,.3,1) both;
    }

    @keyframes homeWorkoutExpand {
      0% { opacity:.72; transform:scale(.94) translateY(28px); filter:blur(7px); }
      55% { opacity:1; }
      100% { opacity:1; transform:none; filter:blur(0); }
    }
'''
    index = index.replace('\n  </style>', smooth_css + '\n  </style>', 1)

# Ensure fullscreen mode itself transitions instead of snapping.
index = index.replace('body.home-workout-fullscreen { overflow: hidden; }', 'body.home-workout-fullscreen { overflow: hidden; }', 1)
index_path.write_text(index, encoding='utf-8')
