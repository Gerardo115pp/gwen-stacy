from .configuration_manager.config import config, createDefaultConfig
from .configuration_manager.default_config import *
from .repositorys.repositorys import repos
from .modules_manager.modules_manager import modules
import click, yaml
import os




def isFirstRun() -> bool:
    """
    Checks if the user has run the program before.
    If not, it will create a config files
    """
    return os.path.exists(PATRIOTS_LINKER_SRC)

@click.group()
@click.pass_context
def cli(context):
    patriots_config = {}
    if not isFirstRun():
        patriots_config = createDefaultConfig()
    else:
        with open(CONFIG_FILE, 'r') as f:
            patriots_config = yaml.load(f, Loader=yaml.FullLoader)
            
    context.obj = {
        "config": patriots_config
    }

    
cli.add_command(config)
cli.add_command(repos)
cli.add_command(modules)
