from src.repositorys.repositorys import getRepositorys
from typing import List
import click, os

@click.group()
@click.pass_context
def mds(context):
    """
    Manage modules
    """
    context.obj["repos"] = getRepositorys(context.obj["config"]['libs'])

@mds.command("load")
@click.argument("repo", nargs=1, required=True)
@click.argument("files_list", nargs=-1, required=True, expose_value=True)
@click.pass_context
def loadModule(context: click.Context, repo:str, files_list: List[str]):
    """
    Add module
    """
    module_name = click.prompt("Module name", default=os.path.basename(os.getcwd()), show_default=True,type=str) # default to current working directory basename
    module_description = click.prompt("Description", default="",type=str)
    
    if repo in context.obj["repos"]:
        context.obj["repos"][repo].load(module_name, module_description, files_list)
    else:
        click.secho("Repository not found", fg="red")