import os
from abc import ABC



class Env(ABC):
    TOKEN = os.environ.get('TOKEN')