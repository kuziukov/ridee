import logging
import timber


def init_timber(app):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    timber_handler = timber.TimberHandler(source_id=app.config.TIMBER_ID, api_key=app.config.TIMBER_API_KEY)
    logger.addHandler(timber_handler)
    app.logger = logger

