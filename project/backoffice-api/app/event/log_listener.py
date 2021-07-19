from app.services.logger import LogService

logger = LogService()

def handle_user_created_event(user, new_user):
    log = f"{user.username} created the user {new_user.username}"
    logger.log_to_db(log)