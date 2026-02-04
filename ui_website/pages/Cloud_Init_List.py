import json 
from datetime import datetime
import streamlit as st
#from streamlit_monaco import st_monaco
from streamlit_ace import st_ace, THEMES

from ui_website.components.component import button_green

from ui_website.lib.common_utility import api, config

st.set_page_config(layout="wide")
st.markdown("# Cloud Init")

def dict_to_vars(data):
    res = ""
    for k,v in data.items():
        res += f"{k}:{v},"
    return res[:len(res)-1]

def vars_to_dict(str):
    data=str.split(",")
    res = {}

    for _d in data:
        k,v = _d.split(":")
        res[k] = v
    
    return res

# per line : name, open, delete
# open -> make new tab containing open code_editor
def get_timestamp():
    dt = datetime.now()
    return str(datetime.timestamp(dt))

def generate_filename():
    return f"new_file_{get_timestamp()}"

def new_cloud_init_data(): 
    data = {
                "filename" : generate_filename(),
                "content" : "hostname: {{hostname}}\n\n",
                "vars" : {"hostname":"_HOSTNAME"}
            }
    return data

def reload_cloud_init_data():
    st.session_state["cloud_init"] = api.cloud_init.read_all()["response"]
    for id in range(0,len(st.session_state["cloud_init"])):
        filename = st.session_state["cloud_init"][id]["filename"]
        print(f"SEBELUM CONTENT >> {api.cloud_init.get_content_by_filename(filename)}")
        content = api.cloud_init.get_content_by_filename(filename)["response"]["content"]
        st.session_state["cloud_init"][id]["content"] = content
        st.session_state["cloud_init"][id]["vars"] = vars_to_dict(st.session_state["cloud_init"][id]["vars"] )


if "cloud_init" not in st.session_state:
    reload_cloud_init_data()

# session state
def updateTabHeader():
    tabs_header = []
    for d in st.session_state["tabs"]:
        if d=="Cloud Init":
            tabs_header.append(f"**{d}**")
        else:
            tabs_header.append(f":page_facing_up: **{d}**")
    
    st.session_state["tabs_header"] = tabs_header


if not "tabs" in st.session_state:
    st.session_state["tabs"] = ["Cloud Init"]
if not "tabs_header" in st.session_state:
    updateTabHeader()

@st.dialog("Const Value",width="large")
def _const_val():
    const_list = api.cloud_init.const_value()["response"]
    data = {"key":[],"value":[]}
    for k,v in const_list.items():
        data["key"].append(k)
        data["value"].append(v)
    st.table(data)

def _create_tab_code_edit(filename):
    data = {}
    for _data in st.session_state["cloud_init"]:
        if _data["filename"] == filename:
            data = _data
    id = 0
    for i in st.session_state["tabs"]:
        if i==filename:
            break
        id += 1
    _filename = st.text_input("filename",key=f"{data['filename']}_filename",value=data["filename"])
    _col, col_themes = st.columns([9,1])
    _content = st_ace(key=f"{data['filename']}_code",
                      value=data["content"],
                      language="yaml",
                      theme=col_themes.selectbox("Theme",key=f"{data['filename']}_theme",
                                                 placeholder="tomorrow_night",label_visibility="collapsed", options=THEMES, index=35),
                      auto_update=True)

    if st.button("Constant List",key=f"{data['filename']}_const_list"):
        _const_val()
    
    _vars = {}
    for k,v in data["vars"].items():
        colk , colv = st.columns(2)
        _vars[colk.text_input(k,key=f"{data['filename']}_vars_{k}",value=k,label_visibility="collapsed")] = colv.text_input(v,key=f"{data['filename']}_vars_{v}",value=v,label_visibility="collapsed")
    if st.button("add var", key=f"{data['filename']}_var"):
        data["vars"][f"item{len(data["vars"])-1}"] = f"value{len(data["vars"])-1}"
        st.rerun()
    
    new_data = {"filename":_filename, "content":_content, "vars":dict_to_vars(_vars)}
    _ , col_save, col_cancel = st.columns([8,1,1])
    print(f"NEW DATA >>> {new_data}")
    with col_save:
        if button_green(key=f"{data['filename']}_save", text="save"):
            res = {}
            print(api.cloud_init.get_content_by_filename(data["filename"])["code"])
            print(f"404 tes >>> {str(404==api.cloud_init.get_content_by_filename(data["filename"])["code"])}")
            if not 404==api.cloud_init.get_content_by_filename(data["filename"])["code"]:
                print(f"NEWWWWW >>>>>> {json.dumps(new_data)}")
                #id = api.cloud_init.get_content_by_filename(data["filename"])["response"]["id"]
                print(f" RESPONSE >>>> {api.cloud_init.update_content(data["id"],json.dumps(new_data))}")
                res = api.cloud_init.update_content(data["id"],json.dumps(new_data))["response"]
                print(res)
            else:
                res = api.cloud_init.post_content(json.dumps(new_data))["response"] 
            # if res["status"]=="success":
            #     st.success("success")
            # else:
            is_exist = False

            for _data in st.session_state["cloud_init"]:
                if _data["filename"]==data["filename"]:
                    is_exist=True
                
            if not is_exist:
                st.session_state["cloud_init"].append({"filename":_filename,"content":_content,"vars":data["vars"]})
                print(st.session_state["cloud_init"][id])
                for id in range(0, len(st.session_state["tabs"])):
                    if st.session_state["tabs"][id]==_filename:
                        st.session_state["tabs"][id]=_filename
            reload_cloud_init_data()
            del st.session_state["tabs"][id]
            updateTabHeader()
            st.rerun()
    with col_cancel:
        if st.button("Cancel edit",key=f"{data['filename']}_cancel",use_container_width=True):
            del st.session_state["tabs"][id]
            updateTabHeader()
            st.rerun()

def create_tab(tab_name):
    if tab_name == "Cloud Init":
        st.markdown("# Cloud Init")
        # list cloud_init file
        # add button
        id = 0
        for data in st.session_state["cloud_init"]:
            cfilename, cedit, cduplicate, cdelete= st.columns([7,1,1,1])

            cfilename.markdown(data['filename'])
            if cedit.button("edit",key=f"{data['filename']}_edit",use_container_width=True):
                st.session_state["tabs"].append(data["filename"])
                updateTabHeader()
                st.rerun()
            if cduplicate.button("duplicate",key=f"{data['filename']}_duplpicate",use_container_width=True):
                new_data = data.copy()
                new_data["filename"] = f"{new_data["filename"]}_{get_timestamp()}"
                st.session_state["cloud_init"].append(new_data)
                st.session_state["tabs"].append(new_data["filename"])
                updateTabHeader()
                st.rerun()
            
            cdelete.button("delete",key=f"{data['filename']}_delete",on_click=delete_confirmation, kwargs={"id":id,"data":data},use_container_width=True)
            id += 1
        if st.button("add"):
            new_data = new_cloud_init_data()
            st.session_state["tabs"].append(new_data["filename"])
            updateTabHeader()
            st.session_state["cloud_init"].append(new_data)
            st.rerun()
    else :
        _create_tab_code_edit(tab_name)
@st.dialog("Delete")
def delete_confirmation(id, data):
    st.markdown("Are you sure to delete ?")
    _, cdel, ccancel = st.columns([6,2,2])
    if cdel.button("delete"):
        if "id" in data:
            api.cloud_init.delete(data['id'])
        reload_cloud_init_data()
        st.rerun()
    if ccancel.button("cancel"):
        st.rerun()


tabs = st.tabs(st.session_state["tabs_header"])

for id in range(0,len(st.session_state["tabs"])):
    with tabs[id]:
        create_tab(st.session_state["tabs"][id])


