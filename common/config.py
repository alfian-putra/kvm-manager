import os
import yaml

class Config():
    def __init__(self, config_file=os.path.join('','','config.yaml')):
        self.filename = config_file
        self.config = self.load_file()

    def load_file(self):
        with open(self.filename, 'r') as file :
            data = yaml.load(file, Loader=yaml.SafeLoader)
        
        if (data["kvm"]["pool"]["path"][0]==".") :
            data["kvm"]["pool"]["path"] = os.path.join(os.getcwd(), data["kvm"]["pool"]["path"][2:])
        elif (data["kvm"]["pool"]["path"][0].isalpha()) :
            data["kvm"]["pool"]["path"] = os.path.join(os.getcwd(), data["kvm"]["pool"]["path"])
        
        data["backend"]["cloud_init"] = {}
        
        data["backend"]["cloud_init"]["tmp"] = os.path.join(data["home"]["path"],"backend","tmp","cloud_init")
        data["backend"]["cloud_init"]["generated"] = os.path.join(data["home"]["path"],"backend","tmp","cloud_init","generated")
        return data
    
    def update_file(self):
        with open(self.filename, 'w') as file :
            yaml.dump(self.config, file)

