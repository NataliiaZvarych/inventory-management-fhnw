from nicegui import ui
from app.views.dashboard import dashboard_page

@ui.page('/')
def main_redirect():
    ui.navigate.to('/dashboard')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host="127.0.0.1",
        port=8080,
        reload=True
    )
