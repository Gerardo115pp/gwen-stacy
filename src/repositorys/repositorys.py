from . import getRepositorys, Repository
import click, os


@click.group()
@click.pass_context
def repos(context):
    context.obj["repos"] = getRepositorys(context.obj["paths"]["libs"])
    pass

# Create a repository function, ask for the name of the repository and promt for the description. it creates a new repository with a repo_description.yaml inside the repository.
@repos.command("create")
@click.argument("name", type=str, nargs=1)
@click.pass_context
def createRepo(context, name):
    new_repo = Repository(os.path.join(context.obj["paths"]["libs"], name))
    
    description = click.prompt("repo description", show_choices=False, show_default=False, type=str)
    new_repo.description = description
    
    new_repo.create()
    click.secho("Repository created", fg="green")
    
# list all the repositories, takes and optional argument 'long', if long is true it will list the description of the repositorys.
@repos.command("list")
@click.option("-l","--long", is_flag=True, default=False,help="list the description of the repositorys")
@click.pass_context
def listRepos(context, long):
    for repo in context.obj["repos"].values():
        if long:
            click.secho(f"{str(repo):>20}: {repo.description:<5}\n", fg="cyan")
        else:
            click.secho(repo.name, fg="cyan")
