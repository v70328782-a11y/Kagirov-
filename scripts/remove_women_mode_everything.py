from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove the embedded BODY MODE view.
s = re.sub(
    r'\n\s*<section class="view workout-platform-view" data-view="women">.*?</section>\s*\n',
    '\n',
    s,
    flags=re.S,
)

# Remove the women navigation button.
s = re.sub(
    r'\n\s*<button class="nav-btn" data-view-target="women">.*?</button>\s*',
    '\n',
    s,
    flags=re.S,
)

# Remove any leftover home-entry card if present.
s = re.sub(
    r'\n\s*<article class="women-entry-card" id="womenHomeEntry">.*?</article>\s*\n',
    '\n',
    s,
    flags=re.S,
)

# Restore bottom navigation sizing for five sections.
s = s.replace('width: min(780px, calc(100% - 22px));', 'width: min(690px, calc(100% - 22px));')
s = s.replace('grid-template-columns: repeat(6,1fr);', 'grid-template-columns: repeat(5,1fr);')

# Remove women-only CSS blocks/rules that may remain from earlier integration.
s = re.sub(r'\n\s*/\*\s*(?:WOMEN|BODY MODE).*?\*/.*?(?=\n\s*/\*|\n\s*</style>)', '\n', s, flags=re.S | re.I)
s = re.sub(r'\n\s*\.women-entry-card\s*\{.*?\}', '', s, flags=re.S)
s = re.sub(r'\n\s*\.women-entry-card[^\{]*\{.*?\}', '', s, flags=re.S)
s = re.sub(r'\n\s*\.women-entry-badge\s*\{.*?\}', '', s, flags=re.S)
s = re.sub(r'\n\s*\.women-platform-frame\s*\{.*?\}', '', s, flags=re.S)

# Remove any remaining direct references to BODY MODE / women platform that are safe standalone leftovers.
s = re.sub(r'^.*women-body-mode\.html.*\n?', '', s, flags=re.M | re.I)
s = re.sub(r'^.*data-view-target="women".*\n?', '', s, flags=re.M)
s = re.sub(r'^.*data-view="women".*\n?', '', s, flags=re.M)

p.write_text(s, encoding='utf-8')

# Remove dedicated women-mode files and old integration helpers if they exist.
for path in [
    Path('women-body-mode.html'),
    Path('scripts/remove_women_home_banner.py'),
    Path('scripts/integrate_women_body_mode.py'),
    Path('.github/workflows/integrate-women-body-mode.yml'),
]:
    if path.exists():
        path.unlink()

print('Women mode and related site integration removed.')
