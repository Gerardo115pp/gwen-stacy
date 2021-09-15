from .default_config import *
from typing import Dict, List
import click, yaml

@click.group()
def config():
    pass

def createDefaultConfig() -> Dict[str, str]:
    patriots_lib_path = LIBS_DIR
    patriots_templates_path = TEMPLATES_DIR
    
    os.mkdir(PATRIOTS_LINKER_SRC)
    os.mkdir(patriots_lib_path)
    os.mkdir(patriots_templates_path)
    
    patriots_config = {
            "src": PATRIOTS_LINKER_SRC,
            'libs': patriots_lib_path,
            'templates': patriots_templates_path
        }
    print("First run detected. Creating config file...")
    
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(patriots_config, f)

def saveConfig(config):
    pass
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)

@config.command("set")
@click.option('-e' ,'--entry', default=None, required=True, type=str,help="the name of the entry")
@click.option('-v' ,'--value', default=None, required=True, type=str, help="the new configuration value")
@click.pass_context
def setConfig(context, entry, value):
    print("changeing configurations is now deprecated")
    
    
@config.command("show")
@click.pass_context
def showConfig(context):
    for entry, value in context.obj['config'].items():
        print(f"{entry:>20}:{value:^20}")