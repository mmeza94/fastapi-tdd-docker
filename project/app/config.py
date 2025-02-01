import logging
from functools import lru_cache

from pydantic import AnyUrl
from pydantic_settings import BaseSettings

log = logging.getLogger("uvicorn")


# BaseSettings also automatically reads from environment variables
# for these config settings. In other words, environment: str = "dev" is equivalent to
# environment: str = os.getenv("ENVIRONMENT", "dev")
class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = bool(0)
    database_url: AnyUrl = None


# Essentially, get_settings gets called for each request.therefore, we use cache so it is only called once
# Cuando la caché alcanza su tamaño máximo, elimina los elementos que se han usado menos recientemente
@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
