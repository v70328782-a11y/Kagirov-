from pathlib import Path
import re

path = Path('home-workout.html')
text = path.read_text(encoding='utf-8')

# ---------- Home screen wording ----------
text = text.replace(
    '<h1>Домашняя <span>кросс-фит тренировка</span></h1>',
    '<h1>Домашняя <span>тренировка</span></h1>',
    1,
)
text = text.replace(
    '<p>Полноценная тренировка без оборудования и без необходимости перемещаться по комнате. Достаточно свободного участка примерно 1 × 2 метра, собственного веса и строгой техники.</p>',
    '<p>Полноценная тренировка без оборудования. В каждом упражнении прямо написано: сколько сделать подходов, сколько повторений или секунд и сколько отдыхать.</p>',
    1,
)
text = text.replace(
    '<div class="hero-tags"><span>Без инвентаря</span><span>На одном месте</span><span>Всё тело</span><span>4 ранга</span><span>Интервальный таймер</span></div>',
    '<div class="hero-tags"><span>Без инвентаря</span><span>На одном месте</span><span>Всё тело</span><span>4 уровня</span><span>Понятные подходы</span></div>',
    1,
)

# ---------- Program header and timer wording ----------
old_program_hero = '<article class="program-hero"><div class="program-hero-content"><div id="rankLabel" class="rank">Ранг I</div><h1 id="programTitle" class="program-title">Калибровка</h1><p id="programSubtitle" class="program-subtitle"></p><div class="stats"><div class="stat"><small>Длительность</small><strong id="durationStat"></strong></div><div class="stat"><small>Работа</small><strong id="workStat"></strong></div><div class="stat"><small>Отдых</small><strong id="restStat"></strong></div></div><button id="heroTimerButton" class="timer-launch" type="button">◷ Таймер силового блока</button></div></article>'
new_program_hero = '<article class="program-hero"><div class="program-hero-content"><div id="rankLabel" class="rank">Ранг I</div><h1 id="programTitle" class="program-title">Калибровка</h1><p id="programSubtitle" class="program-subtitle"></p><div class="stats"><div class="stat"><small>Длительность</small><strong id="durationStat"></strong></div><div class="stat"><small>Подходов</small><strong id="workStat"></strong></div><div class="stat"><small>Отдых между подходами</small><strong id="restStat"></strong></div></div><button id="heroTimerButton" class="timer-launch" type="button">◷ Открыть таймер</button></div></article>'
if old_program_hero not in text:
    raise SystemExit('Program hero not found')
text = text.replace(old_program_hero, new_program_hero, 1)

text = text.replace(
    '<header class="topbar"><button id="backButton" class="icon-btn" type="button">←</button><div class="topbar-center"><small>Выбранный ранг</small><strong id="topbarLevelName">Калибровка</strong></div><button id="topTimerButton" class="icon-btn" type="button">◷</button></header>',
    '<header class="topbar"><button id="backButton" class="icon-btn" type="button" aria-label="Вернуться к выбору уровня">←</button><div class="topbar-center"><small>Выбранный уровень</small><strong id="topbarLevelName">Калибровка</strong></div><button id="topTimerButton" class="icon-btn" type="button" aria-label="Открыть таймер" title="Открыть таймер">◷</button></header>',
    1,
)

progress_marker = '<article class="progress-card"><div class="progress-head"><strong>Прогресс тренировки</strong><span id="progressText">0 из 0</span></div><div class="progress-track"><div id="progressFill" class="progress-fill"></div></div></article>'
guide = progress_marker + '''
      <article class="program-guide">
        <strong>Как проходить тренировку</strong>
        <div class="guide-steps">
          <div><span>1</span><p>Открой первый раздел и выполняй упражнения сверху вниз.</p></div>
          <div><span>2</span><p>Сделай указанное число подходов. Между ними отдыхай ровно столько, сколько написано.</p></div>
          <div><span>3</span><p>После выполнения нажми галочку и переходи к следующему упражнению.</p></div>
        </div>
      </article>'''
if progress_marker not in text:
    raise SystemExit('Progress marker not found')
text = text.replace(progress_marker, guide, 1)

old_timer = '<div id="timerOverlay" class="timer-overlay" aria-hidden="true"><section class="timer-panel"><header class="timer-header"><div><small>Интервальный протокол</small><strong>Таймер тренировки</strong></div><button id="closeTimerButton" class="icon-btn" type="button">×</button></header><div class="timer-display"><div id="timerPhase" class="timer-phase">Готовность</div><div id="timerTime" class="timer-time">00:30</div><div id="timerRound" class="timer-round">Круг 1 из 2</div></div><div class="timer-settings"><div class="timer-setting"><label>Работа</label><input id="workInput" type="number" value="30"></div><div class="timer-setting"><label>Отдых</label><input id="restInput" type="number" value="30"></div><div class="timer-setting"><label>Круги</label><input id="roundInput" type="number" value="2"></div></div><div class="timer-controls"><button id="resetTimerButton" class="timer-control secondary">Сброс</button><button id="startTimerButton" class="timer-control primary">Старт</button><button id="skipTimerButton" class="timer-control secondary">Далее</button></div></section></div>'
new_timer = '<div id="timerOverlay" class="timer-overlay" aria-hidden="true"><section class="timer-panel"><header class="timer-header"><div><small>Помощник по времени</small><strong>Таймер упражнения и отдыха</strong></div><button id="closeTimerButton" class="icon-btn" type="button" aria-label="Закрыть таймер">×</button></header><p class="timer-explanation">Используй таймер только там, где в программе указано время в секундах. Для обычных упражнений просто считай повторения.</p><div class="timer-display"><div id="timerPhase" class="timer-phase">Делай упражнение</div><div id="timerTime" class="timer-time">00:30</div><div id="timerRound" class="timer-round">Подход 1 из 2</div></div><div class="timer-settings"><div class="timer-setting"><label>Делать, секунд</label><input id="workInput" type="number" value="30"></div><div class="timer-setting"><label>Отдыхать, секунд</label><input id="restInput" type="number" value="30"></div><div class="timer-setting"><label>Подходов</label><input id="roundInput" type="number" value="2"></div></div><div class="timer-controls"><button id="resetTimerButton" class="timer-control secondary">Сначала</button><button id="startTimerButton" class="timer-control primary">Старт</button><button id="skipTimerButton" class="timer-control secondary">Пропустить</button></div></section></div>'
if old_timer not in text:
    raise SystemExit('Timer markup not found')
text = text.replace(old_timer, new_timer, 1)

# Clean old terminology in source data too.
text = text.replace('dose:"Весь рабочий интервал"', 'dose:"Количество указано ниже"')
text = text.replace('dose:"Удержание весь интервал"', 'dose:"Время указано ниже"')
text = text.replace('dose:"Медленно весь интервал"', 'dose:"Количество указано ниже"')
text = text.replace('dose:"Половина времени на каждую ногу"', 'dose:"Количество указано ниже"')

# ---------- Human-readable styles ----------
css = r'''

    /* HUMAN READABLE PROGRAM */
    .program-guide{
      margin-top:13px;
      padding:17px;
      border:1px solid rgba(255,255,255,.65);
      border-radius:var(--radius-lg);
      background:rgba(255,253,249,.9);
      box-shadow:var(--shadow-sm);
    }
    .program-guide>strong{font-size:14px}
    .guide-steps{display:grid;gap:9px;margin-top:13px}
    .guide-steps>div{display:flex;align-items:flex-start;gap:10px}
    .guide-steps span{
      flex:0 0 auto;
      display:grid;
      place-items:center;
      width:27px;height:27px;
      border-radius:9px;
      color:#fff;
      background:var(--selected);
      font-size:10px;
      font-weight:900;
    }
    .guide-steps p{margin:3px 0 0;color:var(--muted);font-size:11px;line-height:1.5}

    .exercise-prescription{
      display:grid;
      grid-template-columns:repeat(3,minmax(0,1fr));
      gap:7px;
      margin-top:10px;
    }
    .human-field{
      min-height:61px;
      padding:9px;
      border:1px solid var(--line);
      border-radius:12px;
      background:var(--card-2);
    }
    .human-field small{
      display:block;
      color:var(--soft);
      font-size:8px;
      font-weight:900;
      letter-spacing:.06em;
      text-transform:uppercase;
    }
    .human-field strong{
      display:block;
      margin-top:6px;
      color:var(--selected-dark);
      font-size:11px;
      line-height:1.35;
    }
    .human-field.main{
      border-color:transparent;
      color:#fff;
      background:var(--selected);
    }
    .human-field.main small{color:rgba(255,255,255,.68)}
    .human-field.main strong{color:#fff}
    .exercise-order-note{
      margin-top:9px;
      padding:9px 10px;
      border-left:3px solid var(--selected);
      border-radius:0 10px 10px 0;
      color:var(--muted);
      background:rgba(131,93,69,.055);
      font-size:10px;
      line-height:1.48;
    }
    .section-how{
      margin:0 0 12px;
      padding:14px;
      border:1px solid rgba(131,93,69,.11);
      border-radius:15px;
      background:linear-gradient(145deg,var(--selected-soft),#fff);
    }
    .section-how strong{display:block;font-size:12px;color:var(--selected-dark)}
    .section-how p{margin:7px 0 0;color:var(--muted);font-size:11px;line-height:1.55}
    .timer-explanation{
      margin:13px 0 0;
      padding:11px 12px;
      border-radius:13px;
      color:var(--muted);
      background:var(--card-2);
      font-size:10px;
      line-height:1.5;
    }
    @media(max-width:430px){
      .exercise-prescription{grid-template-columns:1fr}
      .human-field{min-height:0}
    }
'''
if '/* HUMAN READABLE PROGRAM */' not in text:
    text = text.replace('\n  </style>', css + '\n  </style>', 1)

# ---------- Human-readable data helpers ----------
old_round_function = re.compile(r'    function roundWord\(value\)\{.*?\n    \}\n', re.S)
new_words = r'''    function wordForm(value,one,few,many){
      const n=Math.abs(Number(value))%100;
      const n1=n%10;
      if(n>10&&n<20)return many;
      if(n1===1)return one;
      if(n1>=2&&n1<=4)return few;
      return many;
    }

    function approachText(value){
      return `${value} ${wordForm(value,"подход","подхода","подходов")}`;
    }

    function blockText(value){
      return `${value} ${wordForm(value,"раз","раза","раз")}`;
    }
'''
text, count = old_round_function.subn(new_words, text, count=1)
if count != 1:
    raise SystemExit('roundWord replacement failed')

prescription_pattern = re.compile(r'    function prescriptionFor\(sectionId,index,exercise\)\{.*?\n    \}\n', re.S)
new_prescription = r'''    const controlRest={calibration:45,vanguard:40,assault:30,absolute:25};

    function humanPlanFor(sectionId,index,exercise){
      const levelId=selectedLevel.id;
      if(sectionId==="strength"){
        return{
          sets:approachText(selectedLevel.strengthRounds),
          amount:exercisePrescriptions.strength[index][levelId],
          rest:`${selectedLevel.strengthRoundRest} секунд`,
          note:"Сделай все подходы этого упражнения. Только после этого переходи к следующему."
        };
      }
      if(sectionId==="control"){
        return{
          sets:approachText(selectedLevel.controlRounds),
          amount:exercisePrescriptions.control[index][levelId],
          rest:`${controlRest[levelId]} секунд`,
          note:"Повтори указанное количество подходов, сохраняя правильное положение тела."
        };
      }
      if(sectionId==="finisher"){
        return{
          sets:"Повторяй по порядку",
          amount:exercisePrescriptions.finisher[index][levelId],
          rest:"Только при необходимости",
          note:`Все четыре упражнения подряд — один полный круг. Повторяй круги в течение ${selectedLevel.finisherMinutes} минут.`
        };
      }
      if(sectionId==="warmup"){
        return{
          sets:"1 раз",
          amount:exercise.dose,
          rest:"Сразу переходи дальше",
          note:"Выполняй спокойно. Разминка не должна утомлять до начала основной части."
        };
      }
      if(sectionId==="cooldown"){
        return{
          sets:"1 раз",
          amount:exercise.dose,
          rest:"Не требуется",
          note:"Двигайся мягко и восстанавливай спокойное дыхание."
        };
      }
      return{sets:"1 раз",amount:exercise.dose,rest:"По самочувствию",note:""};
    }
'''
text, count = prescription_pattern.subn(new_prescription, text, count=1)
if count != 1:
    raise SystemExit('prescriptionFor replacement failed')

# ---------- Level cards and header ----------
render_levels_pattern = re.compile(r'    function renderLevels\(\)\{.*?\n    \}\)\}', re.S)
# The compact original function is safer to replace by exact start/end up to openProgram.
render_levels_block = re.compile(r'    function renderLevels\(\)\{.*?\n    function openProgram\(', re.S)
new_render_levels = r'''    function renderLevels(){
      levelGrid.innerHTML=Object.values(levels).map(level=>`<button class="level-card" type="button" data-level="${level.id}" style="--level-color:${level.color};--level-soft:${level.soft}"><span class="level-number">${level.number}</span><div class="level-kicker">${level.short}</div><strong class="level-name">${level.name}</strong><div class="level-description">${level.description}</div><div class="level-meta"><span>${level.duration}</span><span>${approachText(level.strengthRounds)}</span><span>отдых ${level.strengthRoundRest} сек</span></div><span class="level-arrow">→</span></button>`).join("");
      levelGrid.querySelectorAll(".level-card").forEach(card=>card.addEventListener("click",()=>{
        const levelId=card.dataset.level;
        card.blur();
        window.parent.postMessage({type:"kagirov-home-workout-screen",screen:"program"},window.location.origin);
        openProgram(levelId);
        requestAnimationFrame(()=>window.parent.postMessage({type:"kagirov-home-workout-expand",screen:"program"},window.location.origin));
      }));
    }
    function openProgram('''
text, count = render_levels_block.subn(new_render_levels, text, count=1)
if count != 1:
    raise SystemExit('renderLevels replacement failed')

update_header_pattern = re.compile(r'    function updateHeader\(\)\{.*?\}\n', re.S)
new_update_header = r'''    function updateHeader(){
      $("rankLabel").textContent=selectedLevel.rank;
      $("programTitle").textContent=selectedLevel.name;
      $("programSubtitle").textContent=selectedLevel.subtitle;
      $("topbarLevelName").textContent=selectedLevel.name;
      $("durationStat").textContent=selectedLevel.duration;
      $("workStat").textContent=approachText(selectedLevel.strengthRounds);
      $("restStat").textContent=selectedLevel.strengthRoundRest+" сек";
    }
'''
text, count = update_header_pattern.subn(new_update_header, text, count=1)
if count != 1:
    raise SystemExit('updateHeader replacement failed')

# ---------- Exercise cards ----------
cards_pattern = re.compile(r'    function cards\(exercises,sectionId\)\{.*?\n    \}\n    function section\(', re.S)
new_cards = r'''    function cards(exercises,sectionId){
      return exercises.map((e,i)=>{
        const id=sectionId+"-"+i;
        const plan=humanPlanFor(sectionId,i,e);
        return `<article class="exercise-card" data-exercise-id="${id}"><div class="exercise-top"><span class="exercise-number">${String(i+1).padStart(2,"0")}</span><div class="exercise-heading"><strong class="exercise-title">${e.title}</strong><div class="exercise-prescription"><div class="human-field"><small>Подходы</small><strong>${plan.sets}</strong></div><div class="human-field main"><small>Сколько сделать</small><strong>${plan.amount}</strong></div><div class="human-field"><small>Отдых</small><strong>${plan.rest}</strong></div></div>${plan.note?`<div class="exercise-order-note">${plan.note}</div>`:""}</div><button class="check-btn" data-check-id="${id}" aria-label="Отметить упражнение выполненным">✓</button></div><p class="exercise-description">${e.description}</p><ul class="technique-list">${e.technique.map(x=>`<li>${x}</li>`).join("")}</ul>${e.variation?`<div class="variation"><strong>Можно изменить:</strong> ${e.variation}</div>`:""}</article>`;
      }).join("");
    }
    function section('''
text, count = cards_pattern.subn(new_cards, text, count=1)
if count != 1:
    raise SystemExit('cards replacement failed')

# ---------- Entire program rendered in plain language ----------
render_sections_pattern = re.compile(r'    function renderSections\(\)\{.*?\n    function updateProgress\(\)', re.S)
new_render_sections = r'''    function renderSections(){
      const finisher=[
        {title:"Берпи на месте",dose:"По уровню",description:"Опустись в планку, верни ноги к рукам и выпрямись.",technique:["Поставь ладони рядом со стопами.","Перейди в устойчивую планку.","Верни стопы к рукам и полностью выпрямись."]},
        {title:"Строгие отжимания",dose:"По уровню",description:"Отжимания с прямым корпусом и полной амплитудой.",technique:["Не опускай и не поднимай таз отдельно.","Опусти грудь почти до пола.","Полностью выпрями руки вверху."]},
        {title:"Приседания",dose:"По уровню",description:"Ровные приседания в контролируемом темпе.",technique:["Не отрывай пятки.","Колени направляй по линии носков.","Вверху полностью выпрями ноги и таз."]},
        {title:"Перекрёстный альпинист",dose:"По уровню",description:"Из планки направляй колено к противоположному локтю.",technique:["Держи плечи над кистями.","Не поднимай таз высоко.","Одно подтягивание колена считается одним движением."]}
      ];

      const warmupHow=`<div class="section-how"><strong>Как выполнять разминку</strong><p>Сделай первое упражнение один раз, затем сразу переходи ко второму. Пройди весь список сверху вниз без повторения.</p></div>`;
      const strengthHow=`<div class="section-how"><strong>Как выполнять силовую часть</strong><p>Начни с первого упражнения. Сделай один подход, отдохни ${selectedLevel.strengthRoundRest} секунд и повтори. Выполни всего ${approachText(selectedLevel.strengthRounds)}. Затем переходи ко второму упражнению и работай так же.</p></div>`;
      const cardioHow=`<div class="section-how"><strong>Как выполнять кардио по минутам</strong><p>Запусти обычный таймер. В начале первой минуты сделай упражнение №1. Если закончил раньше — отдыхай до начала следующей минуты. На второй минуте выполни упражнение №2, затем №3 и №4. После четвёртой минуты начни список сначала.</p></div>`;
      const controlHow=`<div class="section-how"><strong>Как выполнять упражнения на корпус</strong><p>Сделай все подходы первого упражнения, отдыхая указанное время. Затем переходи к следующему. Не продолжай подход, если перестал удерживать правильное положение тела.</p></div>`;
      const finisherHow=`<div class="section-how"><strong>Как выполнять финальную часть</strong><p>Сделай берпи, затем отжимания, приседания и альпинист. Это один круг. Сразу начинай следующий круг и продолжай ${selectedLevel.finisherMinutes} минут. Отдыхай только тогда, когда уже не можешь сохранить технику.</p></div>`;
      const cooldownHow=`<div class="section-how"><strong>Как выполнять заминку</strong><p>Выполни каждое упражнение один раз сверху вниз. Не торопись и постепенно успокаивай дыхание.</p></div>`;

      programSections.innerHTML=[
        section("warmup","01","Разминка","Один раз пройти весь список","Подготовь суставы, мышцы и дыхание к основной нагрузке.",warmupHow+`<div class="exercise-list">${cards(warmupExercises,"warmup")}</div>`,true),
        section("strength","02","Силовая часть",`${approachText(selectedLevel.strengthRounds)} каждого упражнения`,`Сначала полностью закончи одно упражнение, затем переходи к следующему.`,strengthHow+`<div class="exercise-list">${cards(strengthExercises,"strength")}</div>`),
        section("engine","03","Кардио по минутам",`${selectedLevel.engineRounds*4} минут всего`,`Четыре упражнения выполняются по одному в начале каждой новой минуты.`,cardioHow+`<div class="section-protocol"><div class="protocol-cell"><small>Один блок</small><strong>4 минуты</strong></div><div class="protocol-cell"><small>Повторить блок</small><strong>${blockText(selectedLevel.engineRounds)}</strong></div><div class="protocol-cell"><small>Общее время</small><strong>${selectedLevel.engineRounds*4} минут</strong></div></div><div class="mini-grid"><article class="mini-card"><small>Первая минута</small><strong>Берпи</strong><span>${selectedLevel.burpees}</span><em>Закончил — отдыхай до второй минуты</em></article><article class="mini-card"><small>Вторая минута</small><strong>Альпинист</strong><span>${selectedLevel.climbers}</span><em>Каждое колено считается отдельно</em></article><article class="mini-card"><small>Третья минута</small><strong>Выходы руками в планку</strong><span>${selectedLevel.walkouts}</span><em>Один выход и возврат = одно повторение</em></article><article class="mini-card"><small>Четвёртая минута</small><strong>Прямые удары руками</strong><span>${selectedLevel.punches}</span><em>Каждый удар считается отдельно</em></article></div>`),
        section("control","04","Корпус и устойчивость",`${approachText(selectedLevel.controlRounds)} каждого упражнения`,`Здесь важнее правильное положение тела, а не скорость.`,controlHow+`<div class="exercise-list">${cards(controlExercises,"control")}</div>`),
        section("finisher","05","Финальная часть",`${selectedLevel.finisherMinutes} минут подряд`,`Четыре упражнения образуют один круг. Повторяй круги до окончания времени.`,finisherHow+`<div class="exercise-list">${cards(finisher,"finisher")}</div>`),
        section("cooldown","06","Заминка","Один раз пройти весь список","Постепенно снизь пульс и восстанови дыхание.",cooldownHow+`<div class="exercise-list">${cards(cooldownExercises,"cooldown")}</div>`)
      ].join("");

      programSections.querySelectorAll(".section-toggle").forEach(button=>button.addEventListener("click",()=>{
        const sectionElement=button.closest(".program-section");
        sectionElement.classList.toggle("open");
        button.setAttribute("aria-expanded",String(sectionElement.classList.contains("open")));
      }));
      programSections.querySelectorAll(".check-btn").forEach(button=>button.addEventListener("click",event=>{
        event.stopPropagation();
        const id=button.dataset.checkId;
        const card=button.closest(".exercise-card");
        completedExercises.has(id)?completedExercises.delete(id):completedExercises.add(id);
        card.classList.toggle("completed",completedExercises.has(id));
        updateProgress();
      }));
    }
    function updateProgress('''
text, count = render_sections_pattern.subn(new_render_sections, text, count=1)
if count != 1:
    raise SystemExit('renderSections replacement failed')

# ---------- Timer labels in JS ----------
text = text.replace(
    '$("timerPhase").textContent=timerPhaseState==="work"?"Работа":timerPhaseState==="rest"?"Восстановление":"Завершено";',
    '$("timerPhase").textContent=timerPhaseState==="work"?"Делай упражнение":timerPhaseState==="rest"?"Отдыхай":"Готово";',
    1,
)
text = text.replace(
    '$("timerRound").textContent=timerPhaseState==="done"?`${s.rounds} кругов выполнено`:`Круг ${currentRound} из ${s.rounds}`',
    '$("timerRound").textContent=timerPhaseState==="done"?`Выполнено подходов: ${s.rounds}`:`Подход ${currentRound} из ${s.rounds}`',
    1,
)
text = text.replace('showToast("Интервальный блок завершён")', 'showToast("Все подходы по таймеру завершены")', 1)

# Final validation: no confusing visible terminology in generated program.
required = [
    'HUMAN READABLE PROGRAM',
    'Как проходить тренировку',
    'Сколько сделать',
    'Сделай все подходы этого упражнения',
    'Кардио по минутам',
    'Делать, секунд',
    'Подход ${currentRound} из ${s.rounds}'
]
for marker in required:
    if marker not in text:
        raise SystemExit(f'Missing marker: {marker}')

for forbidden in ['Лимит:', 'EMOM ·', '>Работа</small>', '>Круги</label>']:
    if forbidden in text:
        raise SystemExit(f'Old confusing wording remains: {forbidden}')

path.write_text(text, encoding='utf-8')
