from src.default_config import  CONFIG_FILE
import click, yaml

@click.group()
def config():
    pass

def saveConfig(config):
    pass
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)

@config.command("set")
@click.option('-e' ,'--entry', default=None, required=True, type=str,help="the name of the entry")
@click.option('-v' ,'--value', default=None, required=True, type=str, help="the new configuration value")
@click.pass_context
def setConfig(context, entry, value):
    context.obj['config'][entry] = value
    saveConfig(context.obj['config'])
    
@config.command("show")
@click.pass_context
def showConfig(context):
    for entry, value in context.obj['config'].items():
        print(f"{entry:>20}:{value:^20}")