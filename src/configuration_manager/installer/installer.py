from src.configuration_manager import app_data
import os, pathlib

# load features install programs
from src.misc.jump_install import install as jump_install



# verify if ~/.gwen exists
def verifyInstallation() -> None:
    if not os.path.exists(os.path.expanduser("~/.gwen")):
        print("First time run detected")
        run()
        
def loadTools(tool_name:str) -> str:
    
    with open(os.path.join(pathlib.Path(__file__).parent, f"tools/{tool_name}.sh"), 'r') as f:
        content = f.read()
    return content

def addToDotRC():
    # check if we were executed from bash
    shell = os.environ["SHELL"]
    if shell.endswith("bash"):
        shell = "bash"
    elif shell.endswith("zsh"):
        shell = "zsh"
    
    configuration_file = os.path.expanduser(f"~/.{shell}rc")
    print(f"Adding to {configuration_file}")
    if(i := input("If u want to use this file hit enter else enter your rc file.\n>>> ")) != "":
        configuration_file = i
    
    rc_content = ""
    with open(configuration_file, "r") as f:
        rc_content = f.read()
    
    installation_flag = f"\n# added by gwen {os.path.basename(__file__)}\n"
    
    if installation_flag not in rc_content:
        rc_content += installation_flag
        rc_content += loadTools("jump")
    else:
        print("jump is already installed")
        
    with open(configuration_file, "w") as f:
        f.write(rc_content)
    
def run():
    # load tools
    addToDotRC()
    
    gwen_path = app_data['paths']['src']
    

    
    # create ~/.gwen
    if not os.path.exists(app_data['paths']['src']):
        os.mkdir(os.path.expanduser("~/.gwen"))
    
    os.chdir(gwen_path)
    # create anything thats on app_data['paths']
    for path_name, path in app_data['paths'].items():
        print(f"Creating {path_name}")
        
        # checking if path exists
        if not os.path.exists(path):
            os.mkdir(path)
    
    # configure jump
    os.chdir(app_data['paths']['checkpoints'])
    jump_install()
    os.chdir(gwen_path)
    
    
    

