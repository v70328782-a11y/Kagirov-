from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

css = '''

    /* HOME WORKOUT PLATFORM */
    .workout-platform-view {
      min-height: calc(100svh - 120px);
    }

    .workout-platform-head {
      display: flex;
      align-items: end;
      justify-content: space-between;
      gap: 12px;
      margin: 4px 2px 13px;
    }

    .workout-platform-head h2 {
      margin: 0;
      color: var(--text);
      font-size: 24px;
      letter-spacing: -.045em;
    }

    .workout-platform-head p {
      margin: 5px 0 0;
      color: var(--muted);
      font-size: 12px;
    }

    .workout-platform-frame {
      display: block;
      width: 100%;
      height: calc(100svh - 190px);
      min-height: 620px;
      border: 1px solid var(--line);
      border-radius: 25px;
      background: #e7d3c0;
      box-shadow: 0 17px 48px rgba(91,61,35,.12);
    }

    @media (max-width: 650px) {
      .workout-platform-frame {
        height: calc(100svh - 165px);
        min-height: 560px;
        border-radius: 20px;
      }
    }
'''

if "/* HOME WORKOUT PLATFORM */" not in text:
    text = text.replace("\n  </style>", css + "\n  </style>", 1)

section = '''

      <section class="view workout-platform-view" data-view="home-workout">
        <div class="workout-platform-head">
          <div>
            <h2>Домашняя тренировка</h2>
            <p>Отдельная платформа внутри kagirov: четыре ранга, упражнения и интервальный таймер</p>
          </div>
        </div>

        <iframe
          class="workout-platform-frame"
          src="home-workout.html"
          title="Домашняя тренировка"
          loading="eager"
          allow="autoplay"
        ></iframe>
      </section>
'''

marker = '      <section class="view" data-view="progress">'
if 'data-view="home-workout"' not in text:
    if marker not in text:
        raise SystemExit("Progress section marker not found")
    text = text.replace(marker, section + "\n" + marker, 1)

nav_button = '''
    <button class="nav-btn" data-view-target="home-workout">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 20h16"></path>
        <path d="M7 20v-5l2-2 2 2v5"></path>
        <path d="M13 20v-8l2-2 2 2v8"></path>
        <path d="M5 8h14"></path>
        <path d="M8 8V5h8v3"></path>
      </svg>
      <span>Домашняя</span>
    </button>

'''

progress_nav = '    <button class="nav-btn" data-view-target="progress">'
if 'data-view-target="home-workout"' not in text:
    if progress_nav not in text:
        raise SystemExit("Progress nav marker not found")
    text = text.replace(progress_nav, nav_button + progress_nav, 1)

text = text.replace('grid-template-columns: repeat(4,1fr);', 'grid-template-columns: repeat(5,1fr);', 1)
text = text.replace('grid-template-columns: repeat(4, 1fr);', 'grid-template-columns: repeat(5, 1fr);', 1)

path.write_text(text, encoding="utf-8")
