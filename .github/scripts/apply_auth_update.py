from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")

AUTH_CSS = r'''

    /* =========================================================
       PASSWORD ACCESS SCREEN
       ========================================================= */
    body.auth-locked {
      overflow: hidden;
    }

    body.auth-locked > .app,
    body.auth-locked > .bottom-nav,
    body.auth-locked > .sheet-backdrop,
    body.auth-locked > .timer-widget,
    body.auth-locked > .toast {
      visibility: hidden;
      pointer-events: none;
      user-select: none;
    }

    .auth-screen {
      position: fixed;
      inset: 0;
      z-index: 1000;
      min-height: 100svh;
      padding:
        max(24px, env(safe-area-inset-top))
        18px
        max(24px, env(safe-area-inset-bottom));
      display: grid;
      place-items: center;
      overflow-y: auto;
      background:
        radial-gradient(circle at 10% 0%, rgba(255,255,255,.42), transparent 31%),
        radial-gradient(circle at 100% 10%, rgba(255,246,233,.32), transparent 34%),
        linear-gradient(160deg, #e2ceb4 0%, #d4bb9b 48%, #dec8ac 100%);
      opacity: 1;
      visibility: visible;
      transition: opacity .28s ease, visibility .28s ease;
    }

    .auth-screen.hidden {
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
    }

    .auth-card {
      width: min(430px, 100%);
      padding: 30px;
      border: 1px solid rgba(103,77,52,.16);
      border-radius: 30px;
      color: #6d5139;
      background: rgba(255,253,249,.96);
      box-shadow:
        0 30px 90px rgba(91,61,35,.20),
        inset 0 1px 0 rgba(255,255,255,.85);
      backdrop-filter: blur(22px) saturate(120%);
    }

    .auth-logo {
      width: 62px;
      height: 62px;
      display: grid;
      place-items: center;
      border: 1px solid rgba(103,77,52,.15);
      border-radius: 21px;
      color: #6d5139;
      background: #f3e5d6;
      box-shadow: 0 13px 28px rgba(91,61,35,.11);
      font-size: 32px;
      font-weight: 950;
      line-height: 1;
      letter-spacing: -.08em;
      text-transform: lowercase;
    }

    .auth-kicker {
      margin-top: 24px;
      color: #9a7c61;
      font-size: 10px;
      font-weight: 900;
      letter-spacing: .12em;
      text-transform: uppercase;
    }

    .auth-card h1 {
      margin: 7px 0 8px;
      color: #664a33;
      font-size: clamp(36px, 10vw, 52px);
      line-height: .98;
      letter-spacing: -.065em;
    }

    .auth-card > p {
      margin: 0 0 23px;
      color: #987b62;
      font-size: 13px;
      line-height: 1.58;
    }

    .auth-form {
      display: grid;
      gap: 10px;
    }

    .auth-label {
      color: #8d7058;
      font-size: 11px;
      font-weight: 800;
    }

    .auth-input-wrap {
      display: grid;
      grid-template-columns: minmax(0,1fr) auto;
      align-items: center;
      min-height: 54px;
      overflow: hidden;
      border: 1px solid rgba(103,77,52,.19);
      border-radius: 16px;
      background: #fff;
      transition: border-color .16s ease, box-shadow .16s ease;
    }

    .auth-input-wrap:focus-within {
      border-color: rgba(121,88,62,.52);
      box-shadow: 0 0 0 4px rgba(121,88,62,.09);
    }

    .auth-input {
      width: 100%;
      min-width: 0;
      height: 52px;
      padding: 0 14px;
      border: 0;
      outline: 0;
      color: #654a34;
      background: transparent;
      font-size: 16px;
      font-weight: 750;
      letter-spacing: .01em;
    }

    .auth-input::placeholder {
      color: #b9a38d;
      font-weight: 600;
    }

    .auth-toggle {
      height: 38px;
      margin-right: 7px;
      padding: 0 11px;
      border: 1px solid rgba(103,77,52,.13);
      border-radius: 11px;
      color: #806249;
      background: #f5eadf;
      font-size: 10px;
      font-weight: 900;
      cursor: pointer;
    }

    .auth-error {
      min-height: 17px;
      color: #a45d50;
      font-size: 11px;
      font-weight: 750;
    }

    .auth-submit {
      min-height: 51px;
      border: 0;
      border-radius: 16px;
      color: #fffdf9;
      background: linear-gradient(135deg, #76543b, #927054);
      box-shadow: 0 13px 27px rgba(101,70,44,.19);
      font-weight: 900;
      cursor: pointer;
      transition: transform .16s ease, filter .16s ease;
    }

    .auth-submit:active {
      transform: scale(.978);
    }

    .auth-submit:hover {
      filter: brightness(1.04);
    }

    .auth-local-note {
      margin-top: 18px;
      padding: 12px 13px;
      border: 1px solid rgba(103,77,52,.12);
      border-radius: 14px;
      color: #92755d;
      background: #f8eee3;
      font-size: 10px;
      line-height: 1.5;
      text-align: center;
    }

    .auth-card.shake {
      animation: authShake .36s ease;
    }

    @keyframes authShake {
      0%, 100% { transform: translateX(0); }
      25% { transform: translateX(-7px); }
      50% { transform: translateX(7px); }
      75% { transform: translateX(-4px); }
    }

    @media (max-width: 480px) {
      .auth-screen {
        align-items: center;
        padding-left: 14px;
        padding-right: 14px;
      }

      .auth-card {
        padding: 24px 20px;
        border-radius: 25px;
      }
    }
'''

AUTH_HTML = r'''
  <div class="auth-screen" id="authScreen" role="dialog" aria-modal="true" aria-labelledby="authTitle">
    <div class="auth-card" id="authCard">
      <div class="auth-logo" aria-hidden="true">k</div>
      <div class="auth-kicker">Личный доступ</div>
      <h1 id="authTitle">kagirov</h1>
      <p>Введите пароль, чтобы открыть программу тренировок, прогресс и спортивный калькулятор.</p>

      <form class="auth-form" id="authForm" autocomplete="off" novalidate>
        <label class="auth-label" for="authPassword">Пароль</label>

        <div class="auth-input-wrap">
          <input
            class="auth-input"
            id="authPassword"
            name="kagirov-password"
            type="password"
            inputmode="text"
            autocomplete="off"
            autocapitalize="none"
            autocorrect="off"
            spellcheck="false"
            placeholder="Введите пароль"
            aria-describedby="authError"
            required
          >

          <button class="auth-toggle" id="authToggle" type="button" aria-label="Показать пароль">
            Показать
          </button>
        </div>

        <div class="auth-error" id="authError" role="alert" aria-live="polite"></div>

        <button class="auth-submit" type="submit">
          Открыть тренировки
        </button>
      </form>

      <div class="auth-local-note">
        История и выполненные тренировки хранятся только в браузере этого устройства и не передаются на другие устройства.
      </div>
    </div>
  </div>
'''

DEVICE_AND_AUTH_SCRIPTS = r'''
  <script>
    (() => {
      "use strict";

      const DEVICE_ID_KEY = "kagirov_device_id_v1";
      let deviceId = "";

      try {
        deviceId = localStorage.getItem(DEVICE_ID_KEY) || "";

        if (!deviceId) {
          deviceId = (
            window.crypto && typeof window.crypto.randomUUID === "function"
              ? window.crypto.randomUUID()
              : `${Date.now()}-${Math.random().toString(36).slice(2)}-${Math.random().toString(36).slice(2)}`
          );

          localStorage.setItem(DEVICE_ID_KEY, deviceId);
        }
      } catch {
        deviceId = "device-local-fallback";
      }

      window.KAGIROV_DEVICE_ID = deviceId;
    })();
  </script>

  <script>
    (() => {
      "use strict";

      const ACCESS_PASSWORD = "Kagirov112200@";
      const screen = document.getElementById("authScreen");
      const card = document.getElementById("authCard");
      const form = document.getElementById("authForm");
      const passwordInput = document.getElementById("authPassword");
      const toggleButton = document.getElementById("authToggle");
      const error = document.getElementById("authError");

      function unlockApplication() {
        document.body.classList.remove("auth-locked");
        screen.classList.add("hidden");
        screen.setAttribute("aria-hidden", "true");
        passwordInput.value = "";
        error.textContent = "";

        window.setTimeout(() => {
          document.getElementById("continueBtn")?.focus({ preventScroll: true });
        }, 300);
      }

      function rejectPassword() {
        error.textContent = "Неверный пароль. Проверьте заглавные буквы и символы.";
        passwordInput.setAttribute("aria-invalid", "true");
        passwordInput.select();

        card.classList.remove("shake");
        void card.offsetWidth;
        card.classList.add("shake");

        if (typeof navigator.vibrate === "function") {
          navigator.vibrate(90);
        }
      }

      form.addEventListener("submit", event => {
        event.preventDefault();

        if (passwordInput.value === ACCESS_PASSWORD) {
          passwordInput.removeAttribute("aria-invalid");
          unlockApplication();
        } else {
          rejectPassword();
        }
      });

      passwordInput.addEventListener("input", () => {
        error.textContent = "";
        passwordInput.removeAttribute("aria-invalid");
      });

      toggleButton.addEventListener("click", () => {
        const showPassword = passwordInput.type === "password";
        passwordInput.type = showPassword ? "text" : "password";
        toggleButton.textContent = showPassword ? "Скрыть" : "Показать";
        toggleButton.setAttribute(
          "aria-label",
          showPassword ? "Скрыть пароль" : "Показать пароль"
        );
        passwordInput.focus();
      });

      window.setTimeout(() => passwordInput.focus(), 120);
    })();
  </script>
'''

if "PASSWORD ACCESS SCREEN" not in html:
    html = html.replace("\n  </style>", AUTH_CSS + "\n\n  </style>", 1)

if '<body class="auth-locked">' not in html:
    if "<body>" not in html:
        raise SystemExit("Could not find <body> marker")
    html = html.replace("<body>", '<body class="auth-locked">\n\n' + AUTH_HTML, 1)

old_main_marker = '''  <script>\n    (() => {\n      "use strict";\n\n      const STORAGE_KEY = "kagirov_training_clean_v1";'''
new_main_marker = DEVICE_AND_AUTH_SCRIPTS + '''\n\n  <script>\n    (() => {\n      "use strict";\n\n      const STORAGE_KEY = `kagirov_training_v2_${window.KAGIROV_DEVICE_ID}`;'''

if "kagirov_training_v2_${window.KAGIROV_DEVICE_ID}" not in html:
    if old_main_marker not in html:
        raise SystemExit("Could not find main script marker")
    html = html.replace(old_main_marker, new_main_marker, 1)

html = html.replace(
    'const K="kagirov_sport_calculator_clean_v1";',
    'const K=`kagirov_sport_calculator_v2_${window.KAGIROV_DEVICE_ID}`;',
    1,
)

path.write_text(html, encoding="utf-8")
print("index.html updated with password access and device-scoped storage")
