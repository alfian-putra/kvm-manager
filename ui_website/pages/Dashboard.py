from datetime import datetime
import time
import requests
import asyncio

import streamlit as st
import matplotlib.pyplot as plt

from ui_website.lib.common_utility import config

metric_exporter = f"http://{config["monitoring_agent"]["host"]}:{config["monitoring_agent"]["port"]}"

st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

st.markdown("# Dashboard")

plt.style.use('dark_background')

metric = ""
try:
    metric = requests.get(metric_exporter).json()
except Exception as e :
    st.markdown("__Data not found :__")
    st.markdown("Check agent on each server to get server metrics.")


if not metric=="":
    cpu_used = metric["percent_cpu_used"]
    cpu_total = metric["cpu_total"]
    mem_used = metric["percent_memmory_used"]
    uptime = metric["uptime"]

    with st.container():
        st.markdown("### Backend Server - [127.0.0.1]")

        col1, col2, col3, col4 = st.columns([2,2,2,4])

        with col1:
            st.metric("CPU used", f"{cpu_used}%")

        with col2:
            st.metric("CPU Total", f"{cpu_total}")

        with col3:
            st.metric("Memmory used", f"{mem_used}%")

        with col4:
            st.metric("Up time", uptime)

    with st.container():
        st.markdown("### Telegram Bot Server - [127.0.0.1]")

        col1, col2, col3, col4 = st.columns([2,2,2,4])

        with col1:
            st.metric("CPU used", f"{cpu_used}%")

        with col2:
            st.metric("CPU Total", f"{cpu_total}")

        with col3:
            st.metric("Memmory used", f"{mem_used}%")

        with col4:
            st.metric("Up time", uptime)

    with st.container():
        st.markdown("### Web UI Server - [127.0.0.1]")

        col1, col2, col3, col4 = st.columns([2,2,2,4])

        
        with col1:
            st.metric("CPU used", f"{cpu_used}%")

        with col2:
            st.metric("CPU Total", f"{cpu_total}")

        with col3:
            st.metric("Memmory used", f"{mem_used}%")

        with col4:
            st.metric("Up time", uptime)
