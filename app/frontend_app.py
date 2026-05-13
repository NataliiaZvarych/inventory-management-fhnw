from nicegui import ui

# Import pages so their @ui.page decorators are registered before ui.run()
from app.views import dashboard_page, products_page  # noqa: F401
from app.views.categories import categories_page  # noqa: F401
from app.views.locations import locations_page  # noqa: F401
from app.views.login import login_page  # noqa: F401
from app.views.movements import movements_page  # noqa: F401
from app.views.users import users_page  # noqa: F401


ui.colors(
	primary="#6fa1d8",
	secondary="#2f3e4e",
	accent="#f2b134",
	positive="#3bb273",
)

ui.add_head_html(
	"""
<style>
    body {
        background: #f5f7fb;
    }
</style>
"""
)


def run() -> None:
	ui.run(title="Inventory Management", reload=False, show=False)


if __name__ == "__main__":
	run()
