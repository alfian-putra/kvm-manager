import os
import json
import asyncio

import pandas as pd
import streamlit as st
from streamlit_smart_text_input import st_smart_text_input

from ui_website.lib.common_utility import api, config


st.set_page_config(layout="wide")

LIST_OS_RECOMMENDATION = ['AlmaLinux', 'Alpine Linux', 'ALT StarterKits', 'ALT regular', 'ALT', 'Mandrake RE Spring', 
                          'ALT Linux', 'Android-x86', 'Arch Linux', 'Asianux unknown', 'Asianux Server', 
                          'SUSE CaaS Platform Unknown', 'SUSE CaaS Platform', 'CentOS Stream', 'CentOS', 
                          'Circle Linux Unknown', 'Circle Linux', 'CirrOS', 'Clear Linux OS', 'Debian GNU/Linux', 
                          'Debian', 'Debian testing', 'DragonFlyBSD', 'Elementary OS', 'Endless OS', 'EuroLinux', 
                          'Fedora CoreOS', 'Fedora ELN', 'Fedora Rawhide', 'Fedora', 'Fedora Core', 'Fedora Linux', 
                          'FreeBSD', 'FreeDOS', 'Freenix', 'Gentoo Linux', 'GNOME', 'Guix', 'Guix Hurd Latest', 
                          'Guix latest', 'Haiku Nightly', 'Haiku R1', 'Hyperbola', 'Generic Linux', 'MacOS X', 
                          'Mageia', 'Mandrake Linux', 'Mandriva Linux', 'Manjaro', 'Mandriva Business Server', 
                          'Mandriva Enterprise Server', 'MIRACLE LINUX', 'Microsoft MS-DOS', 'NetBSD', 'Novell Netware', 
                          'NixOS', 'NixOS Unstable', 'Oracle Enterprise Linux', 'Oracle Linux', 'OmniOSCE Bloody', 'OpenBSD', 
                          'OpenIndiana Hipster', 'OpenSolaris', 'openSUSE', 'openSUSE Leap', 'openSUSE Tumbleweed', 'Pop!_OS', 
                          'PureOS', 'Red Hat Enterprise Linux Atomic Host', 'Red Hat Enterprise Linux Unknown', 
                          'Red Hat Enterprise Linux', 'Red Hat Linux', 'Rocky Linux Unknown', 'Rocky Linux', 'Scientific Linux', ''
                          'Fedora Silverblue Rawhide', 'Fedora Silverblue', 'Slackware -current', 'Slackware', 
                          'SUSE Linux Enterprise Unknown', 'SUSE Linux Enterprise', 'SUSE Linux Enterprise Desktop', 
                          'SUSE Linux Enterprise Micro', 'SUSE Linux Enterprise Server', 'Triton SmartOS', 'Solaris', 
                          'Oracle Solaris', 'Trisquel', 'Ubuntu', 'Univention Corporate Server', 'Unknown', 'Void Linux', 
                          'Microsoft Windows', 'Microsoft Windows Server', 'Microsoft Windows Millennium Edition', 
                          'Microsoft Windows NT Server', 'Microsoft Windows Vista', 'Microsoft Windows XP']
os_list = api.os.read_all()["response"]

if not "mode" in st.session_state:
    st.session_state.mode = "list"

def update_os_list():
    os_list = api.os.read_all()["response"]

def change_mode_toggle():
    if st.session_state.mode=="list":
        st.session_state.mode = "add"
    else:
        st.session_state.mode = "list"

def download_or_add(os_data):
    _os_data = os_data.copy()
    filename = f'{_os_data["name"]}_{_os_data["version"]}.qcow2'
    if _os_data['download'] and (_os_data["qcow2"][0:4]=="http"):
        download = api.vm_utility.download_os(_os_data['qcow2'],filename)
        if download['response']==200:
            _os_data["qcow2"] = download["response"]["filepath"]
            st.toast("qcow2 download successfully")
        else:
            st.toast(f"ERROR : {download['response']}")
    elif os_data['download'] and not (_os_data["qcow2"][0:4]=="http"):
        err = SyntaxError("Invalid url", "Valid url must be start with protocol http or https")
        st.exception(err)
        return 
    else :
        del _os_data["download"]
    
    _data = {
        'name' : _os_data["name"],
        'version' : _os_data["version"],
        'qcow2' : os.path.join(config["kvm"]["pool"]["path"],filename),
        'description' : _os_data["description"]
    }

    data = json.dumps(_data)
    st.session_state.mode=="list"

    return api.os.create(data)["response"]

async def update(os_data):

    _os_data = os_data.copy()
    filename = f'{_os_data["name"]}_{_os_data["version"]}.qcow2'
    
    print(f"filename {filename}")
    if _os_data['download'] and (_os_data["qcow2"][0:4]=="http"):
        download = api.vm_utility.download_os(os_download=_os_data['qcow2'],filename=filename)
        if download['response']==200:
            _os_data["qcow2"] = download["response"]["filepath"]
            st.toast("qcow2 download successfully")
            st.session_state.mode="list"
            st.rerun()
        else:
            st.toast(f"ERROR : {download['response']}")
    elif os_data['download'] and not (_os_data["qcow2"][0:4]=="http"):
        err = SyntaxError("Invalid url", "Valid url must be start with protocol http or https")
        st.exception(err)
        return 
    else :
        del _os_data["download"]

    _os_data["qcow2"] = os.path.join(config["kvm"]["pool"]["path"], os_data["qcow2"])
    
    _data = {
        'name' : _os_data["name"],
        'version' : _os_data["version"],
        'qcow2' : filename,
        'description' : _os_data["description"]
    }
    data = json.dumps(_data)
    st.session_state.mode=="list"
    print(data)
    return api.os.update(_os_data['id'], data)["response"]

@st.dialog("Add OS")
def add():
    os_data = {}
    st.markdown('## <div style="text-align: center"> Add OS </div>', unsafe_allow_html=True)
    os_data["name"] = st_smart_text_input(
        label="Name",
        options=LIST_OS_RECOMMENDATION
    )
    os_data["version"] = st.text_input(
        label="Version",
        key="os_version"
    )
    os_data["download"] = not st.toggle("existing qcow2", help=f"qcow2 should be exist on {config['kvm']['pool']['path']}")
    os_data["qcow2"] = st.text_input(
        label="Path of qcow2 | Download link to qcow2",
        key="qcow2",
        help=f"qcow2 should be exist on {config['kvm']['pool']['path']}",
    )
    os_data["description"] = st.text_area(
        label="description",
        key="os_description"
    )
    col_add, col_cancel = st.columns(2)
    with col_add:
        if st.button(
                        label="submit",
                        help="submit OS data",
                        on_click=download_or_add,
                        kwargs={"os_data" : os_data}
            ):
            st.session_state.mode="list"
            st.rerun()
    with col_cancel:
        if st.button(
                        label="cancel",
                        help="cancel adding OS data",
                        on_click=change_mode_toggle
            ):
            st.session_state.mode="list"
            st.rerun()

@st.dialog("Edit OS data")
def edit_os(data):
    _os_data = data.copy()
    
    _os_data["name"] = st.text_input(
        label="Name",
        value=_os_data["name"]
    )
    _os_data["version"] = st.text_input(
        label="Version",
        value=_os_data["version"],
        key="os_version"
    )
    _os_data["download"] = not st.toggle("existing qcow2", value=True, help=f"qcow2 should be exist on {config['kvm']['pool']['path']}")
    _os_data["qcow2"] = st.text_input(
        label="Path of qcow2 | Download link to qcow2",
        value=_os_data["qcow2"],
        key="qcow2",
        help=f"qcow2 should be exist on {config['kvm']['pool']['path']}"
    )
    col_add, col_cancel = st.columns(2)
    with col_add:
        if st.button(
                        label="submit",
                        help="submit OS data",
                        on_click=update,
                        kwargs={"os_data" : _os_data}
            ) :
            st.session_state.mode="list"
            st.rerun()
    with col_cancel:
        st.button(
                    label="cancel",
                    help="cancel adding OS data",
                    on_click=change_mode_toggle
        )
        

@st.dialog("Delete OS data")
def delete_os_form(os_data):
    target = f'{os_data['name']} {os_data['version']}'
    st.markdown(f"To confirm deletion, re-type '{target}'")
    confirm = st.text_input(
        label="confirm",
        label_visibility="collapsed"
    ) == target

    col_del, col_cancel, _ = st.columns([2,2,6])

    with col_del:
        _delete =  st.button(
                        label="delete",
                        on_click=delete_os,
                        kwargs={'confirm':confirm, 'os_id':os_data["id"]}
                    )
    with col_cancel:
        if st.button(label="cancel"):
            st.session_state.mode="list"
            st.rerun()

    if _delete:
        if confirm :
            st.session_state.mode="list"
            st.rerun()  
        else :
            st.error("Unmatch target deletion and input !")
                  

def delete_os(confirm, os_id):
    if confirm:
        res = api.os.delete(os_id)
        return res["response"]["status"]
    return False
    

if st.session_state.mode=="list":
    st.markdown('## <div style="text-align: center"> OS List </div>', unsafe_allow_html=True)
    st.markdown("---")

    col_name, col_version, col_qcow2, col_desc, col_edit, col_delete = st.columns([2,1,2,3,1,1])
    with col_name:
        st.markdown('##### <div style="text-align: center"> name </div>', unsafe_allow_html=True)
    with col_version:
        st.markdown('##### <div style="text-align: center"> version </div>', unsafe_allow_html=True)
    with col_qcow2:
        st.markdown('##### <div style="text-align: center"> qcow2 </div>', unsafe_allow_html=True)
    with col_desc:
        st.markdown('##### <div style="text-align: center"> description </div>', unsafe_allow_html=True)
    with col_edit:
        st.markdown('##### <div style="text-align: center"> edit </div>', unsafe_allow_html=True)
    with col_delete:
        st.markdown('##### <div style="text-align: center"> delete </div>', unsafe_allow_html=True)

    for _os in os_list:
        col_name, col_version, col_qcow2, col_desc, col_edit, col_delete = st.columns([2,1,2,3,1,1], vertical_alignment="center")
        with col_name :
            ##st.text_input(label=f"user[{_os["id"]}].name", value=_os["name"], label_visibility="collapsed", disabled=True)
            st.markdown(_os["name"])
        with col_version :
            ##st.text_input(label=f"user[{_os["id"]}].version", value=_os["version"], label_visibility="collapsed", disabled=True)
            st.markdown(_os["version"])
        with col_desc:
            ##st.text_input(label=f"user[{_os["id"]}].description", value=_os["description"], label_visibility="collapsed", disabled=True)
            st.markdown(_os["description"])
        with col_qcow2 :
            ##st.text_input(label=f"user[{_os["id"]}].qcow2", value=_os["qcow2"], label_visibility="collapsed", disabled=True)
            st.markdown(_os["qcow2"])
        with col_edit:
            st.button(
                    label="edit",
                    key=f"user[{_os['id']}].edit",
                    help="Edit data",
                    use_container_width=True,
                    on_click=edit_os,
                    kwargs={"data":_os}
                )
        with col_delete:
            st.button(
                    label="delete",
                    key=f"user[{_os['id']}].delete",
                    help="Delete data",
                    use_container_width=True,
                    on_click=delete_os_form,
                    kwargs={"os_data":_os}
                )

    st.button(
                label="Add",
                help="Add OS data",
                on_click=change_mode_toggle
    )

else:
    add()