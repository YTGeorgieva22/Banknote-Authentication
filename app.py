from flask_bootstrap import Bootstrap

from flask import Flask

from config import Config
from  __init__  import create_app

app = create_app(Config)
bootstrap = Bootstrap(app)

if __name__ == '__main__':
    app.run()