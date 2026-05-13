from nicegui import ui

from app.views import *


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host="127.0.0.1",
        port=8080,
        reload=True
    )
