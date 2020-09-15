from .resources import (
    AuthorizationSmsPost
)


def init_routes_app_v1(app):
    app.router.add_post('/v1.0/authorization/sms', AuthorizationSmsPost)
