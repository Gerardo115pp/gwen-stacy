from typing import List, Dict, Union, final
from src.configuration_manager.default_config import TEMPLATES_DIR
from shutil import rmtree
import json, os

'''
    Templates are used to generate projects directories and files structure. 
    they will be defined in a json file whici will be store ond TEMPLATES_DIR/<template_name>/structure.json.
    this file may or may not reference  some files, this files will also be stored on TEMPLATES_DIR/<template_name>/
    
    the cli will contain the following commands:
    
    use:
    
        this command will generate a new template from current working directory, it will walk
        the current directory and create a new directory with the same name as the template. or 
        a new name can be specified with the --name option.
    
    list:
    
        this command will list all the available templates.
    
    spawn <template_name> [--project <project name> required]:

        this command will generate a new project from a template.
        
    update <template_name>:
    
        this command will update the structure of a template from the current working directory.
        
    --------------------------------------------------------------------------------------------------------------------
    
    the class Template will contain all the necesarry logic to interact with the templates.
    
    the method loadTemplates is used to load all as a list of Template objects.
    
    the method getTemplate is used to get a template by name. the name must exist in the TEMPLATES_DIR.
        
'''
if not os.path.exists(TEMPLATES_DIR):
    os.mkdir(TEMPLATES_DIR)


class Template:
    STRUCTURE_FILE = 'structure.json'
    
    def __init__(self, name:str) -> None:
        self.name = name
        self.structure:Dict = self.loadStructure()
        self.files:List[str] = self.loadFiles() # a list with relative paths to files
        self.template_dir = os.path.join(TEMPLATES_DIR, self.name)
    
    # creates the template
    def boil(self, overwrite:bool=False) -> None:
        '''
            if Template deosnt exists it will create it from self.structure and self.files. it 
            requires self.structure to not be None and if self.files is not empty, every file in
            it must exists on cwd.
            
            if Template already exists it will raise an exception unless overwrite is True in which
            case it will overwrite the template.
        '''
        
        
        if self.structure is None:
            raise Exception('Template.structure is None')
        if len(self.files) > 0:
            for file in self.files:
                if not os.path.exists(file):
                    raise Exception('Template.files contains a file that does not exists on cwd')
        
        print(f'creating template {self.name}')
        # create the template
        if self.IsCreated and not overwrite:
            raise Exception('Template already exists, and overwrite is False')
        elif overwrite:
            # remove everything in the template directory
            rmtree(self.template_dir)
            
        os.mkdir(self.template_dir)
        
        # copy files from cwd to TEMPLATE_DIR/<self.name>/
        for file in self.files:
            print(f"copying {file}")
            os.system(f'cp {file} {self.template_dir}/{file}')
            
            
        # create the structure.json
        with open(os.path.join(self.template_dir, self.STRUCTURE_FILE), 'w') as f:
            json.dump(self.structure, f, indent=4)
        print(f'Template {self.name} created')
    
    def __createStructure(self) -> None:
        '''
            creates the structure of the template.
        '''
        for key, value in self.structure.items():
            if isinstance(value, dict):
                print(f'creating directory {key}')
                os.mkdir(key)
                os.chdir(key)
                self.__createStructure()
                os.chdir('..')
            else:
                print(f'copying {value}')
                os.system(f'cp {os.path.join(self.template_dir, value)} {key}')
    
    def display(self) -> str:
        '''
            returns a string with the template name, files and structure it contains.
        ''' 
        structure = json.dumps(self.structure, indent=4)
        structure += f"\ntemplate: {self.name}"
        return structure
    
    @property
    def IsCreated(self) -> bool:
        '''
            checks if self.name exists in TEMPLATES_DIR
        '''
        return os.path.exists(os.path.join(TEMPLATES_DIR, self.name))
        
    @final
    def loadStructure(self) -> Union[Dict, None]:
        '''
            loads the STRUCTURE_FILE from the TEMPLATES_DIR/<template_name>/
            the structure is a json file which contains the files and directories structure.
            
            it will first check if STRUCTURE_FILE exists in the TEMPLATES_DIR/<template_name>/
            if it does not exists it will return None.
            
        '''
        structure_file = os.path.join(TEMPLATES_DIR, self.name, Template.STRUCTURE_FILE)
        if not os.path.exists(structure_file):
            return None
        
        with open(structure_file) as f:
            return json.load(f)

    @final
    def loadFiles(self) -> Union[List, None]:
        '''
            loads all the files from the TEMPLATES_DIR/<template_name>/
            it will return a list of all the files. it excludes the STRUCTURE_FILE.
            
            if TEMPLATES_DIR/<template_name>/ does not exists it will return None.
        '''
        if not os.path.exists(os.path.join(TEMPLATES_DIR, self.name)):
            return None 
        
        files = []
        for file in os.listdir(os.path.join(TEMPLATES_DIR, self.name)):
            if file != Template.STRUCTURE_FILE:
                files.append(file)
        return files
    
    def scan(self) -> None:
        '''
            scans the current working directory and stores the files in self.files and 
            directories in self.structure.
        '''
        self.files = [] if self.files is None else self.files
        self.structure = {} if self.structure is None else self.structure
        
        # recursively scan the current directory and fill self.structure and self.files
        self.__walkCwd(self.structure, ".")
        
    def __walkCwd(self, structure:Dict, cwd:str) -> None:
        '''
            cwd is the current working directory. on level 0 it will be "." and on level 1 it will be "./<dir1>"
            on level 2 it will be "./<dir1>/<dir2>" and so on.
        '''
        for node in os.scandir(cwd):
            node_path = node.path.replace("./", "")
            if node.is_symlink():
                continue
            
            if node.is_dir():
                structure[node.name] = {}
                self.__walkCwd(structure[node.name], node_path)
            else:
                structure[node.name] = node_path
                self.files.append(node_path)
    
    def spawn(self, project_name:str) -> None:
        '''
            creates a directory structure on <project_name> from the template called self.name.
            it will copy all the files from the template to <project_name>
        '''
        if os.path.exists(project_name):
            print(f'{project_name} already exists')
            exit(1)
        
        # create the project directory
        os.mkdir(project_name)
        
        # self.__createStructure() will recursively create the directory structure from self.structure
        cwd = os.getcwd()
        
        os.chdir(project_name)
        self.__createStructure()
        os.chdir(cwd)
        

def templateExists(template_name:str) -> bool:
    '''
        checks if template_name exists in TEMPLATES_DIR
    '''
    return os.path.exists(os.path.join(TEMPLATES_DIR, template_name))

def getTemplates() -> List[Template]:
    '''
        returns a list of all the templates in TEMPLATES_DIR as Template objects.
    '''
    templates = []
    for template in os.scandir(TEMPLATES_DIR):
        new_template = Template(template.name)
        assert new_template.IsCreated, f'Template {template} is not created, this is most likly a logic error'
        templates.append(new_template)
        
    return templates
    
def getTemplate(template_name:str) -> Template:
    if not os.path.exists(os.path.join(TEMPLATES_DIR, template_name)):
        raise Exception(f'Template {template_name} does not exists')
    
    return Template(template_name)
    
    
    
    
    
    
    