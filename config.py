import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'todo.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = '2fn<`2U#M=}~L#%!eoh3uR8yhf66N]'











