
# main_app.py
from web_ui import WebUI

if __name__ == "__main__":
    ui = WebUI()
    ui.load_data()
    ui.analyze_data()
    ui.compute_trust_score()
    ui.render_page()
