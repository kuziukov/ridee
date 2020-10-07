from .resources import (
    AuthorizationSmsPost,
    AuthorizationSmsCompletePost,
    UserGet,
    UserPost,
    StreamGet
)


def init_routes_app_v1(app):
    app.router.add_post('/v1.0/authorization/sms', AuthorizationSmsPost)
    app.router.add_post('/v1.0/authorization/sms/complete', AuthorizationSmsCompletePost)
    app.router.add_get('/v1.0/user', UserGet)
    app.router.add_post('/v1.0/user', UserPost)
    app.router.add_get('/v1.0/stream', StreamGet)
