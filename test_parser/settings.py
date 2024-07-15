from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    url: str
    
    
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(url=env('URL'))


config: Config = load_config()