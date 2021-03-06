from Gwen.modules_manager import PatriotModule
from Gwen.repositorys import Repository, parseRepoModuleString
from Gwen.repositorys.repositorys import getRepositorys
from typing import List, Dict
import click, os, json

@click.group()
@click.pass_context
def modules(context):
    """
    Manage modules
    """
    context.obj["repos"] = getRepositorys(context.obj["paths"]['libs'])


@modules.command("add_dependency")
@click.option("--module", "-t", help="Target module name", required=True)
@click.option("--repo", "-t", help="Target module name", default="_", required=False)
@click.argument("dependencys", nargs=-1)
@click.pass_context
def add_dependency(context, module, dependencys, repo):
    """
        Adds a module to the dependency list of a target module. if repo is
        provided, it will   look for int only in that repository. if is not provided, it will
        look for a module with the same name in all repositories and use the first one found.
        by defual its assumed that the dependencys are in the same repository as the target module.
        if this is not the case, you can provide the repo on the dependency name as follows:
            
            repo>dependency
    """
    
    # if repo is not provided, it will look for a module with the same name in all repositories and use the first one found.
    target_repo = None
    if repo == "_":
        click.secho(f"Searching for repo containing '{module}'", fg="yellow")
        for r in context.obj["repos"].values():
            if r.hasModule(module):
                target_repo = r
                break
        
        if target_repo:
            click.secho(f"Found {module} on '{r.name}'", fg="green")
            if not click.confirm(f"Do you want to add the dependency to '{module}' on '{r.name}'", default=False):
                click.secho("Aborted", fg="red")
                return
        else:
            click.secho(f"Could not find '{module}'", fg="red")
            return
    else:
        if repo in context.obj["repos"]:
            target_repo = context.obj["repos"][repo]

    target_module:PatriotModule = r.getModule(module)
    if not target_module:
        click.secho(f"Could not find '{module}' on {target_repo.name}", fg="red")
        return
    
    for d in dependencys:
        if '>' not in d:
            d = f"{target_repo.name}>{d}"
        dependency:PatriotModule = parseRepoModuleString(d)[1]
        target_module.addDependency(dependency.base_dir)
    
    target_module.updateModFile()
    
            


@modules.command("remove_dependency")
@click.option("--module", "-t", help="Target module name", required=True)
@click.option("--repo", "-t", help="Target module name", required=False)
@click.argument("dependency", nargs=-1)
@click.pass_context

@modules.command("load")
@click.option("-m","--module", help="Module to load", required=False)
@click.argument("repo", nargs=1, required=True)
@click.argument("files_list", nargs=-1, required=True, expose_value=True)
@click.pass_context
def loadModule(context: click.Context, module:str, repo:str, files_list: List[str]):
    """
    Add module
    """
    if not module:
        module = click.prompt("Module name", default=os.path.basename(os.getcwd()), show_default=True,type=str) # default to current working directory basename
    module_description = click.prompt("Description", show_choices=False, show_default=False, default="",type=str)
    
    if repo in context.obj["repos"]:
        context.obj["repos"][repo].load(module, module_description, files_list)
    else:
        click.secho("Repository not found", fg="red")



'''
    Recives a repo name and a module name and creates a symbolic link to the module. 
    Opcionaly, it can recive a --files flag to specify the files to be symlinked.
'''
@modules.command("link")
@click.option("-f", "--files", default=None, type=str,help="Specify files to be symlinked, separate them by a coma")
@click.argument("repo", nargs=1, required=True)
@click.argument("module", nargs=1, required=True)
@click.pass_context
def linkModule(context:click.Context, repo:str, module:str, files:str):
    """
    Link module
    """
    if repo in context.obj["repos"]:
        target_repository = context.obj["repos"][repo]
        if target_repository.hasModule(module):
            if(target_module := target_repository.getModule(module)):
                if files:
                    files = files.split(",")
                    target_module.link(files)
                else:
                    target_module.link(None)
            else:
                click.secho("Module not found", fg="red")
        else:
            click.secho("Repository not found", fg="red")
    else:
        click.secho("thats odd, you should neve see this unless mds callback wasnt triggered", fg="red")

@modules.command("list")
@click.option("-r","--repo", default="", help="Repository to list", required=False)
@click.option("-l", "--long", default=False, is_flag=True, help="Long list, includes description")
@click.pass_context
def listModules(context:click.Context, repo:str, long:bool):
    """
    List modules from a repository
    """
    if repo == "":
        # list all repos
        for repo in context.obj["repos"].values():
            repo:Repository
            repo.display(long)


@modules.command("update")
@click.argument("repo", nargs=1, required=True)
@click.argument("module", nargs=1, required=True)
@click.argument("files_list", nargs=-1, required=True, expose_value=True)
@click.pass_context
def updateModule(context:click.Context, repo, module, files_list):
    """
    Update module
    """
    if repo in context.obj["repos"]:
        repository = context.obj["repos"][repo]
        if repository.hasModule(module):
            module_to_update:PatriotModule = repository.getModule(module)
            module_to_update.update(files_list)
            click.secho("Module updated", fg="green")
    else:
        click.secho("Repository not found", fg="red")