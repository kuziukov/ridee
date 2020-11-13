from .resources import (
    OAuthSmsPost,
    OAuthSmsCompletePost,
    UserGet,
    UserPost,
    StreamGet,
    ChatsGet,
    ChatGet,
    MessagePost,
    MessagesGet,
    SessionsGet,
    SessionsDelete,
    SessionPost,
    SessionDelete
)


def init_routes_app_v1(app):
    app.router.add_post('/v1.0/oauth/sms', OAuthSmsPost)
    app.router.add_post('/v1.0/oauth/sms/complete', OAuthSmsCompletePost)
    app.router.add_get('/v1.0/user', UserGet)
    app.router.add_post('/v1.0/user', UserPost)
    app.router.add_get('/v1.0/stream', StreamGet)
    app.router.add_get('/v1.0/chats', ChatsGet)
    app.router.add_get('/v1.0/chat/{chat_id}', ChatGet)
    app.router.add_post('/v1.0/messages', MessagePost)
    app.router.add_get('/v1.0/chat/{chat_id}/messages', MessagesGet)
    app.router.add_get('/v1.0/sessions', SessionsGet)
    app.router.add_delete('/v1.0/sessions', SessionsDelete)
    app.router.add_post('/v1.0/session', SessionPost)
    app.router.add_delete('/v1.0/session/{session_id}', SessionDelete)
