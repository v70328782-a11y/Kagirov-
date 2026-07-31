from pathlib import Path
import re

path = Path('home-workout.html')
text = path.read_text(encoding='utf-8')

css_marker = '/* FINAL EXERCISE PRESCRIPTIONS */'
css = r'''

    /* FINAL EXERCISE PRESCRIPTIONS */
    .exercise-prescription{
      display:flex;
      flex-wrap:wrap;
      gap:6px;
      margin-top:9px;
    }
    .prescription-chip{
      display:inline-flex;
      align-items:center;
      min-height:27px;
      padding:6px 9px;
      border:1px solid rgba(101,67,47,.1);
      border-radius:9px;
      color:var(--muted);
      background:var(--card-2);
      font-size:10px;
      font-weight:800;
      line-height:1.25;
    }
    .prescription-chip.primary{
      border-color:transparent;
      color:#fff;
      background:var(--selected);
    }
    .section-protocol{
      display:grid;
      grid-template-columns:repeat(3,minmax(0,1fr));
      gap:7px;
      margin:0 0 12px;
    }
    .protocol-cell{
      min-height:62px;
      padding:10px;
      border:1px solid var(--line);
      border-radius:13px;
      background:#fff;
    }
    .protocol-cell small{
      display:block;
      color:var(--soft);
      font-size:8px;
      font-weight:850;
      letter-spacing:.07em;
      text-transform:uppercase;
    }
    .protocol-cell strong{
      display:block;
      margin-top:6px;
      color:var(--selected-dark);
      font-size:11px;
      line-height:1.35;
    }
    .mini-card em{
      display:block;
      margin-top:6px;
      color:var(--muted);
      font-size:9px;
      font-style:normal;
      font-weight:750;
      line-height:1.35;
    }
    @media(max-width:410px){
      .section-protocol{grid-template-columns:1fr}
      .protocol-cell{min-height:0}
    }
'''
if css_marker not in text:
    text = text.replace('\n  </style>', css + '\n  </style>', 1)

prescription_marker = 'const exercisePrescriptions='
prescriptions = r'''

    const exercisePrescriptions={
      strength:[
        {calibration:"8 повторений",vanguard:"12 повторений",assault:"16 повторений",absolute:"20 повторений"},
        {calibration:"12 повторений",vanguard:"16 повторений",assault:"20 повторений",absolute:"25 повторений"},
        {calibration:"6 повторений",vanguard:"8 повторений",assault:"12 повторений",absolute:"15 повторений"},
        {calibration:"8 на каждую ногу",vanguard:"10 на каждую ногу",assault:"12 на каждую ногу",absolute:"15 на каждую ногу"},
        {calibration:"12 повторений",vanguard:"15 повторений",assault:"18 повторений",absolute:"20 повторений"},
        {calibration:"20 секунд",vanguard:"30 секунд",assault:"40 секунд",absolute:"50 секунд"}
      ],
      control:[
        {calibration:"30 секунд",vanguard:"40 секунд",assault:"45 секунд",absolute:"50 секунд"},
        {calibration:"20 секунд",vanguard:"30 секунд",assault:"40 секунд",absolute:"50 секунд"},
        {calibration:"20 секунд",vanguard:"30 секунд",assault:"40 секунд",absolute:"50 секунд"},
        {calibration:"8 на каждую ногу",vanguard:"10 на каждую ногу",assault:"12 на каждую ногу",absolute:"15 на каждую ногу"},
        {calibration:"5 циклов Y–T–W",vanguard:"6 циклов Y–T–W",assault:"8 циклов Y–T–W",absolute:"10 циклов Y–T–W"}
      ],
      finisher:[
        {calibration:"3 повторения",vanguard:"5 повторений",assault:"6 повторений",absolute:"8 повторений"},
        {calibration:"5 повторений",vanguard:"8 повторений",assault:"10 повторений",absolute:"12 повторений"},
        {calibration:"8 повторений",vanguard:"12 повторений",assault:"15 повторений",absolute:"20 повторений"},
        {calibration:"10 движений",vanguard:"16 движений",assault:"20 движений",absolute:"24 движения"}
      ]
    };

    function roundWord(value){
      const n=Math.abs(Number(value))%100;
      const n1=n%10;
      if(n>10&&n<20)return "кругов";
      if(n1===1)return "круг";
      if(n1>=2&&n1<=4)return "круга";
      return "кругов";
    }

    function prescriptionFor(sectionId,index,exercise){
      const levelId=selectedLevel.id;
      if(sectionId==="strength"){
        return{
          primary:`${selectedLevel.strengthRounds} ${roundWord(selectedLevel.strengthRounds)} × ${exercisePrescriptions.strength[index][levelId]}`,
          chips:[`Лимит: ${selectedLevel.work} сек`,`Отдых: ${selectedLevel.rest} сек`,`После круга: ${selectedLevel.strengthRoundRest} сек`]
        };
      }
      if(sectionId==="control"){
        return{
          primary:`${selectedLevel.controlRounds} ${roundWord(selectedLevel.controlRounds)} × ${exercisePrescriptions.control[index][levelId]}`,
          chips:[`Лимит: ${selectedLevel.work} сек`,`Отдых: ${selectedLevel.rest} сек`,`Техника важнее темпа`]
        };
      }
      if(sectionId==="finisher"){
        return{
          primary:`В каждом круге: ${exercisePrescriptions.finisher[index][levelId]}`,
          chips:[`${selectedLevel.finisherMinutes} мин максимум кругов`,`Без отдельного отдыха`]
        };
      }
      if(sectionId==="warmup"){
        return{primary:`1 подход × ${exercise.dose}`,chips:["Без отдельного отдыха","Спокойный темп"]};
      }
      if(sectionId==="cooldown"){
        return{primary:`1 подход × ${exercise.dose}`,chips:["Без рывков","Медленное дыхание"]};
      }
      return{primary:exercise.dose,chips:[]};
    }
'''
if prescription_marker not in text:
    cooldown_pattern = re.compile(r'(    const cooldownExercises=\[.*?\n    \];)', re.S)
    match = cooldown_pattern.search(text)
    if not match:
        raise SystemExit('cooldownExercises block not found')
    text = text[:match.end()] + prescriptions + text[match.end():]

cards_pattern = re.compile(r'    function cards\(exercises,sectionId\)\{.*?\n    function section\(', re.S)
new_cards = r'''    function cards(exercises,sectionId){
      return exercises.map((e,i)=>{
        const id=sectionId+"-"+i;
        const rx=prescriptionFor(sectionId,i,e);
        const chips=[`<span class="prescription-chip primary">${rx.primary}</span>`,...rx.chips.map(x=>`<span class="prescription-chip">${x}</span>`)].join("");
        return `<article class="exercise-card" data-exercise-id="${id}"><div class="exercise-top"><span class="exercise-number">${String(i+1).padStart(2,"0")}</span><div class="exercise-heading"><strong class="exercise-title">${e.title}</strong><div class="exercise-prescription">${chips}</div></div><button class="check-btn" data-check-id="${id}">✓</button></div><p class="exercise-description">${e.description}</p><ul class="technique-list">${e.technique.map(x=>`<li>${x}</li>`).join("")}</ul>${e.variation?`<div class="variation"><strong>Вариант:</strong> ${e.variation}</div>`:""}</article>`;
      }).join("");
    }
    function section('''
text, count = cards_pattern.subn(new_cards, text, count=1)
if count != 1:
    raise SystemExit(f'cards function replacement failed: {count}')

render_pattern = re.compile(r'    function renderSections\(\)\{.*?\n    function updateProgress\(\)', re.S)
new_render = r'''    function renderSections(){
      const finisher=[
        {title:"Берпи на месте",dose:"По уровню",description:"Контролируемый цикл без перемещения по комнате.",technique:["Ладони рядом со стопами.","Перейди в устойчивую планку.","Верни стопы к рукам и полностью выпрямись."]},
        {title:"Строгие отжимания",dose:"По уровню",description:"Полная амплитуда без провисания таза.",technique:["Корпус остаётся прямым.","Грудь опускается почти до пола.","Руки полностью выпрямляются вверху."]},
        {title:"Приседания",dose:"По уровню",description:"Быстрые, но технически чистые повторения.",technique:["Стопы полностью прижаты.","Колени идут по линии носков.","Вверху полностью разогни таз."]},
        {title:"Перекрёстный альпинист",dose:"По уровню",description:"Колено направляется к противоположному локтю.",technique:["Плечи находятся над кистями.","Таз не поднимается вверх.","Каждое касание считается одним движением."]}
      ];

      const strengthProtocol=`<div class="section-protocol"><div class="protocol-cell"><small>Круги</small><strong>${selectedLevel.strengthRounds} ${roundWord(selectedLevel.strengthRounds)}</strong></div><div class="protocol-cell"><small>Между упражнениями</small><strong>${selectedLevel.rest} секунд</strong></div><div class="protocol-cell"><small>После круга</small><strong>${selectedLevel.strengthRoundRest} секунд</strong></div></div>`;
      const controlProtocol=`<div class="section-protocol"><div class="protocol-cell"><small>Круги</small><strong>${selectedLevel.controlRounds} ${roundWord(selectedLevel.controlRounds)}</strong></div><div class="protocol-cell"><small>Между упражнениями</small><strong>${selectedLevel.rest} секунд</strong></div><div class="protocol-cell"><small>Правило</small><strong>Остановись при потере формы</strong></div></div>`;
      const finisherProtocol=`<div class="section-protocol"><div class="protocol-cell"><small>Время</small><strong>${selectedLevel.finisherMinutes} минут</strong></div><div class="protocol-cell"><small>Задача</small><strong>Максимум чистых кругов</strong></div><div class="protocol-cell"><small>Отдых</small><strong>Только по необходимости</strong></div></div>`;

      programSections.innerHTML=[
        section("warmup","01","Активация системы","1 последовательный круг · около 10 минут","Выполни каждое указанное количество один раз. Между упражнениями не отдыхай, но не ускоряй технику.",`<div class="exercise-list">${cards(warmupExercises,"warmup")}</div>`,true),
        section("strength","02","Силовая броня",`${selectedLevel.strengthRounds} ${roundWord(selectedLevel.strengthRounds)} · точные повторения`,`Сделай указанное количество. Если закончил раньше лимита ${selectedLevel.work} секунд — используй остаток времени для дыхания. Не добивай повторения ценой техники.`,strengthProtocol+`<div class="exercise-list">${cards(strengthExercises,"strength")}</div>`),
        section("engine","03","Двигатель",`EMOM · ${selectedLevel.engineRounds*4} минут`,`Каждую новую минуту начинай упражнение. Закончи указанное количество и отдыхай остаток минуты. Четырёхминутный блок повторяется ${selectedLevel.engineRounds} ${roundWord(selectedLevel.engineRounds)}.`,`<div class="section-protocol"><div class="protocol-cell"><small>Блок</small><strong>4 упражнения</strong></div><div class="protocol-cell"><small>Повторить</small><strong>${selectedLevel.engineRounds} ${roundWord(selectedLevel.engineRounds)}</strong></div><div class="protocol-cell"><small>Общее время</small><strong>${selectedLevel.engineRounds*4} минут</strong></div></div><div class="mini-grid"><article class="mini-card"><small>Минута 1</small><strong>Берпи</strong><span>${selectedLevel.burpees}</span><em>Затем отдых до конца минуты</em></article><article class="mini-card"><small>Минута 2</small><strong>Альпинист</strong><span>${selectedLevel.climbers}</span><em>Одно движение = одно колено</em></article><article class="mini-card"><small>Минута 3</small><strong>Выходы в планку</strong><span>${selectedLevel.walkouts}</span><em>Полный выход и возврат</em></article><article class="mini-card"><small>Минута 4</small><strong>Прямые удары</strong><span>${selectedLevel.punches}</span><em>Считай каждый удар отдельно</em></article></div>`),
        section("control","04","Контроль под усталостью",`${selectedLevel.controlRounds} ${roundWord(selectedLevel.controlRounds)} · корпус`,`Каждое упражнение имеет точное время или количество. Скорость не важна: останови подход, если поясница, плечи или таз теряют положение.`,controlProtocol+`<div class="exercise-list">${cards(controlExercises,"control")}</div>`),
        section("finisher","05","Последний рубеж",`${selectedLevel.finisherMinutes} минут · максимум кругов`,`Повторяй четыре упражнения по порядку. Указанные повторения относятся к каждому отдельному кругу. Записывай только полностью завершённые технически чистые круги.`,finisherProtocol+`<div class="exercise-list">${cards(finisher,"finisher")}</div>`),
        section("cooldown","06","Возвращение в контроль","1 последовательный круг · около 6 минут","Выполни каждое указанное время один раз. Не сокращай заминку даже после тяжёлого финишера.",`<div class="exercise-list">${cards(cooldownExercises,"cooldown")}</div>`)
      ].join("");

      programSections.querySelectorAll(".section-toggle").forEach(b=>b.addEventListener("click",()=>{
        const s=b.closest(".program-section");
        s.classList.toggle("open");
        b.setAttribute("aria-expanded",String(s.classList.contains("open")));
      }));
      programSections.querySelectorAll(".check-btn").forEach(b=>b.addEventListener("click",e=>{
        e.stopPropagation();
        const id=b.dataset.checkId,card=b.closest(".exercise-card");
        completedExercises.has(id)?completedExercises.delete(id):completedExercises.add(id);
        card.classList.toggle("completed",completedExercises.has(id));
        updateProgress();
      }));
    }
    function updateProgress()'''
text, count = render_pattern.subn(new_render, text, count=1)
if count != 1:
    raise SystemExit(f'renderSections replacement failed: {count}')

# Strength timer is the default timer, so explain that directly in the launch buttons.
text = text.replace('◷ Запустить интервальный таймер', '◷ Таймер силового блока', 1)

# Final integrity checks.
required = [
    css_marker,
    prescription_marker,
    '3 круга × 12 повторений',
    'Затем отдых до конца минуты',
    'В каждом круге:',
    'Таймер силового блока'
]
for item in required:
    if item not in text:
        raise SystemExit(f'Missing expected marker: {item}')

path.write_text(text, encoding='utf-8')
