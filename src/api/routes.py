from .resources import (
    AuthorizationSmsPost,
    AuthorizationSmsCompletePost,
    UserGet,
    UserPost,
    StreamGet,
    ChatsGet,
    ChatGet,
    MessagePost
)


def init_routes_app_v1(app):
    app.router.add_post('/v1.0/authorization/sms', AuthorizationSmsPost)
    app.router.add_post('/v1.0/authorization/sms/complete', AuthorizationSmsCompletePost)
    app.router.add_get('/v1.0/user', UserGet)
    app.router.add_post('/v1.0/user', UserPost)
    app.router.add_get('/v1.0/stream', StreamGet)
    app.router.add_get('/v1.0/chats', ChatsGet)
    app.router.add_get('/v1.0/chat/{chat_id}', ChatGet)
    app.router.add_post('/v1.0/messages', MessagePost)
