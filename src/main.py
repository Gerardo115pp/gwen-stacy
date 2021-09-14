import click

@click.group()
@click.pass_context
def cli(context):
    context.obj = {}

@cli.command()
@click.argument("name", nargs=1)
def hello(name):
    click.echo(f"hellow {name}")
    

