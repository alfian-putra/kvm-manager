#!/usr/bin/python3
import os
import sys
import subprocess

from common.config import Config
from common.fetch_api import FetchApi

config = Config().config
api = FetchApi()

# CONST & VARIABLE
CMD_START_BACKEND = f"fastapi run --workers {config['backend']['worker']} kvm-manager-backend.py"
CMD_START_WEB = "streamlit run kvm-manager-ui-web.py"
CMD_START_BOT = "python3 kvm-manager-ui-bot.py"

if config["home"]["venv"]:
    CMD_START_BACKEND = f"{config["home"]["venv_path"]}/bin/python -m fastapi run --workers {config['backend']['worker']} kvm-manager-backend.py"
    CMD_START_WEB = f"{config["home"]["venv_path"]}/bin/python -m streamlit run kvm-manager-ui-web.py"
    CMD_START_BOT = f"{config["home"]["venv_path"]}/bin/python kvm-manager-ui-bot.py"

OUTPUT_FILE_BACKEND = os.path.join(config["log"]["path"],"backend.output")
OUTPUT_FILE_WEB = os.path.join(config["log"]["path"],"web.output")
OUTPUT_FILE_BOT = os.path.join(config["log"]["path"],"bot.output")

READ_OUTPUT_FILE_BACKEND = open(OUTPUT_FILE_BACKEND, "w")
READ_OUTPUT_FILE_WEB = open(OUTPUT_FILE_WEB, "w")
READ_OUTPUT_FILE_BOT = open(OUTPUT_FILE_BOT, "w")

PWD = os.getcwd()
PATH_PID = os.path.join(PWD, ".pid")

PID_FILE_BACKEND = os.path.join(PATH_PID, "backend.pid")
PID_FILE_WEB = os.path.join(PATH_PID, "web.pid")
PID_FILE_BOT = os.path.join(PATH_PID, "bot.pid")

if not os.path.isdir(PATH_PID) :
    os.mkdir(PATH_PID)


# FUNCTION
def run_command(cmd):
    _cmd = cmd.split(" ")
    result = subprocess.run(_cmd, capture_output=True, text=True)    
    return result

def run_command_nohup(cmd, output_file):
    _cmd = cmd.strip()
    if not _cmd[-1]=="&":
        _cmd = ("nohup "+ _cmd)
        _cmd = _cmd.split(" ")
    print(repr(_cmd))
    return subprocess.Popen(_cmd, stdout=output_file, stderr=subprocess.STDOUT)


def get_pid(pid_file):
    f = open(pid_file, "r")
    return str(f.readlines()[0])


def start(cmd, pid_file, output_file):
    print("start service ...")
    cmd = run_command_nohup(cmd, output_file)
    pid = cmd.pid

    if not cmd.stderr==None:
        raise Exception(f"PID file creation failed : {cmd.stderr}")
    
    with open(pid_file, "w") as f:
        f.write(str(pid))
    
    print("Service started successfully !")

def stop(pid_file):
    print("stop service ...")

    try :
        pid = get_pid(pid_file)
        cmd = f"kill {pid}"
        cmd_result = run_command(cmd)
        print(cmd_result.stderr)
        os.remove(pid_file)

    except Exception as e:
        raise Exception(f"Stop failed : \n\t{e}")

    print("Service stopped")

# handling virtual env (venv)

# RUN
## backend
def start_backend():
    start(CMD_START_BACKEND, PID_FILE_BACKEND, READ_OUTPUT_FILE_BACKEND)

def stop_backend():
    stop(PID_FILE_BACKEND)

## ui-website
def start_web():
    start(CMD_START_WEB, PID_FILE_WEB, READ_OUTPUT_FILE_WEB)

def stop_web():
    stop(PID_FILE_WEB)

## ui-bot
def start_bot():
    start(CMD_START_BOT, PID_FILE_BOT, READ_OUTPUT_FILE_BOT)

def stop_bot():
    stop(PID_FILE_BOT)

command = sys.argv[1]
service = None

try :
    service = sys.argv[2]
except :
    service = "all"

if command=="start":
    if service=="backend":
        start_backend()
    elif service=="web":
        start_web()
    elif service=="bot":
        start_bot()
    elif service=="all":
        start_backend()
        start_web()
        start_bot()

elif command=="stop":
    if service=="backend":
        stop_backend()
    elif service=="web":
        stop_web()
    elif service=="bot":
        stop_bot()
    elif service=="all":
        print("it is work !")
        stop_backend()
        stop_web()
        stop_bot()

elif command=="status":
    print("backend", end="\t\t")
    if os.path.exists(PID_FILE_BACKEND):
        print("up")
    else:
        print("down")

    print("web", end="\t\t")
    if os.path.exists(PID_FILE_WEB):
        print("up")
    else: 
        print("down")
    

    print("bot", end="\t\t")
    if os.path.exists(PID_FILE_BOT):
        print("up")
    else:
        print("down")

elif command=="init":
    if config["home"]["venv"]:
        err =None

        try: 
            import venv
        except Exception as e:
            err = e
            run_command("pip install venv")
        
        run_command(f"python3 -m venv {config["home"]["venv_path"]}")
        run_command(f"source {config["home"]["venv_path"]}/bin/activate")
    
    try:
        run_command("pip install -r requirement")
        api.user.init()
        api.cloud_init.init()
        
        print("Init success")
    except Exception as e:
        print(f"ERROR module installation failed : {e}")

