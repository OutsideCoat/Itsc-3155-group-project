from . import orders, order_details, sandwiches, promotions, reports, menu_items


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(sandwiches.router)
    app.include_router(promotions.router)
    app.include_router(reports.router)
    app.include_router(menu_items.router)
