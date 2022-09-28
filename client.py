from tkinter import *
import httpx
import json

client_name = "Fr"

def config():
    with open("config.json", "r") as E:
        lE = json.load(E)
        return lE

username = f"{config()['user']} ({client_name})"

class server:
    @staticmethod
    def return_message_list():
        config_url = f"{config()['url']}"
        try:
            return httpx.get(f"{config_url}/api/messages").text
        except httpx.ConnectTimeout:
            return "Unable to get messages from server"
    
    @staticmethod
    def send_message(message):
        config_url = f"{config()['url']}"
        httpx.post(f"{config_url}/api/send", headers={"user" : username, "content" : message})
    
    

class client:
    @staticmethod
    def connect():
        config_url = f"{config()['url']}"
        httpx.post(f"{config_url}/api/join", headers={"user" : username})
        return server.return_message_list()

root = Tk()

root.title(f"The Francium Client - {config()['url']}")

config_url = f"{config()['url']}"

message_list = Label(root, text=client.connect(), background=config()["chat-bg"])
entry = Entry(root, width=150)
member_list = Label(root, text="Member list | off")

message_list.grid(row=1, sticky=W)
entry.grid(row=5, sticky=SW)

def mem_list():
    if config()["member_list"] == "on":
        member_list.grid(row=1, column=10, sticky=E)
        member_list.config(text=httpx.get(f"{config()['url']}/api/members").text)
        root.after(10000, mem_list)
        return
        
    else:
        return "Member list | off"
        

def update():
    message_list.config(text=server.return_message_list())
    root.after(1000, update)

def send_message():
        config_url = f"{config()['url']}"
        httpx.post(f"{config_url}/api/send", headers={"user" : username, "content" : entry.get()})

send = Button(text="Send", command=send_message)
send.grid(row=5, column=3, sticky=SW)

root.configure(bg=config()["bg"])
mem_list()
update()
root.mainloop()

#make a function with no arguements
