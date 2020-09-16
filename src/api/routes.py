from .resources import (
    AuthorizationSmsPost,
    AuthorizationSmsCompletePost
)


def init_routes_app_v1(app):
    app.router.add_post('/v1.0/authorization/sms', AuthorizationSmsPost)
    app.router.add_post('/v1.0/authorization/sms/complete', AuthorizationSmsCompletePost)
