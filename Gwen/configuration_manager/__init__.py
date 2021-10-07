import os
# 
PATRIOTS_LINKER_SRC = os.path.join(os.path.expanduser('~'), '.gwen')
TEMPLATES_DIR = os.path.join(PATRIOTS_LINKER_SRC, 'templates')
LIBS_DIR = os.path.join(PATRIOTS_LINKER_SRC, 'libs')
CONFIG_FILE = os.path.join(PATRIOTS_LINKER_SRC, 'config.yml')
CHECKPOINTS_DIR = os.path.join(PATRIOTS_LINKER_SRC, 'checkpoints')

app_data = {
    "paths": {
        "src": PATRIOTS_LINKER_SRC,
        "templates": TEMPLATES_DIR,
        "libs": LIBS_DIR,
        "checkpoints": CHECKPOINTS_DIR
    },
    "repos": {}

}