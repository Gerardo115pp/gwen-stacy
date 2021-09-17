from .misc.jump import jumpToCheckpoint, addCheckpoint, listCheckpoints, removeCheckpoint
from .configuration_manager import app_data
from .configuration_manager.config import config
from .configuration_manager.installer.installer import verifyInstallation
from .modules_manager.modules_manager import modules
from .templates.templates_cli import templates
from .repositorys.repositorys import repos
import click, yaml
import os




@click.group()
@click.pass_context
def cli(context):
    
    verifyInstallation()
    
    context.obj = app_data
    

    
cli.add_command(config)
cli.add_command(repos)
cli.add_command(modules)
cli.add_command(templates)

# ===========================
# Misc Commands
# ===========================

# jumps
cli.add_command(jumpToCheckpoint)
cli.add_command(addCheckpoint)
cli.add_command(listCheckpoints)
cli.add_command(removeCheckpoint)