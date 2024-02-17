# -*- encoding: utf-8 -*-
'''

        
'''

import OlivOS
import UTLov
from .UTLovWindow import Home
from .ConfigTool import *

import flet
import time
import threading
import re


UTLovv=Home()

# def start(plugin_event,Proc):
#     message=message=plugin_event.data.message
    


def start(plugin_event,Proc):
    message=plugin_event.data.message
    if (message.lower()==".utlov" or message.lower()=="。utlov") and plugin_event.data.user_id==config.data['Master_id']:
        UTLovv.running=True
        flet.app(target=UTLovv.start)
        plugin_event.reply("UTLov已开启...")

def end(plugin_event,Proc):
    message=plugin_event.data.message
    if (message.lower()==".utlov end" or message.lower()=="。utlov end") and plugin_event.data.user_id==config.data['Master_id']:
        plugin_event.reply("UTLov已关闭...\n感谢各位PL以及OBer！")
        time.sleep(5)
        UTLovv.running=False
        UTLovv.close()


def unity_message(plugin_event,Proc):
    message:str
    if plugin_event.data.group_id != config.data["Group_id"]:
        return
    # else:
    #     print(plugin_event.data.group_id)
    #     print(type(plugin_event.data.group_id))
    #     print(config.data["Group_id"])
    message=plugin_event.data.message
    if not UTLovv.running:
        start(plugin_event,Proc)
        return
    else:
        end(plugin_event,Proc)
    if message.strip()=='':
        return
    if ((message.startswith('.') or message.startswith('。')) and not (message.startswith('.sset') or message.startswith('。sset'))) and (not message.startswith('..') or not message.startswith('。。')) and (re.search('^[\.。](\S*?)[\.。]\s*(.*?)$',message) is None):
        return
    user_id=plugin_event.data.user_id
    if user_id in config.PL_list:
        UTLovv.pc_message(user_id,message)
    elif user_id==config.data['KP_id']:
        UTLovv.kp_message(message)
    else:
        UTLovv.ob_message(user_id,message)
    
def if_roll(message):
    return re.search("\d+[dD]\d+",message) is not None


def unity_send(plugin_event,Proc):
    if plugin_event.data.group_id != config.data["Group_id"]:
        return
    # print(message)
    if not UTLovv.running:
        return
    message=plugin_event.data.message
    # print(message)
    UTLovv.bot_message(message)
               
    

class Event(object):
    # def private_message(plugin_event, Proc):
    #     start(plugin_event,Proc)

    def group_message(plugin_event, Proc):
        unity_message(plugin_event,Proc)

    def group_message_sent(plugin_event, Proc):
        unity_send(plugin_event,Proc)


