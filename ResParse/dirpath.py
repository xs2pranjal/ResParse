import os
from configurations import get_env_var

RESUMEPATH = os.path.expanduser("~") + '/ResParse'
RESUMEPATH = get_env_var("RESUME_PATH", RESUMEPATH)

PKGPATH = os.path.dirname(os.path.abspath(__file__))
