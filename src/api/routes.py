from .resources import (
    OAuthSmsPost,
    OAuthCodePost,
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


def init_routes(app):
    app.router.add_post('/v1/oauth/sms', OAuthSmsPost)
    app.router.add_post('/v1/oauth/code', OAuthCodePost)
    app.router.add_get('/v1/user', UserGet)
    app.router.add_post('/v1/user', UserPost)
    app.router.add_get('/v1/stream', StreamGet)
    app.router.add_get('/v1/chats', ChatsGet)
    app.router.add_get('/v1/chat/{chat_id}', ChatGet)
    app.router.add_post('/v1/messages', MessagePost)
    app.router.add_get('/v1/chat/{chat_id}/messages', MessagesGet)
    app.router.add_get('/v1/sessions', SessionsGet)
    app.router.add_delete('/v1/sessions', SessionsDelete)
    app.router.add_post('/v1/session', SessionPost)
    app.router.add_delete('/v1/session/{session_id}', SessionDelete)
