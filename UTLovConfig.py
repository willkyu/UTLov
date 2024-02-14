import os
import configparser
import requests
import re

cfg={
    "Path":"C://willkyu/.TRPG/UTLov/data/"
    }

def mkdir(path):
    path=re.search("^(.*)/.*?$",path).group(1)
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

def download_avatar(self_id,path):
    qqimgurl = 'https://q2.qlogo.cn/headimg_dl?dst_uin='+self_id+'&spec=640&img_type=jpg'
    response = requests.get(qqimgurl)
    response = response.content
    mkdir(path)
    with open(path,'wb') as p:
        p.write(response)

class ConfigReader():
    def __init__(self, path) -> None:
        self.path=path
        self.result={}
        if not os.path.exists(self.path+'UTLov.ini'):
            cfg['Path']+='/'
            self.path=path
            if not os.path.exists(self.path+'UTLov.ini'):
                print("Wrong path!")
                return
            # return False
        self.config = configparser.ConfigParser()
        self.config.optionxform = lambda option: option
        self.config.read(self.path+'UTLov.ini', encoding='utf-8')
        self.read_from_config()
        # print(self.result)
        self.get_dice_bot_config()

        # get pl list
        self.PL_list=[]
        for dic in os.listdir(self.path):
            if (not os.path.isfile(os.path.join(self.path,dic))) and dic.isdigit() and len(dic)>=5 and dic!=self.result["KP_id"]:
                self.PL_list.append(dic)

        # get npc list
        self.NPC_list=[]
        for dic in os.listdir(self.path+'npc/'):
            if (not os.path.isfile(os.path.join(self.path+'npc/',dic))) and (not dic.isdigit()) and dic not in ['dice_bot','ob','bg']:
                self.NPC_list.append(dic)
        
        self.result['PCs']=self.PL_list
        self.result['NPCs']=self.NPC_list
        self.get_pl_config()
        self.get_npc_config()
        # print(self.result)
        self.convert_int()
        self.update_avatar_and_fig()
        

    def get_dice_bot_config(self):
        path=self.path+'dice_bot_avatar'
        if os.path.isfile(path+'.jpg'):
            self.result['dice_bot']={'avatar':path+'.jpg'}
        elif os.path.isfile(path+'.png'):
            self.result['dice_bot']={'avatar':path+'.png'}

    def get_pl_config(self):
        for pl in self.PL_list:
            self.config = configparser.ConfigParser()
            self.config.optionxform = lambda option: option
            self.config.read(self.path+pl+'/userinfo.ini', encoding='utf-8')
            self.result[pl]={}
            for sec in self.config.sections():
                if sec == 'Main':
                    self.result[pl].update(self.config[sec])
                else:
                    self.result[pl][sec]=dict(self.config[sec])
    
    def get_npc_config(self):
        self.config = configparser.ConfigParser()
        self.config.optionxform = lambda option: option
        self.config.read(self.path+'npc/default_male.ini',encoding='utf-8')
        self.result['default_male']={'audio':dict(self.config['audio'])}
        self.config = configparser.ConfigParser()
        self.config.optionxform = lambda option: option
        self.config.read(self.path+'npc/default_female.ini',encoding='utf-8')
        self.result['default_female']={'audio':dict(self.config['audio'])}
        if os.path.exists(self.path+'npc/default_male.jpg'):
            self.result['default_male']['fig']=self.path+'npc/default_male.jpg'
        elif os.path.exists(self.path+'npc/default_male.png'):
            self.result['default_male']['fig']=self.path+'npc/default_male.png'
        if os.path.exists(self.path+'npc/default_female.jpg'):
            self.result['default_female']['fig']=self.path+'npc/default_female.jpg'
        elif os.path.exists(self.path+'npc/default_female.png'):
            self.result['default_female']['fig']=self.path+'npc/default_female.png'
        

        for npc in self.NPC_list:
            self.config = configparser.ConfigParser()
            self.config.optionxform = lambda option: option
            print(self.NPC_list)
            # if os.path.exists
            self.config.read(self.path+'/npc/{}/audio.ini'.format(npc),encoding='utf-8')
            self.result[npc]={'audio':dict(self.config['audio'])}
            if os.path.exists(self.path+'npc/{}/avatar.jpg'.format(npc)):
                self.result[npc]['avatar']=self.path+'npc/{}/avatar.jpg'.format(npc)
            elif os.path.exists(self.path+'npc/{}/avatar.png'.format(npc)):
                self.result[npc]['avatar']=self.path+'npc/{}/avatar.png'.format(npc)
            if os.path.exists(self.path+'npc/{}/fig.jpg'.format(npc)):
                self.result[npc]['fig']=self.path+'npc/{}/fig.jpg'.format(npc)
            elif os.path.exists(self.path+'npc/{}/avatar.png'.format(npc)):
                self.result[npc]['fig']=self.path+'npc/{}/fig.png'.format(npc)
            
    def read_from_config(self):
        for sec in self.config.sections():
            # print('111')
            # print(self.result)
            if sec == 'Main':
                self.result.update(self.config[sec])
            else:
                self.result[sec]=dict(self.config[sec])
    
    def convert_int(self):
        for key,value in self.result['KP_audio'].items():
            self.result['KP_audio'][key]=eval(value)
        for pl in self.PL_list:
            for key,value in self.result[pl]['audio'].items():
                self.result[pl]['audio'][key]=eval(value)

    def update_avatar_and_fig(self):
        self.result[self.result['KP_id']]={'audio':self.result['KP_audio']}
        if os.path.exists(self.path+'{}/avatar.jpg'.format(self.result['KP_id'])):
            self.result[self.result['KP_id']]['avatar']=self.path+'{}/avatar.jpg'.format(self.result['KP_id'])
        elif os.path.exists(self.path+'{}/avatar.png'.format(self.result['KP_id'])):
            self.result[self.result['KP_id']]['avatar']=self.path+'{}/avatar.png'.format(self.result['KP_id'])
        else:
            download_avatar(self.result['KP_id'],self.path+'{}/avatar.jpg'.format(self.result['KP_id']))
            self.result[self.result['KP_id']]['avatar']=self.path+'{}/avatar.jpg'.format(self.result['KP_id'])
        
        # fig
        if os.path.exists(self.path+'{}/fig.jpg'.format(self.result['KP_id'])):
            self.result[self.result['KP_id']]['fig']=self.path+'{}/fig.jpg'.format(self.result['KP_id'])
        elif os.path.exists(self.path+'{}/fig.png'.format(self.result['KP_id'])):
            self.result[self.result['KP_id']]['fig']=self.path+'{}/fig.png'.format(self.result['KP_id'])
        else:
            self.result[self.result['KP_id']]['fig']=self.result[self.result['KP_id']]['avatar']

        for pl in self.PL_list:
            # avatar
            if os.path.exists(self.path+'{}/avatar.jpg'.format(pl)):
                self.result[pl]['avatar']=self.path+'{}/avatar.jpg'.format(pl)
            elif os.path.exists(self.path+'{}/avatar.png'.format(pl)):
                self.result[pl]['avatar']=self.path+'{}/avatar.png'.format(pl)
            else:
                download_avatar(pl,self.path+'{}/avatar.jpg'.format(pl))
                self.result[pl]['avatar']=self.path+'{}/avatar.jpg'.format(pl)
            
            # fig
            if os.path.exists(self.path+'{}/fig.jpg'.format(pl)):
                self.result[pl]['fig']=self.path+'{}/fig.jpg'.format(pl)
            elif os.path.exists(self.path+'{}/fig.png'.format(pl)):
                self.result[pl]['fig']=self.path+'{}/fig.png'.format(pl)
            else:
                self.result[pl]['fig']=self.result[pl]['avatar']
        
        for npc in self.NPC_list:
            # avatar
            if os.path.exists(self.path+'npc/{}/avatar.jpg'.format(npc)):
                self.result[npc]['avatar']=self.path+'npc/{}/avatar.jpg'.format(npc)
            elif os.path.exists(self.path+'npc/{}/avatar.png'.format(npc)):
                self.result[npc]['avatar']=self.path+'npc/{}/avatar.png'.format(npc)
            elif os.path.exists(self.path+'npc/default_avatar.jpg'):
                # download_avatar(pl,self.path+'{}/avatar.jpg'.format(pl))
                self.result[npc]['avatar']=self.path+'npc/default_avatar.jpg'
            elif os.path.exists(self.path+'npc/default_avatar.png'):
                # download_avatar(pl,self.path+'{}/avatar.jpg'.format(pl))
                self.result[npc]['avatar']=self.path+'npc/default_avatar.png'

            # fig
            if os.path.exists(self.path+'npc/{}/fig.jpg'.format(npc)):
                self.result[npc]['fig']=self.path+'npc/{}/fig.jpg'.format(npc)
            elif os.path.exists(self.path+'npc/{}/fig.png'.format(npc)):
                self.result[npc]['fig']=self.path+'npc/{}/fig.png'.format(npc)
            # elif os.path.exists(self.path+'npc/default_fig.jpg'):
            #     # download_fig(pl,self.path+'{}/fig.jpg'.format(pl))
            #     self.result[npc]['fig']=self.path+'npc/default_fig.jpg'
            # elif os.path.exists(self.path+'npc/default_fig.png'):
            #     # download_fig(pl,self.path+'{}/fig.jpg'.format(pl))
            #     self.result[npc]['fig']=self.path+'npc/default_fig.png'

        pass
        
        

cfg.update(ConfigReader(cfg["Path"]).result)
