from config import settings


def get_env():
    return settings.ENV if settings.ENV in ["prod", "dev"] else "local"
