import streamlit as st
import pandas as pd

from ui_website.lib.common_utility import api, config
from ui_website.components.component import button_status

users = api.user.read_all()["response"]
vms = api.vm.read_all()["response"]
disks = api.disk.read_all()["response"]
os = api.os.read_all()["response"]


st.set_page_config(layout="wide")

st.markdown('## <div style="text-align: center"> VM List </div>', unsafe_allow_html=True)
st.markdown("---")

# VMs = pd.DataFrame(
#     [
#         {
#             "id" : 0,
#             "name" : "VM 1 Debian",
#             "hostname" : "n1.debian",
#             "vcpu" : 1,
#             "memmory" : 2048,
#             "disk_size" : 500,
#             "os_id" : 0,
#             "status" : "ON"
#         },
#                 {
#             "id" : 1,
#             "name" : "VM 2 Debian",
#             "hostname" : "n2.debian",
#             "vcpu" : 1,
#             "memmory" : 2048,
#             "disk_size" : 500,
#             "os_id" : 1,
#             "status" : "OFF"
#         },
#                 {
#             "id" : 2,
#             "name" : "Docker Server",
#             "hostname" : "docker_server.debian",
#             "vcpu" : 1,
#             "memmory" : 2048,
#             "disk_size" : 500,
#             "os_id" : 2,
#             "status" : "ON"
#         },
#     ]
# )

# OS = pd.DataFrame(
#     [
#         {
#             "id":0,
#             "name":"Debian",
#             "version":"8",
#             "iso":"/iso/debian_8.iso",
#             "description":"this is debian 8 iso."
#         },
#         {
#             "id":1,
#             "name":"Debian",
#             "version":"9",
#             "iso":"/iso/debian_8.iso",
#             "qcow2":"/path/to/debian.qcow2",
#             "description":"this is debian 9 iso."
#         },
#         {
#             "id":2,
#             "name":"Fedora",
#             "version":"40",
#             "iso":"/iso/fedora.iso",
#             "description":"this is fedora iso."
#         }
#     ]
# )


## SETUP SESSION VARIABLE
if  'edit_data_vm' not in st.session_state :
    st.session_state.edit_data_vm = True

for vm in vms:
    st.session_state[f"{vm["hostname"]}_view_spec"] = False

## BUTTON ON_CLICK FUNCTION
def toggle_edit_data_vm():
    st.session_state.edit_data_vm = not st.session_state.edit_data_vm

label_visibility = "collapsed"
is_protected = st.session_state.edit_data_vm

col_name, col_hostname, col_spec, col_status = st.columns(4, gap="large")
with st.container():
    with col_name:
        st.markdown('##### <div style="text-align: center"> Name </div>', unsafe_allow_html=True)
    with col_hostname:
        st.markdown('##### <div style="text-align: center"> Hostname </div>', unsafe_allow_html=True)
    with col_spec:
        st.markdown('##### <div style="text-align: center"> Specification </div>', unsafe_allow_html=True)
    with col_status:
        st.markdown('##### <div style="text-align: center"> Status </div>', unsafe_allow_html=True)

for vm in vms:
    col_name, col_hostname, col_spec, col_status = st.columns(4, gap="large")
    
    with col_name:
        st.text_input(label=f"vm[{vm["id"]}].name", value=vm["name"], label_visibility=label_visibility, disabled=is_protected)

    with col_hostname:
        st.text_input(label=f"vm[{vm["id"]}].hostname", value=vm["hostname"], label_visibility=label_visibility, disabled=is_protected)

    with col_spec:
        # def togle_spec_view():
        #     st.session_state[f"{vm.hostname}_view_spec"] = not st.session_state[f"{vm.hostname}_view_spec"]

        # st.button(
        #     label=f"{vm.hostname}_view_spec_button",
        #     help=f"Specification of {vm.name}",
        #     on_click=togle_spec_view
        # )

        # while st.session_state[f"{vm.hostname}_view_spec"]:
        #     pass

        with st.popover("spec", use_container_width=True):
            disk = ""
            for d in disks:
                if d["vm_id"]==vm["id"]:
                    disk_size = d["disk_size"]
            # print("DISK SIZE")
            # print(disk["disk_size"])
            # print(type(disk["disk_size"]))
            st.markdown(f'##### **{vm["name"]}**')
            st.markdown(f'**Hostname :** {vm["hostname"]}')
            st.markdown(f'**vcpu     :** {vm["vcpu"]}')
            st.markdown(f'**Memmory  :** {vm["memmory"]}')
            st.markdown(f'**Disk     :** {disk_size}')
            curr_os = None

            for _os in os:
                if _os["id"]==vm["os_id"]:
                    curr_os=_os
                    
            st.markdown(f'**OS       :** {curr_os["name"]} {curr_os["version"]}')

    with col_status:
        button_status(
            status=vm["status"],
            key=f'vm[{vm["id"]}].status' # vm[0].status
        )
