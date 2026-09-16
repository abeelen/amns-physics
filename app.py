import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent))
st.set_page_config(
    page_title="AMNS-Physique",
    page_icon="👋",
)

PAGES_DIR = Path(__file__).resolve().parent / "pages"
# Sections affichées dans un ordre et avec un libellé propre, indépendants du nom du dossier
SECTION_TITLES = {
    "ondes": "Ondes",
    "optique_geometrique": "Optique Géométrique",
}


def discover_navigation(pages_dir: Path) -> dict[str, list]:
    nav: dict[str, list] = {}
    for folder in sorted(p for p in pages_dir.iterdir() if p.is_dir()):
        section = SECTION_TITLES.get(folder.name, folder.name.replace("_", " ").title())
        # st.Page infère titre/icône depuis le nom de fichier "<ordre>_<icone>_<nom>.py"
        nav[section] = [st.Page(str(file)) for file in sorted(folder.glob("*.py"))]
    return nav


accueil = st.Page(str(PAGES_DIR / "accueil.py"), title="Accueil", icon="👋", default=True)
navigation = {"": [accueil], **discover_navigation(PAGES_DIR)}

pg = st.navigation(navigation)
pg.run()
