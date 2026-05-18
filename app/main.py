from nicegui import ui

import app.views.login
import app.views.dashboard

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host="127.0.0.1",
        port=8080,
        reload=True
    )