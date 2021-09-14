from src.configuration_manager.config import config
from src.default_config import PATRIOTS_LINKER_SRC, CONFIG_FILE
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
        patriots_lib_path = os.path.join(PATRIOTS_LINKER_SRC, 'libs')
        patriots_templates_path = os.path.join(PATRIOTS_LINKER_SRC, "templates")
        
        os.mkdir(PATRIOTS_LINKER_SRC)
        os.mkdir(patriots_lib_path)
        os.mkdir(patriots_templates_path)
        
        patriots_config = {
                "src": PATRIOTS_LINKER_SRC,
                'patriots_libs': patriots_lib_path,
                'patriots_templates': patriots_templates_path
            }
        print("First run detected. Creating config file...")
        
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(patriots_config, f)
    else:
        with open(CONFIG_FILE, 'r') as f:
            patriots_config = yaml.load(f, Loader=yaml.FullLoader)
            
    context.obj = {
        "config": patriots_config
    }

    
cli.add_command(config)
