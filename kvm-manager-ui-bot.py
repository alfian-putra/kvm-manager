import os
import threading

from telebot import TeleBot, types

from ui_bot.lib.common_utility import log, \
                                      config, \
                                      api
from ui_bot.lib.utility import request_vm, \
                                download_file

## CONST
BOT_TOKEN = config["bot"]["token"]
MESSAGE = {}

## VAR
### user
users = api.user.read_all()["response"]
user_session = {} # {"chat_id" : "request"}
### file
tmp_path = os.path.join(os.getcwd(),"ui_bot","tmp")
file_request_vm_example = os.path.join(os.getcwd(),"ui_bot","tmp","request_vm.csv")

## DEFINE BOT OBJECT
Bot = TeleBot(BOT_TOKEN, parse_mode="MarkdownV2")

## Utility
def parse_special_char(str):
    char = ['\\','_', '*', '[', ']', '(', ')', 
            '~', '`', '>', '#', '+', '-', 
            '=', '|', '{', '}', '.', '!',"'",":"]
    for i in char :
        str = str.replace(i, f"\{i}")
    
    return str


## MENU INTERFACE

### common component
button_back_to_main_menu = types.InlineKeyboardButton("back", callback_data="back_to_main_menu")

### menu 
def main_menu():
    button_vm = types.InlineKeyboardButton("virtual Machine", callback_data="vm_menu")
    button_user = types.InlineKeyboardButton("user", callback_data="user_menu")

    main_menu = types.InlineKeyboardMarkup()
    main_menu.add(button_vm)
    main_menu.add(button_user)
    return main_menu

### menu /user
def user_menu():
    button_register = types.InlineKeyboardButton("Sign Up", callback_data="session_userRegister")
    button_change_password = types.InlineKeyboardButton("change password", callback_data="session_userChangePassword")
    button_user_status = types.InlineKeyboardButton("User Detail", callback_data="session_userDetail")

    user_menu = types.InlineKeyboardMarkup()
    user_menu.add(button_register)
    user_menu.add(button_change_password)
    user_menu.add(button_user_status)
    return user_menu

### menu /vm
def vm_menu():
    button_add = types.InlineKeyboardButton("Request VM", callback_data='session_requestVm')

    vm_menu = types.InlineKeyboardMarkup()
    vm_menu.add(button_add)
    vm_menu.add(button_back_to_main_menu)
    return vm_menu

## SESSION HANDLER

### common function
#### menu main
def main_menu_handler(chat_id):
    return Bot.send_message(
            chat_id=chat_id,
            text="*KVM Manager*\n\nWelcome to KVM Manager",
            reply_markup=main_menu()
        )
#### menu vm
def vm_menu_handler(chat_id):
    return Bot.send_message(
            chat_id=chat_id,
            text="*KVM Manager*\n\nSelect vm menu :",
            reply_markup=vm_menu()
        )

#### request vm 
def request_vm_example(chat_id):
    # add user_session = {"user_id" : "request"}
    #print("*Request VM*\\n\\nFill this csv and put request urge as an caption like the example\. use \/cancel to cancel request\\n\n")
    
    # send procedure request message 
    Bot.send_message(
        chat_id=chat_id, 
        text="*Request VM*\n\nFill this csv\. use /cancel to cancel request\n\n", 
        parse_mode="MarkdownV2"
    )

    # send example
    Bot.send_document(
        chat_id=chat_id,
        document=open(file_request_vm_example),
        parse_mode="MarkdownV2"
    )

def sendError(chat_id, error):
    Bot.send_message(
        chat_id=chat_id, 
        text=f"*Error : *\n\n{error}", 
        parse_mode="MarkdownV2"
    )
def request_vm_handler(chat_id, user_id, file_id):
    ## download file
    print(file_id)
    try :
        file = Bot.get_file(file_id)
        filepath = os.path.join(tmp_path, file_id)

        ## handling if file already exist
        if os.path.isfile(filepath):
            os.remove(filepath)
        
        ## download file
        ## THIS : file.file_path
        download_file(bot_token=BOT_TOKEN, file_path=file.file_path, target_filepath=filepath)

    except Exception as e:
        sendError(chat_id, e)
    
    ## add vm data to db
    request_result = request_vm(csv_file=filepath, user_id=user_id)
    
    res = "```\n"

    hostname_length = 0

    for k,v in request_result.items():
        if hostname_length < len(k):
            hostname_length = len(k)
    
    hostname_length += 4

    for k,v in request_result.items():
        hostname = f"{k}"

        space = hostname_length - len(hostname)

        for _ in range(0, space):
            hostname += " "

        res += f"{hostname}{v}\n"
    
    res += "```"
    
    Bot.send_message(
            chat_id=chat_id,
            text=f"*VM request result*\n\n{res}",
            reply_markup=vm_menu(),
        )
    ## 

### Menu handler
@Bot.message_handler(func=lambda message:True)
def menu_handler(message):
    if "/cancel" in message.text:
        user_session[message.chat.id] = ""
        main_menu_handler(message.chat.id)

### File handling
@Bot.message_handler(content_types=['document'])
def handle_docs(message):

    try:
        if user_session[message.from_user.id]=="session_requestVm":
            res = request_vm_handler(message.chat.id, message.from_user.id, message.document.file_id)
    except Exception as e:
        sendError(message.chat.id, e)
### Query Handler
@Bot.callback_query_handler(func=lambda callback:True)
def session_handler(callback):
    if callback.data == "vm_menu":
        vm_menu_handler(callback.from_user.id)
    # register
    if callback.data == "session_requestVm":
        user_session[callback.from_user.id] = "session_requestVm"
        print(user_session[callback.from_user.id])
        request_vm_example(callback.from_user.id)
    elif callback.data == "session_userChangePassword":
        pass
    elif callback.data == "session_userDetail":
        pass
    else :
        pass


## RUN SERVER
def main():
    Bot.polling() # looking for message

def monitoring():
    ## waiting approval whan success deploy or fail will sent 
    while True:
        pass

if __name__ == '__main__':
    t1 = threading.Thread(target=main)
    t2 = threading.Thread(target=monitoring)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Telegram bot started on {}")