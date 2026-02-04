import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def _button_color(background_color, text_color, text, key, on_click, type, args=None, kwargs=None):
    _button = None

    with stylable_container(
        key=f"container_{key}",
        css_styles=
        f"button[kind='{type}']"
        "{"
        f"    background-color: {background_color};"
        f"    color: {text_color};"
        "     border: none;"
        "}"
        f"button[kind='{type}']:hover"
        "{"
        f"    background-color: rgba(0, 0, 0, 0.5);"
        f"    color: {background_color};"
        f"    border: none;"
        "}"
    ):
        if on_click==None:
            _button = st.button(text, key=key, type=type, use_container_width=True)
        else:
            if not kwargs==None:
                _button = st.button(text, key=key, type=type, on_click=on_click, kwargs=kwargs, use_container_width=True)
            elif not args==None:
                _button = st.button(text, key=key, type=type, on_click=on_click, args=args, use_container_width=True)
            else:
                _button = st.button(text, key=key, type=type, on_click=on_click, use_container_width=True)
    return _button

def button_status(status, key, on_click=None):
    button = None

    color_scheme = {
        "ON" : {
            "color" : "#319e33ff",
            "background-color" : "#319e33ff",
            "text-color" : "white"
        },
        "REQUEST" : {
            "color" : "#ffa92aff",
            "background-color" : "#ffa92aff",
            "text-color" : "white"
        },
        "OFF" : {
            "color" : "#ef524fff",
            "background-color" : "#ef524fff",
            "text-color" : "white"
        },
        "FAIL" : {
            "color" : "#cb4343ff",
            "background-color" : "#cb4343ff",
            "text-color" : "white"
        }
    }

    return _button_color(
        background_color=color_scheme[status]["background-color"], 
        text_color=color_scheme[status]["text-color"], 
        text=status.lower(), 
        key=key, 
        on_click=on_click,
        type='primary'
    )

def button_green(key, text="Deploy", on_click=None, kwargs=None):
    print(repr(kwargs))
    return _button_color(
        text=text,
        background_color="#319e33ff", 
        text_color="white", 
        key=key, 
        on_click=on_click,
        type='primary',
        kwargs=kwargs
    )

