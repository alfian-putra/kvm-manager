import subprocess
import re
import os
from urllib.request import Request, urlopen
import shutil
import psutil
import glob
from datetime import datetime

from backend.lib.common_utility import log, config
# KVM SERVER MONITOR
#
#   - monitoring vm (servced on web ui dashboard
#   - execute command

KVM_USER = config["kvm"]["user"]
KVM_HOST = config["kvm"]["host"]
CLOUD_INIT_PATH = "../tmp"
CLOUD_INIT_LIST = glob.glob(os.path.join(CLOUD_INIT_PATH,"/*"))

def execute_subprocess(cmd):
    # example cmd : ["systemctl status postgresql"]

    log.debug(f"Executing : {cmd}")

    result = subprocess.run(cmd.split(" "), capture_output=True, text=True)
    
    if not result.stderr == "":
        log.debug(f"Execution failed {result.stderr}")
    else:
        log.debug("Execution success !")
    
    return result

def execute_command(command):
    cmd = f"ssh {KVM_USER}@{KVM_HOST} " + command

    return execute_subprocess(cmd)

# VM MANAGEMENT
#
#   - initiate vm
#      requirement :
#          - virt-install (run using subprocess)
#          - cloud-init (using yaml, will be 
#                        execcuted when running virt-instal 
#                        as a parameter)
#          - --os-variant detect=on
#          - cloud-base qcow2 (registered by admin 
#                              using web ui)
#
#   - start vm
#
#   - stop vm
def generate_cloudInit_iso(cloudInitFile):
    isoFile = cloudInitFile.split("/")[-1]+".iso"
    isoFile = os.path.join(config["kvm"]["pool"]["path"],isoFile)

    cmd = f"genisoimage -output '{isoFile}' -input-charset utf-8 -volid cidata -joliet -rock '{cloudInitFile}'"
    exec = execute_command(cmd)

    print(exec)
    return isoFile

def vm_create(qemu_url, cloud_init_tmp, disk_os_path, disk_vm_path, var,vm,os_data):
    print(f' VM >>> {vm}')

    rendered_cloud_init_file = render_template(cloud_init_tmp,var, vm,os_data) # nameVm_default
    cloudInit_iso = generate_cloudInit_iso(rendered_cloud_init_file)

    execute_command(f'cp {disk_os_path} {disk_vm_path}')

    cmd = f"virt-install --name '{vm.name}' " \
          f"--connect {qemu_url} " \
          f"--memory {vm.memmory} --vcpus {vm.vcpu} " \
          f"--disk path='{disk_vm_path}',device=disk,bus=virtio,format=qcow2 " \
          f"--cdrom '{cloudInit_iso}' " \
          f"--os-variant generic " \
          f"--noautoconsole "

    print(f"CMD >>> {cmd}")

    try :
        exec = execute_command(cmd)
        print(exec)
    except Exception as e:
        log.error(e)
        return False
    
    log.info("VM created successfully !")
    log.info(f"Removing : {rendered_cloud_init_file}")
    log.info(f"Removing : {cloudInit_iso}")
    execute_command(f"rm {rendered_cloud_init_file} {cloudInit_iso}")

    return True

def vm_start(qemu_url, name):
    cmd = f"virsh --connect {qemu_url} start {name}"

    res = ""
    try :
        res = execute_command(cmd)
    except Exception as e:
        log.error(e)
        return [False, e]
    
    return [True, res.stdout]

def vm_status(qemu_url, name):
    cmd = f"virsh --connect {qemu_url} domstate {name}"

    res = ""
    try :
        res = execute_command(cmd)
    except Exception as e:
        log.error(e)
        return False
    
    return res.stdout

def vm_stop(qemu_url, name):
    cmd = f"virsh --connect {qemu_url} shutdown {name}"

    res = ""
    try :
        res = execute_command(cmd)
    except Exception as e:
        log.error(e)
        return [False, e]
    
    return [True, res.stdout]

def vm_reboot(qemu_url, name):
    cmd = f"virsh --connect {qemu_url} shutdown {name}"

    res = ""
    try :
        res = execute_command(cmd)
    except Exception as e:
        log.error(e)
        return [False, e]
    
    return [True, res.stdout]

def vm_extract_all_pool():
    cmd_list = "virsh pool-list --all"
    list = ""

    try:
        list = execute_command(cmd_list).stdout
    except :
        log.error(f"Execution '{cmd_list}' failed !")
    
    
    list = list.split("\n")
    pool_list = []

    log.info(repr(pool_list))
    for i in range(2, len(list)-2):
        pool_list.append(list[i].split(" ")[1])
    
    res = {}
    for x in pool_list:
        cmd = f"virsh pool-dumpxml {x}"
        
        path = re.findall("<path>[\s\S]*?<\/path>",execute_command(cmd).stdout)[0]

        path = path.replace("<path>","")
        path = path.replace("</path>","")

        res[x] = path
    
    return res

def vm_create_pool(name, path):
    cmd_define = f"virsh pool-define-as --name {name} --type dir --target {path}"
    cmd_autostart =  f"virsh pool-autostart {name}"
    cmd_start = f"virsh pool-start {name}"

    if not os.path.exists(path):
        execute_command(f"mkdir -p {path}")

    try :
        log.info(cmd_define)
        execute_command(cmd_define)

        log.info(cmd_autostart)
        execute_command(cmd_autostart)

        log.info(cmd_start)
        execute_command(cmd_start)

        log.info(f"Pool {name} created on {path} successfully !")

    except Exception as e:
        log.error(e)
        return False
    
    
    return True

def vm_is_pool_exist(name):
    cmd = f"virsh pool-info {name}"
    is_exist = False
    try :
        res = execute_command(cmd)
        log.info(res.stdout)
        log.info(res.stderr)
        is_exist = not "not found" in res.stderr
    except Exception as e:
        log.error(e)

    if is_exist:
        log.info(f"Pool {name} exist.")
    else:
        log.info(f"Pool {name} does not exist.")
    
    return is_exist

def download_file(url, filepath):
        try:
            log.info(f"Downloading : {url} to : {filepath}")

            cmd_download = f"wget {url} -O {filepath}"
            log.info(f"Executing command '{cmd_download}'")
            execute_command(cmd_download)
            
            cmd_perm = f"chmod 777 {filepath}"
            log.info(f"Executing command '{cmd_perm}'")
            execute_command(cmd_perm)
            
            log.info(f"File downloaded successfully!")
        except Exception as e:
            log.info("Error downloading the file:", e)

def download_os(url, filename):
    filepath = os.path.join(config["kvm"]["pool"]["path"], filename)
    download_file(url, filepath)
    return filepath

def kvm_server_status():
    def bytes_to_gigabytes(val):
                return round(val / (1024 * 1024 * 1024), 2)
    
    def extract_value(txt, target):
        per_line = txt.split("\n")
        res = None

        for line in per_line:
            if target in line:
                res = int(line.split(" ")[-1])
        return res
    
    # VCPU
    lscpu = execute_command("lscpu | grep -E '^Thread|^Core|^Socket|^CPU\('")

    THREAD_PER_CORE_KEY = "Thread(s) per core"
    CORE_PER_SOCKET_KEY = "Core(s) per socket"
    SOCKET_KEY = "Socket(s)"

    thread_per_core = extract_value(lscpu.stdout, THREAD_PER_CORE_KEY)
    core_per_socket = extract_value(lscpu.stdout, CORE_PER_SOCKET_KEY)
    socket = extract_value(lscpu.stdout, SOCKET_KEY)
    vcpu = thread_per_core * core_per_socket * socket

    # disk
    free_disk = bytes_to_gigabytes(shutil.disk_usage("/").free)

    # memmory
    memmory = bytes_to_gigabytes(psutil.virtual_memory().total)
    
    return {"vcpu" : vcpu, "disk" : free_disk, "memmory" : memmory}

def cloud_init_create(filename,content):
    with open(filename, "w") as f:
        for l in content:
            f.write(l+"\n")

def _resolve_template_var(k, v, vm, _os):
    var = {}
    _kvm_server_status = kvm_server_status()
    if v.strip()[0]=="_":
        match v:
            case "_IP":
                return vm.ip
            case "_HOSTNAME":
                return vm.hostname
            case "_VCPU":
                return vm.vcpu
            case "_MEMMORY":
                return vm.memmory
            case "_OS_NAME":
                return _os.name
            case "_OS_VERSION":
                return _os.version
            case "_KVM_SERVER_HOST":
                return KVM_HOST
            case "_KVM_VCPU":
                return _kvm_server_status["vcpu"]
            case "_KVM_FREE_DISK":
                return _kvm_server_status["disk"]
            case "_KVM_MEMMORY":
                return _kvm_server_status["memmory"]*1024
    return v

def const_value():
    const = {
        "_IP" : "VM IP",
        "_HOSTNAME" : "VM hostname",
        "_VCPU" : "VM VCPU",
        "_MEMMORY" : "VM memmory",
        "_INPUT_VARS_KEY" : "Variable key, the value inputed on vm creation, example: _INPUT_VARS_ADMIN1-SSH-KEY",
        "_OS_NAME" : "OS name",
        "_OS_VERSION" : "OS version",
        "_KVM_SERVER_HOST" : "KVM server hostname",
        "_KVM_VCPU" : "KVM server total possible vcpu",
        "_KVM_FREE_DISK" : "KVM server free disk ",
        "_KVM_MEMMORY" : "KVM server memmory",
    }

    return const

def tmp_full_path(filename):
    return os.path.join(config["home"]["path"],"backend","tmp","cloud_init", filename)

def render_template(filename,var,vm,_os):
    _var_split = var.split(",")
    _var = {}

    print(f"filename {filename}")
    _tmp_filename = tmp_full_path(filename)
    _target_filename = tmp_full_path(f"{datetime.now().strftime("%Y%m%d-%H%M%S")}_{vm.hostname}_{filename}")

    content_template_file =  list(open(_tmp_filename, "r"))

    for item in _var_split:
        k,v = item.split(":")
        key = k.strip()
        _var[key] = _resolve_template_var(k,v,vm,_os)

    print(_var)
    
    for k,v in _var.items():
        for i in range(0,len(content_template_file)):
            _t = "{{"+k+"}}"
            print(f"_t {_t} {_t in content_template_file[i]} {v}")
            if _t in content_template_file[i]:
                print(content_template_file[i])
                content_template_file[i] = content_template_file[i].replace(_t, v)
    
    print(content_template_file)

    cloud_init_create(_target_filename, content_template_file)

    return _target_filename