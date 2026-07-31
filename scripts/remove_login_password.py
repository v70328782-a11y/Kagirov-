from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Open the application immediately without the authorization lock.
text = text.replace('<body class="auth-locked">', '<body>', 1)

# Permanently remove the login screen from layout, even if old cached JS runs.
override = '''\n\n    /* PASSWORD SCREEN REMOVED */\n    .auth-screen { display: none !important; }\n    body.auth-locked { overflow: auto !important; }\n    body.auth-locked .app,\n    body.auth-locked .bottom-nav {\n      opacity: 1 !important;\n      visibility: visible !important;\n      pointer-events: auto !important;\n      filter: none !important;\n    }\n'''

if '/* PASSWORD SCREEN REMOVED */' not in text:
    text = text.replace('\n  </style>', override + '\n  </style>', 1)

path.write_text(text, encoding='utf-8')
