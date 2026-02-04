import os
import json
import pandas as pd
import streamlit as st

from ui_website.lib.common_utility import api, config

users = api.user.read_all()["response"]
vms = api.vm.read_all()["response"]


st.set_page_config(layout="wide")

st.markdown("# User List")
st.markdown("")
## SETUP SESSION VARIABLE
if  'edit_data_user' not in st.session_state :
    st.session_state.edit_data_user = True

## BUTTON ON_CLICK FUNCTION
def toggle_edit_data_user():
    st.session_state.edit_data_user = not st.session_state.edit_data_user

def submit_data():
    pass

## DUMMY DATA
# all_vm = [1,2,3,4,5,6,7,8,9,10]
# data = pd.DataFrame(
#         [
#             {
#                 "id" : 0,
#                 "name" : "admin name",
#                 "password" : "p4ss",
#                 "user_id": "7890",
#                 "role": "admin",
#                 "vm_id": [
#                     1,
#                     2
#                 ]
#             },
#             {
#                 "id" : 1,
#                 "name" : "user name",
#                 "password" : "p4ss",
#                 "user_id": "7890",
#                 "role": "user",
#                 "vm_id": [
#                     1,
#                     2
#                 ]
#             },
#             {
#                 "id" : 2,
#                 "name" : "user name1",
#                 "password" : "p4ss",
#                 "user_id": "7890",
#                 "role": "user",
#                 "vm_id": [
#                     1,
#                     2
#                 ]
#             }
#         ]
# ).drop(
#     columns=["password"], 
#     axis=1
# )


# vm = pd.DataFrame(
#     [
#         {
#             "id" : 0,
#             "name" : "VM 1 Debian",
#             "hostname" : "n1.debian",
#             "vcpu" : 1,
#             "memmory" : 2048,
#             "disk_size" : 500,
#             "os" : "debian",
#             "status" : "ON"
#         },
#                 {
#             "id" : 1,
#             "name" : "VM 2 Debian",
#             "hostname" : "n2.debian",
#             "vcpu" : 1,
#             "memmory" : 2048,
#             "disk_size" : 500,
#             "os" : "fedora",
#             "status" : "ON"
#         },
#                 {
#             "id" : 2,
#             "name" : "Docker Server",
#             "hostname" : "docker_server.debian",
#             "vcpu" : 1,
#             "memmory" : 2048,
#             "disk_size" : 500,
#             "os" : "debian",
#             "status" : "ON"
#         },
#     ]
# )


ROLE = ["ADMIN","USER"]
VM_LIST = {}
VM = []

# for id,vm in vm.iterrows():
#     VM_LIST[vm["id"]] = vm["name"]
#     VM.append(vm["name"])
@st.dialog("Edit user data")
def edit_user(user):
    user["name"] = st.text_input(
        label="name",
        value=user["name"]
    )

    user["username"] = st.text_input(
        label="username",
        value=user["username"]
    )

    user["user_id"] = st.text_input(
        label="user_id",
        value=user["user_id"]
    )

    default = ROLE.index(user["role"])
    user["role"] = st.selectbox(
            label="role",
            index=default,
            options=ROLE
        )
    
    col_edit, col_cancel = st.columns(2)

    with col_edit:
        if st.button(
                        label="submit",
                        help="submit user data",
                        on_click=edit_user_util,
                        kwargs={"user" : user}
            ):
            st.rerun()
    with col_cancel:
        if st.button(
                        label="cancel",
                        help="cancel adding user data",
            ):
            st.rerun()

def edit_user_util(user):
    print(json.dumps(user))
    return api.user.update(user["id"], json.dumps(user))['code']==200

@st.dialog("Add user data")
def add_user():
    user = {}
    user["name"] = st.text_input(
        label="name",
    )

    user["username"] = st.text_input(
        label="username",
    )

    user["password"] = st.text_input(
        label="password",
    )

    user["user_id"] = st.text_input(
        label="user_id",
    )

    user["role"] = st.selectbox(
            label="role",
            options=ROLE
        )
    
    col_edit, col_cancel = st.columns(2)

    with col_edit:
        if st.button(
                        label="submit",
                        help="submit user data",
                        on_click=add_user_util,
                        kwargs={"user" : user}
            ):
            st.rerun()
    with col_cancel:
        if st.button(
                        label="cancel",
                        help="cancel adding user data",
            ):
            st.rerun()

def add_user_util(user):
    user["password"] = api.user.hash_password(user["password"])["response"]
    print(json.dumps(user))
    return api.user.create(json.dumps(user))['code']==200

@ st.dialog("Delete user data")
def delete_user():
    pass

def delete_user_util():
    pass

## SETUP TABLE

with st.container(border=False):
    col_name, col_user_id, col_role, col_edit, col_delete = st.columns(5,vertical_alignment='center')
    
    with col_name:
        st.markdown("**:grey[Name]**")
    with col_user_id:
        st.markdown("**:grey[Telegram ID]**")
    with col_role:
        st.markdown("**:grey[Role]**")
    with col_edit:
        st.markdown("")
    with col_delete:
        st.markdown("")
    st.html("<hr style='height:0.25px;color:gray;'>")

for user in users :
    #col_id, 
    col_name, col_user_id, col_role, col_edit, col_cancel = st.columns(5)
    is_protected = st.session_state.edit_data_user
    label_visibility = "collapsed"
    # with col_id:
    #     st.markdown(user["id"])
    with col_name:
        st.markdown(user["name"])
        #st.text_input(label=f"user[{user["id"]}].name", value=user["name"], label_visibility=label_visibility, disabled=is_protected)
    with col_user_id:
        st.markdown(user["user_id"])
        #st.text_input(label=f"user[{user["id"]}].user_id", value=user["user_id"], label_visibility=label_visibility, disabled=is_protected)
    with col_role:
        default = ROLE.index(user["role"])
        #print(user["role"])
        st.markdown(user["role"])
        # st.selectbox(
        #     label_visibility=label_visibility,
        #     label=f"user[{user["id"]}].role",
        #     index=default,
        #     options=ROLE,
        #     disabled=is_protected
        # )
    with col_edit:
        st.button(
            key=f"edit_{user['id']}",
            label="edit",
            help="edit data",
            on_click=edit_user,
            kwargs={"user":user},
            use_container_width=True
        )

    with col_cancel:
        st.button(
            key=f"cancel_{user['id']}",
            label="delete",
            help="delete data",
            on_click=delete_user,
            kwargs={"user":user},
            use_container_width=True
        )

st.button(
    label="add",
    help="add data",
    on_click=add_user
)

# st.write(
#     """<style>
#     [data-testid="stHorizontalBlock"] {
#         align-items: flex-end;
#         height: 20px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )



# ls_vm_user = []

# for index, user in data.iterrows() :
#     user_vm_option = st.multiselect(
#         "VM maintained by user :",
#         all_vm,
#         key=index,
#         default=user["vm_id"]
#     )

#     ls_vm_user.append(user_vm_option)

# data["vm"] = ls_vm_user

# ls_t = []
# for index, user in data.iterrows() :
#     ls_t.append(st.markdown("# TEST !"))
# # data["ls_t"] = ls_t
# print(data)

# st.data_editor(
#     data, 
#     column_config={
#         "role": st.column_config.SelectboxColumn(
#             options=[
#                 "admin",
#                 "user"
#             ]
#         ),
#         "vm_id" : st.column_config.ListColumn(

#         )
#     }
# )

# st.table(data)

# @st.dialog("Cast your vote")
# def vote(user):
#     vm = st.multiselect(
#         f"VM maintained by {user} :",
#         all_vm,
#         default=[1,2]
#     )
#     if st.button("Submit"):
#         st.session_state.edit_vm = {"user": user, "vm_id": vm}
#         st.write(st.session_state.edit_vm)
#         st.rerun()

# if "vote" not in st.session_state:
#     st.write("Vote for your favorite")
#     if st.button("Edit VM list"):
#         vote("user1")
# else:
#     f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"

# st.write(st.session_state.edit_vm)
