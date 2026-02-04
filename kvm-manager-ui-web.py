import streamlit as st
import os
import requests
from common.config import Config
from common.fetch_api import FetchApi

config = Config().config
api = FetchApi()


all_user = api.user.read_all()["response"]
print(len(all_user)==0)
if len(all_user)==0:
     x = api.user.initialize()
     print(x)
pages = [
            st.Page(
                "ui_website/pages/Dashboard.py",
                title="Dashboard",
                icon=":material/analytics:"
            )
            ,
            st.Page(
                "ui_website/pages/User_List.py",
                title="User",
                icon=":material/account_box:"
            )
            ,
            st.Page(
                "ui_website/pages/VM_List.py",
                title="Virtual Machine",
                icon=":material/desktop_windows:"
            )
            ,
            st.Page(
                "ui_website/pages/VM_Request.py",
                title="Request",
                icon=":material/announcement:"
            )
            ,
            st.Page(
                "ui_website/pages/OS_List.py",
                title="OS",
                icon=":material/save:"
            )
            ,
            st.Page(
                "ui_website/pages/Cloud_Init_List.py",
                title="Cloud Init",
                icon=":material/article:"
            )
]

pg = st.navigation(
 pages
)

pg.run()