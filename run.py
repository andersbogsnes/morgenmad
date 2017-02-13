from flask.helpers import get_debug_flag
from morgenmad.app import create_app
from morgenmad.config import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig
app = create_app(CONFIG)
