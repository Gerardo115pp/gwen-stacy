import click, json, os
from subprocess import Popen, PIPE
'''

    this library is used to jump to different checkpoints(which are just directories) definded
    by the user. it will have the following cli commands:
    
    add_checkpoint <name> <?path>:
    
        add a new checkpoint named <name> pointing to <path>. if <path> is not specified, 
        current directory is assumed.
    
    jump <name>:
    
        jump to the checkpoint named <name>. if not exists, it will notify the user and do nothing.
        
    list_checkpoints:
    
        list all checkpoints.
    
    remove_checkpoint <name>:
    
    
    Side note, this commands are not meant to be assigned to a group since they belong to the
    misc category, this means they will exist in the main cli group.
        

'''


@click.command('add_chk')
@click.argument('name')
@click.option('-p', '--path', default='.', help='path where the checkpoint points to.')
@click.pass_context
def addCheckpoint(context, name, path):
    '''
    add a new checkpoint named <name> pointing to <path>. if <path> is not specified, 
    current directory is assumed.
    '''
    if path == '.':
        path = os.getcwd()
        
    path = os.path.abspath(path)
    checkpoint_dir = os.path.join(context.obj['paths']["checkpoints"], "checkpoints.json")
    
    # checkpoints.json must exist because is verified in the main cli group
    with open(checkpoint_dir, 'r') as f:
        checkpoints = json.load(f)
    
    checkpoints[name] = path
    click.secho(f"added checkpoint {name} pointing to '{path}'", fg='green')
    
    with open(checkpoint_dir, 'w') as f:
        json.dump(checkpoints, f)
        
@click.command('jump')
@click.argument('name')
@click.pass_context
def jumpToCheckpoint(context, name):
    '''
    jump to the checkpoint named <name>. if not exists, it will notify the user and do nothing.
    '''
    checkpoint_dir = os.path.join(context.obj['paths']["checkpoints"], "checkpoints.json")
    
    with open(checkpoint_dir, 'r') as f:
        checkpoints = json.load(f)
    
    if name in checkpoints:
        print(checkpoints[name]) # this output is consumed by a bash script which executes the command
        
    
@click.command('list_chk')
@click.pass_context
def listCheckpoints(context):
    '''
    list all checkpoints.
    '''
    checkpoints_dir = os.path.join(context.obj['paths']["checkpoints"], "checkpoints.json")
    
    with open(checkpoints_dir, 'r') as f:
        checkpoints = json.load(f)
        
    for checkpoint in checkpoints:
        click.secho(f"{checkpoint} -> {checkpoints[checkpoint]}", fg='green')
