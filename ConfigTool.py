import configparser

try:
    from .UTLovConfig import *
except:
    from UTLovConfig import *



class Config:
    def __init__(self) -> None:
        self.data=cfg
        self.read_config()
            # self.create_ini()
            # printf("New config.ini file has been created.")
            # self.readini()

    def read_config(self):
        # with open(self.configfile,"r") as load_json:
        #     self.data=json.load(load_json)
        self.PL_list=self.data['PCs']
        self.PL_name_list=[self.get_pc_name(pl) for pl in self.PL_list]
        self.NPC_list=self.data['NPCs']
        # for pl in self.data["PCs"]:
        #     self.PL_list.append(pl["id"])
        pass

    def get_pc_config(self, id):
        if id in self.PL_list:
            # return self.data["PCs"][self.PL_list.index(id)]
            return self.data[id]
        else:
            return False
    
    def get_pc_name(self, id):
        if id in self.PL_list:
            # return self.data["PCs"][self.PL_list.index(id)]['name']
            return self.data[id]['name']
        else:
            return False

    def get_pc_id_from_name(self,name):
        # return self.PL_name_list[self.PL_list.index]
        return self.PL_list[self.PL_name_list.index(name)]


    def update_pc_status(self, pc_id, type, value):
        if type in ['hp','hpmax','mp','mpmax','san','sanmax','status']:
            new_cfg=configparser.ConfigParser()
            new_cfg.optionxform = lambda option: option
            new_cfg.read(self.data['Path']+'{}/userinfo.ini'.format(pc_id), encoding='utf-8')
            # main={}
            # new_cfg['Main']=main
            # # print(self.data[pc_id])
            # for k,v in self.data[pc_id].items():
            #     if not isinstance(v,dict) and k!='avatar' and k!='fig':
            #         new_cfg['Main'][k]=v
            #     else:
            #         new_cfg[k]=v
            new_cfg['status'][type]=value
            with open(self.data['Path']+'{}/userinfo.ini'.format(pc_id),'w', encoding='utf-8') as p:
                new_cfg.write(p)


config=Config()
