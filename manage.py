import os
from shutil import copyfile

from flask_script import Manager

from src.app import App

app = App()

manager = Manager(app.flask_app)

if __name__ == '__main__':
    manager.run()
