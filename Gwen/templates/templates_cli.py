from typing import List
from . import Template, getTemplates, templateExists
import click, os

@click.group()
@click.pass_context
def templates(context):
    """
    Manage templates
    """
    context.obj["templates"] = {t.name:t for t in getTemplates()}
    
@templates.command("use")
@click.option("--name", "-n", type=str, default="", help="Name of the template to use")
@click.option("-t", "--test", is_flag=True, default=False, help="Test the template")
@click.option("-e", "--exclude", multiple=True, type=str, default=None, help="Exclude a file from the template")
@click.pass_context
def useCwdAsTemplate(context, name:str, test:bool, exclude:List[str]):
    """
    Use the current working directory as a template
    """
    if exclude is None:
        exclude = set()
    else:
        exclude = set(exclude)
        
    if name == "":
        name = os.path.basename(os.getcwd())
    
    
    new_template = Template(name)
    click.secho(f"Using {name} as template", fg="yellow")
    new_template.scan(exclude) # walk the directory and add all files to the template, excluding the exclude set
    print("scanning done")
    click.secho(f"""
        structure: {new_template.structure}\n
        files: {new_template.files}
                """)
    if test:
        return
    
    if click.confirm("Do you want to use this template?", default=False):
        new_template.boil()
        click.secho(f"Boiling done", fg="green")
    else:
        click.secho("Aborted", fg="red")
        
@templates.command("spawn")
@click.option("--project", "-p", type=str, default="", help="Name of the template to use")
@click.argument("template", nargs=1)
@click.pass_context
def spawn(context, project, template):
    """
        create a new project from a template
    """
    
    project = project if project != "" else template
    assert templateExists(template), f"Template {template} does not exist"
    
    target:Template = context.obj["templates"][template]
    print(target.display())
    if click.confirm(f"Do you want to use {template} as template for {project}?", default=False):
        target.spawn(project)
        click.secho(f"Spawning done", fg="green")
    else:
        click.secho("Aborted", fg="red")

@templates.command("update")
@click.argument("template", nargs=1)
@click.pass_context
def update(context, template):
    """
        update a template
    """
    assert templateExists(template), f"Template {template} does not exist"
    
    target:Template = context.obj["templates"][template]
    
    # scan structure of current working directory to update template
    target.scan()
    print(target.display()) # show user what has changed
    if click.confirm(f"Do you want to update {template}?", default=False):
        target.boil(overwrite=True) # overwrite template
        click.secho(f"Updating done", fg="green")
    else:
        click.secho("Aborted", fg="red")


@templates.command("list")
@click.pass_context
def listTemplates(context):
    """
        List all templates
    """
    for template in context.obj["templates"].values():
        print(template.name)
        
