from pydantic import BaseSettings, Field, SecretStr
from redis import Redis

class BaseConfig(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

class _BotConfig(BaseConfig):
    token: SecretStr
    skip_updates: bool
    owner_id: int 

class _PostgresQLConfig(BaseConfig):
    host: str = Field(env='psql_host')
    port: int = Field(env='psql_port')
    user: str = Field(env='psql_user')
    password: SecretStr = Field(env='psql_password')
    database: str = Field(env='psql_database')

class _RedisConfig(BaseConfig):
    host: str = Field(env='redis_host')
    port: int = Field(env='redis_port')
    password: SecretStr = Field(env='redis_password')
    database: int = Field(env='redis_database')

class Config:
    bot = _BotConfig()
    psql = _PostgresQLConfig()
    redis = _RedisConfig()
