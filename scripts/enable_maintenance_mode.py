from pathlib import Path

# Triggered maintenance lock deployment.
p = Path('index.html')
s = p.read_text(encoding='utf-8')

marker = '/* KAGIROV MAINTENANCE MODE */'
if marker not in s:
    css = r'''

    /* KAGIROV MAINTENANCE MODE */
    body.maintenance-locked{overflow:hidden!important}
    body.maintenance-locked > *:not(#maintenanceScreen){
      pointer-events:none!important;
      user-select:none!important;
    }
    #maintenanceScreen{
      position:fixed;
      inset:0;
      z-index:999999;
      min-height:100svh;
      display:grid;
      place-items:center;
      padding:max(24px,env(safe-area-inset-top)) 18px max(24px,env(safe-area-inset-bottom));
      color:#6d5139;
      background:
        radial-gradient(circle at 12% 0%,rgba(255,255,255,.52),transparent 34%),
        radial-gradient(circle at 100% 10%,rgba(255,247,236,.30),transparent 34%),
        linear-gradient(160deg,#e2ceb4 0%,#d4bb9b 50%,#dec8ac 100%);
    }
    .maintenance-card{
      width:min(520px,100%);
      padding:30px 26px;
      border:1px solid rgba(103,77,52,.16);
      border-radius:30px;
      text-align:center;
      background:rgba(255,253,249,.97);
      box-shadow:0 30px 90px rgba(91,61,35,.20),inset 0 1px 0 rgba(255,255,255,.85);
      backdrop-filter:blur(22px) saturate(120%);
    }
    .maintenance-icon{
      width:68px;height:68px;margin:0 auto 20px;
      display:grid;place-items:center;
      border-radius:22px;
      color:#fffdf9;
      background:linear-gradient(135deg,#76543b,#927054);
      box-shadow:0 13px 30px rgba(101,70,44,.20);
      font-size:31px;font-weight:950;
    }
    .maintenance-kicker{
      color:#9a7c61;font-size:10px;font-weight:900;letter-spacing:.13em;text-transform:uppercase;
    }
    .maintenance-card h1{
      margin:8px 0 10px;
      color:#664a33;
      font-size:clamp(34px,9vw,50px);
      line-height:1;
      letter-spacing:-.06em;
    }
    .maintenance-card p{
      margin:0;
      color:#8d7058;
      font-size:14px;
      line-height:1.65;
    }
    .maintenance-time{
      margin-top:20px;
      padding:16px;
      border:1px solid rgba(103,77,52,.13);
      border-radius:17px;
      background:#f6ecdf;
    }
    .maintenance-time small{display:block;color:#9a7c61;font-size:10px;font-weight:850;text-transform:uppercase;letter-spacing:.08em}
    .maintenance-time strong{display:block;margin-top:5px;color:#6b4d35;font-size:25px;letter-spacing:-.04em}
    .maintenance-note{margin-top:15px!important;color:#a1866f!important;font-size:11px!important}
'''
    s = s.replace('\n  </style>', css + '\n  </style>', 1)

if 'id="maintenanceScreen"' not in s:
    overlay = '''\n  <section id="maintenanceScreen" role="status" aria-live="polite">\n    <div class="maintenance-card">\n      <div class="maintenance-icon">↻</div>\n      <div class="maintenance-kicker">KAGIROV · технические работы</div>\n      <h1>Идёт обновление</h1>\n      <p>Сайт временно недоступен. Сейчас устанавливается крупное обновление программы и интерфейса. Доступ будет открыт после завершения работ.</p>\n      <div class="maintenance-time">\n        <small>Примерное время обновления</small>\n        <strong>2 часа 30 минут</strong>\n      </div>\n      <p class="maintenance-note">Пожалуйста, зайдите позже.</p>\n    </div>\n  </section>\n'''
    s = s.replace('<body>', '<body class="maintenance-locked">' + overlay, 1)
else:
    s = s.replace('<body>', '<body class="maintenance-locked">', 1)

s = s.replace('<body class="auth-locked">', '<body class="maintenance-locked">', 1)

required = ['KAGIROV MAINTENANCE MODE','id="maintenanceScreen"','2 часа 30 минут','class="maintenance-locked"']
for item in required:
    if item not in s:
        raise SystemExit(f'Missing required marker: {item}')

p.write_text(s, encoding='utf-8')
