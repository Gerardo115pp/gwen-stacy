from src.configuration_manager.default_config import PATRIOTS_LINKER_SRC
from typing import List, Dict, Tuple
import os, yaml

# A repository is a collection of modules
class Repository:
    repo_data_file = "repo_data.yaml"
    
    def __init__(self, repository_base_path):
        self.name = os.path.basename(repository_base_path)
        self.base_path = repository_base_path
        self.exists = os.path.exists(self.base_path)
        self.description = ""
        self.count: int = -1
        if self.exists:
            self.__loadRepoInfo()
        
    
    def __str__(self):
        return self.name
    
    @property
    def Count(self) -> int:
        if self.count < 0:
            self.count = len(self._getModules())
        return self.count    
        
    def create(self):
        if self.exists:
            print("Repository already exists")
            return
        
        self.exists = True
        os.mkdir(self.base_path)
        self.__addDataFile()

    def __addDataFile(self):
        data_file = {
            "repo_data": {
                "name": self.name,
                "description": self.description,
                "count": 0
            }   
        }
        
        if self.exists:
            with open(self.DataFile, "w") as f:
                yaml.dump(data_file, f)
                

    @property
    def DataFile(self) -> str:
        return os.path.join(self.base_path, Repository.repo_data_file)

    def load(self, module_name:str, desc:str, files: Tuple[str]):
        module_data = {
            "name": module_name,
            "description": desc,
        }
        module_path = os.path.join(self.base_path, module_name)
        
        if not os.path.exists(module_path):
            # Create module directory
            os.mkdir(module_path)
            
            # Create module data file
            with open(os.path.join(module_path, "data.yaml"), "w") as f:
                yaml.dump(module_data, f, version="3.8")
        
        
        # Move files to module directory and create links to them
        for f in files:
            new_file = os.path.join(self.base_path, module_name, os.path.basename(f))
            print(f"moving {f} to '{new_file}'... ", end="")
            if not os.path.islink(f):
                os.rename(f, new_file)
                os.symlink( new_file, os.path.abspath(f"./{f}"))
            print("linked")
        
        print(f"{module_name} created")
        
        
        
            

    def __loadRepoInfo(self):
        if self.exists:
            with open(self.DataFile, "r") as f:
                repo_data = yaml.load(f, Loader=yaml.FullLoader)
                self.description = repo_data["repo_data"]["description"]
                self.count = repo_data["repo_data"]["count"]
        else:
            print("Repository does not exist")

    @property
    def modules(self) -> List[str]:
        return self._getModules()
        
    def _getModules(self) -> List[str]:
        return [ mod.name for mod in os.scandir(self.base_path) if mod.is_dir()]
    
# recives a path for the repository base dire and returns a list of all the repositorys found
def getRepositorys(repository_path: str) -> Dict[str,Repository]:
    repositorys = {}
    for repository in os.scandir(repository_path):
        repositorys[repository.name] = Repository(repository.path)
    return repositorys

