import os
import json
import pandas as pd
# /user 
#   register
#   change_password
# /request_vm
# 
import requests


from common.common_utility import config
from ui_bot.lib.common_utility import log
from ui_bot.lib.common_utility import api

MESSAGE = {} # contain all message template

def register(new_user):
    pass

def change_password(user_id, old_password, new_password):
    pass

def download_file(bot_token, file_path, target_filepath):
    log.info("Download file")
    try :
        url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        log.info(f"GET {url}")
        response = requests.get(url)

        print(f"target_filepath : {target_filepath}" )
        with open(target_filepath, "wb") as f:
            f.write(response.content)

    except Exception as e :
        log.warning(f"Download failed : {e}")
        return False
    return True

def request_vm(csv_file, user_id):
    # read csv of vm list
    # make an VM object for each row
    # deploy to database vm in status : 'REQUEST'
    csv = pd.read_csv(csv_file)

    csv_obj = csv.select_dtypes("object")
    csv[csv_obj.columns] = csv_obj.apply(lambda x : x.str.strip())


    res = {}
    for id, data in csv.iterrows():
        try :
            new_vm = {}
            print(f"TES >>> {repr(data)}")
            # print(f"TES >>> {data["hostname"]}")

            if data["hostname"]=="hostname@example":
                res[data["hostname"]] = "Restricted hostname 'example'."
                continue

            if data.isnull().any():
                res[data["hostname"]] = "Restricted empty value."
                continue 

            print(f"ISNULL >> {data.isnull().any()}")
            ##try:
            print(f"THIS >> {api.user.read_by_user_id(user_id)["response"]}")
            is_user_exist = api.user.read_by_user_id(user_id)
            
            if is_user_exist["code"]==404:
                raise Exception("User not found !")
            else :
                print(api.user.read_by_user_id(user_id)["api"])
                print(api.user.read_by_user_id(user_id)["code"])
                new_vm["user_id"] = api.user.read_by_user_id(user_id)["response"]["id"]
            new_vm["name"] = data["name"]
            new_vm["hostname"] = data["hostname"]
            check_hostname = api.vm.read_by_hostname(new_vm["hostname"])["response"]
            print(f">> CHECK_HOSTNAME {check_hostname}")
            if check_hostname:
                raise Exception("Hostname already exist !")
            new_vm["vcpu"] = data["vcpu"]
            new_vm["memmory"] = data["memmory (Mib)"]

            dd = data["os"]
            print(f"CHECK >>>>> {dd}")
            if (not type(data["os"]==str)) or (not "_" in data["os"]):
                raise Exception("OS format")
            else :
                data["os_name"] = data["os"].split("_")[0].title()
                data["os_version"] = data["os"].split("_")[1]
            
            all_os = api.os.read_all()["response"]

            print(f">> ALL OS  {all_os}")

            new_vm_os = None

            for _os in all_os:
                print("'"+_os["name"].strip()+"'")
                print("'"+data["os_name"]+"'")
                print(f"_os = {_os["name"].strip()==data["os_name"]}")
                print(f"_os = {str(_os["version"])==data["os_version"]}")
                if (_os["name"].strip()==data["os_name"]) and (str(_os["version"])==data["os_version"]):
                    new_vm["os_id"] = _os["id"]
                    new_vm_os = _os["id"]
            if new_vm_os==None:
                raise Exception("OS not Found !")
            
            
            new_vm["group_name"] = data["group_name"]
            print(f"GROUP_NAME >>>>> {new_vm}")
            vm_data = json.dumps(new_vm)

            # add data
            create = api.vm.create(vm_data)

            print(create)
            vm_id = api.vm.read_by_hostname(new_vm["hostname"])["response"][0]["id"]

            disk_name = new_vm["hostname"] + "_disk1"
            disk_qcow2 = os.path.join(config["kvm"]["pool"]["path"], disk_name+".qcow2")
            disk = {"vm_id":vm_id, "disk_size":data["disk_size (Gib)"], "name":disk_name, "qcow2":disk_qcow2}
            _disk = json.dumps(disk)

            api.disk.create(_disk)
        
            res[data["hostname"]] = "success"

        except Exception as e:
            res[data["hostname"]] =  e
        
    return res