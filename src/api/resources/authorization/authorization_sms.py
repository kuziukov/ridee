from api.resources.authorization.schemas import DeserializationSchema


async def AuthorizationSmsPost(request):

    data = DeserializationSchema().deserialize(await request.json())
    return data

