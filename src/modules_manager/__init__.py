
from typing import Dict, Tuple, List
import yaml, os


'''
    holds data about a single module, its files, name and description. Its function is to generate a
    yaml file that on basedir which will be given after initialization.
'''
class PatriotModule:
    MOD_DATA_FILE = '.mod.yml'
    DEPENDANTS_FILE = '.dependants.yml'
    
    def __init__(self, name:str, description:str, files:Tuple[str]) -> None:
        self.name:str = name
        self.description:str = description
        self.files:Tuple[str] = files
        self.base_dir:str = None # directory to the module
    
    def generateYaml(self) -> None:
        if not (self.base_dir is None):
            with open(f"{self.base_dir}/{PatriotModule.MOD_DATA_FILE}", 'w') as f:
                yaml.dump({'name': self.name, 'description': self.description, 'files': list(self.files)}, f)
        else:
            print('Error: base_dir not set')

    def link(self, files:List[str]) -> None:
        '''
            creates a symbolic link to the files in the files list. if no file list is given, it will
            link all files in the module. if base_dir is not set, it will print an error.
        '''
        if self.base_dir is None:
            raise ValueError('base_dir not set')
        
        if not files:
            files = [f.name for f in os.scandir(self.base_dir) if f.is_file() and not f.name.startswith('.')]

        for f in files:
            os.symlink(f'{self.base_dir}/{f}', f'{os.getcwd()}/{f}')
            print(f'linked {f}')
        
        # DEPENDANTS UPDATE: add current working directory to dependants file
        self.updateDependants(os.getcwd())
            
    def setBaseDir(self, base_dir:str) -> None:
        ''''''
        if self.name != os.path.basename(base_dir):
            raise ValueError(f'module name {self.name} is not the same as directory basenmae: {os.path.basename(base_dir)}')
        
        self.base_dir = base_dir

    def updateDependants(self, dependant:str) -> None:
        """
        adds dependant to DEPEANDANTS_FILE, if it exists. if not the it will created.

        Parameters
        ----------
        dependant : str
            is the path where the module is been used
        """
        dependant_file_content:Dict = None
        
        if not os.path.exists(f'{self.base_dir}/{PatriotModule.DEPENDANTS_FILE}'):
            # create dependants file
            print(f'no dependants file was found. creating...')
            os.mknod(f'{self.base_dir}/{PatriotModule.DEPENDANTS_FILE}')
            dependant_file_content = {'dependants': [dependant]}
        else:
            with open(f'{self.base_dir}/{PatriotModule.DEPENDANTS_FILE}', 'r') as f:
                dependant_file_content = yaml.load(f, Loader=yaml.FullLoader)
                
            # check if dependant is already in dependants file
            if dependant not in dependant_file_content['dependants']:
                dependant_file_content['dependants'].append(dependant)
    
        print(f'{len(dependant_file_content["dependants"])} depentants for module {self.name}')
        
        # save dependants file
        with open(f'{self.base_dir}/{PatriotModule.DEPENDANTS_FILE}', 'w') as f:
            yaml.dump(dependant_file_content, f)
        print(f'updated dependants file')
        

        
def loadModuleFromYaml(mod:str, repo_path:str) -> PatriotModule:
    module_yaml_path = f"{repo_path}/{mod}/{PatriotModule.MOD_DATA_FILE}"
    if os.path.exists(module_yaml_path):
        with open(module_yaml_path, 'r') as f:
            module_yaml = yaml.load(f, Loader=yaml.FullLoader)
        module = PatriotModule(module_yaml['name'], module_yaml['description'], tuple(module_yaml['files']))
        module.setBaseDir(os.path.join(repo_path, mod))
        return module
    