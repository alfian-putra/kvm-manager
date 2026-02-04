import streamlit as st
import pandas as pd
from ui_website.lib.common_utility import api, config
from ui_website.components.component import button_green
from streamlit_smart_text_input import st_smart_text_input

users = api.user.read_all()["response"]
vms = api.vm.read_all()["response"]
disks = api.disk.read_all()["response"]
os = api.os.read_all()["response"]
kvm_server = api.vm_utility.kvm_server_status()["response"]
cloud_init = api.cloud_init.read_all()["response"]

st.set_page_config(layout="wide")

st.markdown('# VM Request')
st.markdown("---")

group = []
request_vm = []

## SETUP SESSION VARIABLE
if not "const" in st.session_state:
    const_list = api.cloud_init.const_value()["response"]
    const = list(const_list)

    st.session_state["const"]=const
    print(f"    >>>     {const}")


if  not 'edit_data_vm' in st.session_state :
    st.session_state.edit_data_vm = True

if not "cloud_init_vm" in st.session_state:
    st.session_state["cloud_init_vm"] = []

# already parsed vars
if not "cloud_init_vm_deployment" in st.session_state:
    st.session_state["cloud_init_vm_deployment"] = {}

if not "group" in st.session_state:
    st.session_state["group"] = {}

    # {
    #     "group_name" : {
    #         "validity" : False,
    #         "data" : pd.DataFrame(
    #                     {
    #                         "metrics" : ["hostname","total vcpu","total memmory", "total disk"],
    #                         "value" : [_vm_list, total["vcpu"], total["memmory"], total["disk"]],
    #                         "status" :[hostname_validity,vcpu_validity,memmory_validity,disk_validity]
    #                     }
    #                 )
    #     }
    # }


for vm in vms:
    print("Tes vms")
    print(vms)
    print("======================")
    if not vm["group_name"] in group:
        st.session_state["group"][vm["group_name"]] = {}
    if vm["status"] in ["REQUEST","FAIL"]:
        print(f"REQUEST VM >> {repr(request_vm)}")
        request_vm.append(vm)
print(request_vm)
print("}}}}}}}}}}}}}}}}}}}}}}}}}}")
if not "cloud_init_default" in st.session_state:
    print("assign cloud init default")
    
    if len(cloud_init)>0:
        st.session_state["cloud_init_default"] = cloud_init[0]
    else:
        st.session_state["cloud_init_default"] = ""
        
    print(st.session_state["cloud_init_default"])

for vm in vms:
    st.session_state[f"{vm["hostname"]}_view_spec"] = False

## BUTTON ON_CLICK FUNCTION
@st.dialog("Deploy",width="large")
def group_status(group_name):
    #group_name, vm, total

    st.markdown(f"### Group : {group_name}")
    print(f"            >>   {st.session_state["group"]}")
    st.table(st.session_state["group"][g]["data"])

def resolve_cloud_init_vars(parent_st, data):
    _data = {}

    for _d in data["vars"].split(","):
        k,v = _d.split(":")
        _data[k] = v

    _vars = {}
    
    for k,v in _data.items():
        colk , colv = parent_st.columns([3,7])

        edit_val = v in st.session_state["const"]

        default = ""
        if edit_val:
            default = v

        colk.markdown(k)
        _vars[k] = colv.text_input(
                                v,
                                key=f"{data['filename']}_vars_{v}",
                                value=default,
                                label_visibility="collapsed",
                                disabled=edit_val
                            )
    print("VARS == "+repr(_vars))
    return _vars

def dict_to_vars(ls):
    str = ""
    for k,v in ls.items():
        str +=(k +":"+ v+",")
    return str[:-1]

def set_vars(group_name, dict_vars):
    print(f' TEST st.session_state["cloud_init_vm_deployment"] >>> {st.session_state["cloud_init_vm_deployment"]}')
    print(f' GROUP VM BEFORE {group_vm}')
    for k,v in dict_vars.items():
        for hostname,vm_data in group_vm.items():
            for vm in vm_data:
                if vm["hostname"]==k:
                    vm["cloud_init"]['vars'] = dict_to_vars(v) 
    print(f'UPDATE GROUP_VM => {group_vm}')
    return True

def confirm_cloud_init(group_name, vms):
    if st.session_state["cloud_init_default"]=="":
        st.toast("There is no cloud-init file exist !")
    else:
        _confirm_cloud_init(group_name, vms)

@st.dialog("Confirm CLoud Init",width="large")
def _confirm_cloud_init(group_name, vms):
    _, col_ci = st.columns([6,4])

    if st.session_state["cloud_init_default"]=="":
        st.toast("There is no cloud-init file exist !")

    CLOUD_INIT = []
    vms_dict_var = {}

    for _data in cloud_init:
        CLOUD_INIT.append(_data["filename"])
    
    with col_ci:    
        filename = st_smart_text_input(
            label = "cloud init",
            key=f"cloud_init_default_input",
            options=CLOUD_INIT,
            placeholder=st.session_state["cloud_init_default"]["filename"],
            label_visibility="collapsed"
        )
        st.session_state["cloud_init_default"] = api.cloud_init.get_content_by_filename(filename)["response"] if not filename==None else st.session_state["cloud_init_default"]
        print(f"        >>>         {st.session_state["cloud_init_default"]}")
    for vm in vms:
        print(f">>>         VM    {vm}")
        cont = st.container(border=True)

        with cont :
            cont_data = st.container()
            cont_vars = st.container()

            with cont_data :
                col_name, col_cloud_init = st.columns([6,4],vertical_alignment="center")
                
                col_name.markdown(f"# {vm["hostname"]}")
                col_name.markdown("")
                col_name.markdown("")
                col_name.markdown("")
                with col_cloud_init :
                    print(f' VM SOLVING PLACEHOLDER >> {vm}')
                    filename = st_smart_text_input(
                        label = "cloud init",
                        options=CLOUD_INIT,
                        key=f"cloud_init_{vm['hostname']}_input",
                        placeholder=vm["cloud_init"]["filename"],
                        label_visibility="collapsed"
                    )
                    vm["cloud_init"] = api.cloud_init.get_content_by_filename(filename)["response"] if not filename==None else vm["cloud_init"]

            with cont_vars:
                print(f"CONT VARS >>>> {vm["cloud_init"]}")
                vms_dict_var[vm["hostname"]] = resolve_cloud_init_vars(parent_st=cont_vars, data=vm["cloud_init"])
    
    _, col_cancel, col_confirm = st.columns([6,2,2])
    if col_cancel.button(
        "cancel",
    ):
        st.rerun()

    with col_confirm:
        print(f'vm_dict_vars : {vms_dict_var}')
        if button_green(
            text="ok",
            key="confirm_cloud_init_button",
            on_click=set_vars,
            kwargs={
                "group_name" : group_name,
                "dict_vars" : vms_dict_var
            }
        ):
            st.rerun()

group_vm = {}

@st.dialog("Confirm Deployment",width="large")
def confirm_deploy(group_name, group_vm):
    st.markdown(f"Are you sure to deploy {group_name} ?")
    if button_green(
        "deploy",
        on_click=deploy,
        kwargs={"group_name": group_name, "group_vm":group_vm}
    ):
        st.rerun()

    if st.button("cancel_deploy"):
        st.rerun()

def deploy(group_name, group_vm):
    print(f" GROOOOOOOUp VM >>>> {group_vm}")
    status = {}
    for vm in group_vm:
        _vm = vm.copy()
        _cloud_init = _vm["cloud_init"].copy()
        del _vm["cloud_init"]
        print(f'test : {_cloud_init} {_vm}')
        status[vm["name"]] = api.vm_utility.create_vm(_cloud_init,  _vm)

        if status[vm["name"]]["code"]==200:
            _vm["status"]  = "ON"
        else:
            _vm["status"]  = "FAIL"
        
        print("========================= ))")
        print(api.vm.update(_vm["id"], _vm))
        print( status[vm["name"]])


def confirm_validity(group_name, vms, total):
    _vm_list = ""

    for _vm in vms :
        st.session_state["cloud_init_vm"].append(_vm)
        _vm_list += (_vm["hostname"]+", ")
    
    for vm in st.session_state["cloud_init_vm"]:
        vm["cloud_init"] = st.session_state["cloud_init_default"]

    _vm_list = _vm_list[:-2]

    deployment_validity = True
    hostname_validity = ":green[valid]"

    vcpu_validity = ":green[valid]" 
    if total["vcpu"]>=kvm_server["vcpu"] :
        deployment_validity=False 
        vcpu_validity = f":red[invalid (memmory vcpu= {kvm_server['vcpu']})]"
    
    memmory_validity = ":green[valid]"
    if total["memmory"]>=(kvm_server["memmory"]*1024) :
        deployment_validity=False 
        memmory_validity = f":red[invalid (server memmory= {kvm_server['memmory']})]"
    
    disk_validity = ":green[valid]"
    if total["disk"]>=kvm_server["disk"] :
        deployment_validity=False 
        disk_validity=f":red[invalid (Server disk= {kvm_server['disk']})]"

    data = pd.DataFrame(
        {
            "metrics" : ["hostname","total vcpu","total memmory", "total disk"],
            "value" : [_vm_list, total["vcpu"], total["memmory"], total["disk"]],
            "status" :[hostname_validity,vcpu_validity,memmory_validity,disk_validity]
        }
    )

    st.session_state["group"][group_name]["validity"] = deployment_validity
    st.session_state["group"][group_name]["data"] = data
    st.session_state["group"][group_name]["cloud_init"] = st.session_state["cloud_init_default"]

for g in list(st.session_state["group"]):
# list() to handling error : RuntimeError: dictionary changed size during iteration

    ## handling if no request in the group
    any_request = False
    for x in request_vm:
        if g==vm["group_name"]:
            any_request = True

    if any_request:
        group_vm[g] = []
        total_vcpu = 0
        total_memmory = 0
        total_disk = 0

        st.markdown(f"## {g}")

        idx = 0

        col_hostname, col_status, col_ci, col_deploy = st.columns([7,1,1,1])
        with col_hostname:
            col_1, col_2, col_3 = st.columns(3, gap="small")

            for vm in request_vm:
                group_vm[g].append(vm)
                if g==vm["group_name"]:
                    
                    col = ""

                    if idx == 0:
                        col = col_1
                    elif idx == 1:
                        col = col_2
                    else:
                        col = col_3
                        
                    with col :
                        with st.popover(vm["hostname"]):
                            disk = ""
                            for d in disks:
                                if d["vm_id"]==vm["id"]:
                                    disk_size = d["disk_size"]

                            curr_os = None

                            total_vcpu += vm["vcpu"]
                            total_memmory += vm["memmory"]
                            total_disk += disk_size

                            for _os in os:
                                if _os["id"]==vm["os_id"]:
                                    curr_os=_os

                            vm_data = pd.DataFrame(
                                {
                                    "metric" : ["hostname","vcpu","memmory","disk","os"],
                                    "value": [vm["hostname"],vm["vcpu"],f"{vm["memmory"]} Mib",f"{disk_size} Gib",f"{_os['name']} {_os['version']}"]
                                }
                            )
                            st.table(vm_data)

                    idx += 1
                    if idx>=3:
                        idx=0

        confirm_validity(
            group_name=g, 
            vms=group_vm[g],
            total={
                    "vcpu": total_vcpu,
                    "memmory": total_memmory,
                    "disk":total_disk
                    }
        )

        with col_status:
            # button_deploy
            st.button(
                "Status",
                key=f"status_group_{g}",
                on_click=group_status,
                kwargs={"group_name":g},
                use_container_width=True
            )
        
        with col_ci:
            print(f' GROUP VM {group_vm[g]}')
            st.button(
                "Config",
                use_container_width=True,
                key=f"confirm_cloud_init_{g}",
                on_click=confirm_cloud_init,
                kwargs={
                    "group_name":g,
                    "vms": group_vm[g]
                }
            )
        
        print(st.session_state["cloud_init_vm_deployment"])
        
        with col_deploy:
            button_green(
                text="Deploy",
                key="deploy_group_{g}",
                on_click=confirm_deploy,
                kwargs={
                    "group_name":g,
                    "group_vm":group_vm[g]
                }
            )