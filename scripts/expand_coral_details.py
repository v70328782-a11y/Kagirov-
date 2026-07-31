from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = '''<article class="coral-main" id="coralClubBlock"><div class="coral-tag">Coral Club</div><h3>Поддержка активного образа жизни</h3><p>Продукты Coral Club для повседневного рациона, водного баланса и восстановления. Добавки не заменяют полноценное питание и медицинское лечение.</p><div class="coral-grid"><div class="coral-item"><strong>Водный баланс</strong><span>Поддержка удобного питьевого режима.</span></div><div class="coral-item"><strong>Рацион</strong><span>Продукты для дополнения ежедневного питания.</span></div><div class="coral-item"><strong>Консультация</strong><span>Связь через WhatsApp по ассортименту.</span></div></div><div class="coral-links"><a class="coral-reg" href="https://coral.club/8100919.html" target="_blank" rel="noopener">Зарегистрироваться</a><a class="coral-wa" href="https://wa.me/79640741621" target="_blank" rel="noopener">Написать в WhatsApp</a></div><div class="coral-phone">WhatsApp: +7 964 074 16 21</div></article>'''

new = '''<article class="coral-main" id="coralClubBlock">
  <div class="coral-tag">Coral Club</div>
  <h3>Поддержка восстановления, набора массы и активного образа жизни</h3>
  <p>Подбор продуктов Coral Club под цели тренировок, повседневного рациона, водного баланса, контроля калорийности и удобного добора питательных веществ.</p>

  <div class="coral-grid">
    <div class="coral-item"><strong>Восстановление</strong><span>Решения для поддержки рациона после тренировок и в периоды высокой нагрузки.</span></div>
    <div class="coral-item"><strong>Набор массы</strong><span>Удобные продукты для повышения калорийности и добора белка в течение дня.</span></div>
    <div class="coral-item"><strong>Водный баланс</strong><span>Продукты для более удобного питьевого режима дома, на работе и во время тренировок.</span></div>
  </div>

  <button class="coral-expand" id="coralExpand" type="button" aria-expanded="false" aria-controls="coralDetails">Развернуть подробнее</button>

  <div class="coral-details" id="coralDetails" hidden>
    <div class="coral-detail-grid">
      <div class="coral-detail-card"><strong>Для восстановления после нагрузок</strong><p>Подбор продуктов, которые удобно встроить в послетренировочный рацион: источники белка, напитки, продукты для восполнения энергии и ежедневного питания.</p></div>
      <div class="coral-detail-card"><strong>Для набора веса и мышечной массы</strong><p>Подходящие варианты для тех, кому сложно добирать калории обычной едой: дополнительные приёмы питания, белковые продукты и удобные решения для плотного рациона.</p></div>
      <div class="coral-detail-card"><strong>Для контроля питания</strong><p>Продукты, которые помогают сделать рацион более организованным: понятные порции, удобный формат и возможность заранее планировать питание на день.</p></div>
      <div class="coral-detail-card"><strong>Для активного дня</strong><p>Решения для тренировок, работы, учёбы и поездок, когда важно не пропускать питание и поддерживать стабильный режим.</p></div>
      <div class="coral-detail-card"><strong>Для питьевого режима</strong><p>Продукты и аксессуары Coral Club, которые помогают сделать регулярное употребление воды более удобной привычкой.</p></div>
      <div class="coral-detail-card"><strong>Персональный подбор</strong><p>Можно написать в WhatsApp, описать цель, режим тренировок и особенности рациона, чтобы получить помощь с выбором подходящих продуктов.</p></div>
    </div>
    <div class="coral-detail-note">Результат зависит от общего рациона, тренировочной программы, режима сна и регулярности применения.</div>
  </div>

  <div class="coral-links"><a class="coral-reg" href="https://coral.club/8100919.html" target="_blank" rel="noopener">Зарегистрироваться</a><a class="coral-wa" href="https://wa.me/79640741621" target="_blank" rel="noopener">Написать в WhatsApp</a></div>
  <div class="coral-phone">WhatsApp: +7 964 074 16 21</div>
</article>'''

if old not in s:
    raise SystemExit('Coral block not found')
s = s.replace(old, new, 1)

css = '''
.coral-expand{width:100%;min-height:44px;margin-top:15px;border:1px solid rgba(90,130,65,.18);border-radius:14px;background:#eef6e9;color:#4d7139;font-weight:900;cursor:pointer}.coral-expand:active{transform:scale(.99)}.coral-details{margin-top:13px}.coral-detail-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}.coral-detail-card{padding:14px;border-radius:16px;background:rgba(255,255,255,.82);border:1px solid rgba(90,130,65,.12)}.coral-detail-card strong{display:block;font-size:12px;color:#4e392c}.coral-detail-card p{margin:6px 0 0;font-size:11px;line-height:1.55;color:#7c6958}.coral-detail-note{margin-top:10px;padding:11px 13px;border-radius:13px;background:rgba(102,141,77,.08);color:#6e5b4c;font-size:10px;line-height:1.5}@media(max-width:650px){.coral-detail-grid{grid-template-columns:1fr}}
'''
s = s.replace('</style>', css + '</style>', 1)

js = '''<script>(()=>{const btn=document.getElementById("coralExpand"),details=document.getElementById("coralDetails");btn?.addEventListener("click",()=>{const open=btn.getAttribute("aria-expanded")==="true";btn.setAttribute("aria-expanded",String(!open));details.hidden=open;btn.textContent=open?"Развернуть подробнее":"Свернуть подробности"})})();</script>'''
s = s.replace('</body>', js + '</body>', 1)

p.write_text(s, encoding='utf-8')
