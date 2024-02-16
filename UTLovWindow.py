import flet
from queue import Queue
import threading
import re
import time
from playsound import playsound

try:
    from .PlaySound import SoundPlayer
    from .ConfigTool import *
    # from .PCs_info import PCs_info
    from .MyUI import *
except:
    from PlaySound import SoundPlayer
    from ConfigTool import *
    # from PCs_info import PCs_info
    from MyUI import *

class Home():
    """Home page of UTLov
    """

    def __init__(self) -> None:
        super().__init__()
        self.running=False
        pass

    def init(self):
        self.sound_player=SoundPlayer()
        self.page.title="UTLov on "+config.data['Group_id']
        self.page.window_width=1920
        self.page.window_height=1080

        # self.PCs_info=PCs_info(config.PL_list)

        self.ui=ft.Row(spacing=20)
        self.left=ft.Column(width=380, spacing=20)
        self.right=ft.Column(expand=1,spacing=20)

        # 1名字 3原因 4结果表达式
        self.dice_rd=re.compile('\[(.*?)\](由于\[(.*?)\])*掷骰: (\d+D\d+=\d*)')
        
        # 1名字 2技能名 3技能成功率 4结果表达式
        self.dice_ra=re.compile('\[(.*?)\]进行技能\[(.*?):(\d*?)\]检定: (\d+D\d+=\d*)')
        
        # 1名字 3原因 4bp 5第一次表达式 6第二次十位 7结果
        self.dice_rbp=re.compile('\[(.*?)\](由于\[(.*?)\])*掷骰: (b|p|B|P)\D*?(\d+?D\d+?=\d+?) \D*?\[(\d+?)\].*?=(\d+)')

        # 1名字 2技能名 3技能成功率 4BP 5第一次表达式 6第二次十位 7结果
        self.dice_rbpa=re.compile('\[(.*?)\]进行技能\[(.*?):(\d*?)\]检定: (b|p|B|P)\D*?(\d+?D\d+?=\d+?) \D*?\[(\d+?)\].*?=(\d+)')

        # 1名字 2类型 3结果表达式
        self.st=re.compile('\s*\[(.*?)\]的.*?\s*\[(.*?)\]:\s*(.*?)$')

        # 1名字
        self.dice_rh=re.compile('\[(.*?)\]掷暗骰')

        # 1名字 2原始值 3sc表达式 4san减少表达式 5结果
        # "[焦糖色]进行理智检定[50]: 1D100=45 成功了！ 理智减少1=1点,当前剩余[49]点"
        self.sc=re.compile('\[(.*?)\]进行理智检定\[(.*?)\]:\s*(\d+D\d+=\d*?)\D*\s*理智减少(.*?)点,当前剩余\[(.*?)\]')

        self.dice_res=re.compile('(.*?)=(.*?)$')

        self.kp_npc=re.compile('^[\.。](\S*?)[\.。]\s*(.*?)$')

        self.set_pc_status=re.compile('^[\.。]sset\s*(.*?)\s+(.*?)$')
        


    def start(self, page: flet.Page):
        self.page=page
        self.init()

        # Dice
        self.dice=MyDice()
        self.page.add(self.dice)

        # Background
        padding=20
        self.bg=flet.Container(
                image_src=config.data["Path"]+"bg/bg.png",
                image_fit=flet.ImageFit.CONTAIN,
                expand=True,
                content=flet.Container(
                    padding=flet.Padding(*[padding for i in range(4)]),
                    content=self.ui
                    )
                )
        self.page.add(self.bg)

        # Left
        # Status
        self.all_pc_status=AllPCStatus()
        self.left.controls.append(flet.Container(expand=1,content=self.all_pc_status))
        # BG Dropdown
        self.choose_bg=ChooseBG()
        self.choose_bg.on_change=self.change_bg
        self.left.controls.append(self.choose_bg)
        self.left.alignment=flet.MainAxisAlignment.CENTER

        self.ui.controls.append(self.left)

        # Right
        self.story_and_meta=flet.Row(spacing=20,expand=1)
        # Story
        self.story=Story()
        self.story_and_meta.controls.append(flet.Container(content=self.story,bgcolor=flet.colors.with_opacity(0.3,flet.colors.WHITE),border_radius=10,padding=flet.Padding(20,20,20,20),expand=2))
        # MetaGame
        self.meta_game=Story(meta=True)
        self.story_and_meta.controls.append(flet.Container(content=self.meta_game,bgcolor=flet.colors.with_opacity(0.3,flet.colors.WHITE),border_radius=10,padding=flet.Padding(20,20,20,20),expand=1))
        # Speaking
        self.main_speaking=Speaking()

        self.right.controls.append(self.story_and_meta)
        self.right.controls.append(flet.Container(
            content=self.main_speaking,
            bgcolor=flet.colors.with_opacity(0.3,flet.colors.WHITE),
            border_radius=10,
            padding=flet.Padding(20,20,20,20),
            expand=1
        ))
        # self.right.controls.append(self.meta_game)
        self.ui.controls.append(self.right)

        self.page.update()
        # time.sleep(1)
        # self.speaking(config.data["KP_id"],config.data["Opening"])
        # self.speaking(config.PL_list[1],"这是测试语句")
        # self.speaking(config.PL_list[2],"这是测试语句")
        # self.speaking(config.PL_list[3],"这是测试语句")
        # self.bot_message("[焦糖色]的人物卡已更新:\n[SAN]: 64+2*(2d4)=64+2*{3+4}(7)=78")
        # self.bot_message("[夏目辉]的人物卡已更新:\n[SAN]: 0+67=67")
        # self.bot_message("[真弓鈴絵]的人物卡已更新:\n[SAN]: 69+1=70")
        # self.kp_message(".npc1.这是npc的话")
        # self.kp_message("。sset 龙洋和真 疯狂")
        # self.bot_message("[焦糖色]进行理智检定[53]:\n1D100=74 呜呜，失败了。\n理智减少1d3=3点,当前剩余[50]点")



    def my_strip(self,message):
        message=message.strip('(').strip(')').strip('（').strip('）')
        message=re.sub("\[.*?\]", "", message)
        message=message.strip()
        return message


    def pc_message(self, user_id, message:str):
        # print("pc test")
        if message.startswith("(") or message.startswith("（"):
            # meta message
            self.meta_game.append(user_id,self.my_strip(message))
            pass
        elif message.startswith(".") or message.startswith("。"):
            return  
        else:
            self.speaking(user_id,self.my_strip(message))
            pass
        pass

    def kp_message(self, message:str):
        # print("kp test")
        if message.startswith("(") or message.startswith("（"):
            # meta message
            # print(message)
            self.meta_game.append(config.data["KP_id"],self.my_strip(message))
            pass
        elif re.search(self.set_pc_status,message) is not None:
            pc_name,status=re.search(self.set_pc_status,message).group(1),re.search(self.set_pc_status,message).group(2)
            if pc_name not in config.PL_name_list:
                return
            # print(status)
            pc_id=config.get_pc_id_from_name(pc_name)
            self.all_pc_status.update_status(pc_id,'status',status)
        else:
            kp_npc=re.search(self.kp_npc,message)
            if kp_npc is not None:
                # message.lstrip('.')
                npc_name,message=kp_npc.group(1),kp_npc.group(2)
                self.speaking(npc_name,message)
                # if npc_name in config.NPC_list:
                #     self.speaking(npc_name,message)
                # elif npc_name.startswith('f'):
                #     self.speaking('default_female',message)
                # else:
                #     self.speaking('default_male',message)
            elif message.startswith(".") or message.startswith("。"):
                return
            else:
                self.speaking(config.data["KP_id"],self.my_strip(message))
            pass
        pass

    def get_success(self,message):
        for success_level in ['大成功','大失败','失败','极难成功','困难成功','成功']:
            if success_level in message:
                return success_level

        return ''

    def bot_message(self, message):
        # print("bot test")
        message=message.strip()
        self.story.append("dice_bot",config.data["Bot_name"]+"(Dice Bot):\n"+message)
        success_level=self.get_success(message)
        # rd
        if re.search(self.dice_rd,message) is not None:
            res=re.search(self.dice_rd,message)
            self.rd(res.group(1),res.group(3),res.group(4),success_level)
        # ra
        elif re.search(self.dice_ra,message) is not None:
            res=re.search(self.dice_ra,message)
            self.ra(*[res.group(i) for i in range(1,5)],success_level)
        # rbp
        elif re.search(self.dice_rbp,message) is not None:
            res=re.search(self.dice_rbp,message)
            self.rbp(res.group(1),*[res.group(i) for i in range(3,8)],success_level)
        # rbpa
        elif re.search(self.dice_rbpa,message) is not None:
            res=re.search(self.dice_rbpa,message)
            self.rbp(*[res.group(i) for i in range(1,8)],success_level)
        # rh
        elif re.search(self.dice_rh,message) is not None:
            res=re.search(self.dice_rh,message)
            self.rh(res.group(1))
        # sc
        elif re.search(self.sc,message) is not None:
            res=re.search(self.sc,message)
            self.sancheck(*[res.group(i) for i in range(1,6)],success_level)
        # st
        elif re.search(self.st,message) is not None:
            res=re.search(self.st,message)
            self.update_status(*[res.group(i) for i in range(1,4)])
        
        
        pass

    def ob_message(self, ob_id, message):
        # print("ob test")
        self.meta_game.append(ob_id,self.my_strip(message))
        pass

    def change_bg(self,e):
        self.bg.image_src=self.choose_bg.get_value()
        self.bg.update()

    def speaking(self,user_id,message):
        self.sound_player.play_sound(user_id,message,self.main_speaking.update_)
        self.story.append(user_id,message)
        pass

    def close(self):
        self.page.window_close()
        pass


        # # 1名字 3原因 4结果表达式
        # self.dice_rd=re.compile('^\[(.*?)\](由于\[(.*?)\])*掷骰: (\d+D\d+=\d*?)$')
        
        # # 1名字 2技能名 3技能成功率 4结果表达式
        # self.dice_ra=re.compile('^\[(.*?)\]进行技能\[(.*?):(\d*?)\]检定: (\d+D\d+=\d*?)\D*?$')
        
        # # 1名字 3原因 4bp 5第一次表达式 6第二次十位 7结果
        # self.dice_rbp=re.compile('^\[(.*?)\](由于\[(.*?)\])*掷骰: (b|p|B|P)\D*?(\d+?D\d+?=\d+?) \D*?\[(\d+?)\].*?=(\d+?)\D*?$')

        # # 1名字 2技能名 3技能成功率 4BP 5第一次表达式 6第二次十位 7结果
        # self.dice_rbpa=re.compile('^\[(.*?)\]进行技能\[(.*?):(\d*?)\]检定: (b|p|B|P)\D*?(\d+?D\d+?=\d+?) \D*?\[(\d+?)\].*?=(\d+?)\D*?$')

        # # 1名字 2类型 3结果表达式
        # self.st=re.compile('^\[(.*?)\]的人物卡已更新:\s*?\[(.*?)\]: (.*?)$')

        # # 1名字
        # self.dice_rh=re.compile('^\[(.*?)\]掷暗骰$')

        # self.dice_res=re.compile('(.*?)=(\d*?)')

    def rd(self,name,reason,res,success_level):
        Dres=re.search(self.dice_res,res)
        if reason is not None:
            self.dice.roll_dice("【{}】由于【{}】掷骰：{}=???".format(name,reason,Dres.group(1)),"【{}】由于【{}】掷骰：{}   {}".format(name,reason,res,success_level))
        else:
            self.dice.roll_dice("【{}】掷骰：{}=???".format(name,Dres.group(1)),"【{}】掷骰：{}   {}".format(name,res,success_level))
        pass

    def rbp(self,name,reason,bp,res1,res2,res,success_level):
        Dres1=re.search(self.dice_res,res1)
        if bp.lower()=='b':
            bp='奖励骰'
        elif bp.lower()=='p':
            bp='惩罚骰'
        if reason is not None:
            self.dice.roll_dice("【{}】由于【{}】掷骰：{}=???\n{}：1D10={}，结果=???".format(name,reason,Dres1.group(1),bp,'?'*len(res2)),
                "【{}】由于【{}】掷骰：{}\n{}：1D10={}，结果={}   {}".format(name,reason,res1,bp,res2,res,success_level))
        else:
            self.dice.roll_dice("【{}】掷骰：{}=???\n{}：1D10={}，结果=???".format(name,Dres1.group(1),bp,'?'*len(res2)),
                "【{}】掷骰：{}\n{}：1D10={}，结果={}   {}".format(name,res1,bp,res2,res,success_level))
        pass

    def ra(self, name, skill_name, skill_p, res,success_level):
        Dres=re.search(self.dice_res,res)
        self.dice.roll_dice("【{}】进行技能鉴定：{}（{}）\n{}=???".format(name,skill_name,skill_p,Dres.group(1)),
            "【{}】进行技能鉴定：{}（{}）\n{}   {}".format(name,skill_name,skill_p,res,success_level))
        
        pass

    def rbpa(self,name,skill_name,skill_p,bp,res1,res2,res,success_level):
        Dres1=re.search(self.dice_res,res1)
        if bp.lower()=='b':
            bp='奖励骰'
        elif bp.lower()=='p':
            bp='惩罚骰'
        self.dice.roll_dice("【{}】进行技能鉴定：{}（{}）\n{}=???\n{}：1D10={}，结果=???".format(name,skill_name,skill_p,Dres1.group(1),bp,'?'*len(res2)),
            "【{}】进行技能鉴定：{}（{}）\n{}\n{}：1D10={}，结果={}   {}".format(name,skill_name,skill_p,res1,bp,res2,res, success_level)) 
        pass
    
    def rh(self,name):
        self.dice.roll_dice("【{}】掷暗骰...".format(name),"【{}】掷暗骰...".format(name))
        pass

    def update_status(self,name,type,res):
        pl_id=config.get_pc_id_from_name(name)
        # 1原始值 2表达式 3杂项 4表达式随机部分结果 5表达式随机部分和 6结果
        dice_update=re.compile('(\d+)(.*?)=(.*?){(.*?)}\((.*?)\)=(\d+)')
        if re.search(dice_update,res) is not None:
            diceres=re.search(dice_update,res)
            self.dice.roll_dice("【{} 】的【{}】更新：\n{}{}=???".format(name,type,diceres.group(1),diceres.group(2)),
                "【{} 】的【{}】更新：\n".format(name,type)+res)
            self.all_pc_status.update_status(pl_id,type,diceres.group(6))
            # config.update_pc_status(pl_id,type,diceres.group(6))
        elif re.search('.*?=(\d+?)$',res):
            value=re.search('.*?=(\d+?)$',res).group(1)
            self.all_pc_status.update_status(pl_id,type,value)
            pass
    
    def sancheck(self,name,ori_san,sc_res,sc_reduce_res,res,success_level):
        Dres=re.search(self.dice_res,sc_res)
        Dres_=re.search(self.dice_res,sc_reduce_res)
        if 'd' in sc_reduce_res or 'D' in sc_reduce_res:
            self.dice.roll_dice("【{}】进行理智检定（{}）:\n{}=???".format(name,ori_san,Dres.group(1)),
                "【{}】进行理智检定（{}）:\n{}   {}".format(name,ori_san,sc_res,success_level))
            self.dice.roll_dice("【{}】理智减少:\n{}=???\n当前剩余：???".format(name,Dres_.group(1)),
                "【{}】理智减少:\n{}\n当前剩余：{}".format(name,sc_reduce_res,res))
        else:
            self.dice.roll_dice("【{}】进行理智检定（{}）:\n{}=???\n理智减少：???\n当前剩余：???".format(name,ori_san,Dres.group(1)),
                "【{}】进行理智检定（{}）:\n{}   {}\n理智减少：{}\n当前剩余：{}".format(name,ori_san,sc_res,success_level,Dres_.group(2),res))
        pl_id=config.get_pc_id_from_name(name)
        self.all_pc_status.update_status(pl_id,'san',res)
            


        # config.update_pc_status(pl_id,type,value)

        pass


    # def npc_speaking(self,name,message):
        


    # def get_bg_files(self):
    #     pathdir = config.data["Path"]+"bg/"
    #     imgFileList = os.listdir(pathdir)   #图片列表
    #     res=[]
        
    #     for filename in imgFileList:
    #         filepath = os.path.join(pathdir, filename)  #图片的绝对路径
    #         if os.path.isfile(filepath) and (filename.lower().endswith('.jpg') or filename.lower().endswith('.png')):
    #             res.append(filename)
        
    #     return res


class MyDice(flet.AlertDialog):
    def __init__(self):
        super().__init__()        
        self.queue=Queue(1)
        self.current_thread=None
        self.open=False
        self.title=flet.Text(value='检定',theme_style=flet.TextThemeStyle.HEADLINE_LARGE)
        self.content=flet.Text(value='',width=600,height=400,theme_style=flet.TextThemeStyle.HEADLINE_MEDIUM)
       

    def __roll_dice(self,before_text,after_text):
        self.content.value=before_text
        self.open=True
        self.update()
        playsound(config.data['Path']+'dice.mp3')
        time.sleep(0.3)
        self.content.value=after_text
        self.update()
        time.sleep(1.2)
        self.open=False
        self.update()
        if not self.queue.empty():
            self.current_thread=self.queue.get()
            self.current_thread.start()
        # self.play_dice_sound()

    def roll_dice(self,before_text,after_text):
        self.queue.put(threading.Thread(target=self.__roll_dice, args=(before_text,after_text)))
        if self.current_thread is None or (not self.current_thread.is_alive()):
            self.current_thread=self.queue.get()
            self.current_thread.start()
        

    # def play_dice_sound(self):
    #     pass
    




class AllPCStatus(flet.Column):
    def __init__(self):
        super().__init__()
        self.pc_status_dict={}
        # self.pc_status=ft.Column(controls=[])
        for pc in config.PL_list:
            self.pc_status_dict[pc]=PCStatus(pc)
        for values in self.pc_status_dict.values():
            self.controls.append(values)
        # self.ui.controls.append(PCStatus(self.PCs_info.pc_list[0]))
        self.expand=1
        self.spacing=20
    
    def update_status(self,pl_id,type,value):
        if pl_id not in config.PL_list:
            return
        # pl_index=config.PL_list.index(pl_id)
        eval('self.pc_status_dict[pl_id].set_{}(value)'.format(type.lower()))
        self.update()
    
class Story(flet.ListView):
    def __init__(self, maxlen=100, meta=False):
        super().__init__(spacing=10, auto_scroll=True,expand=1)
        self.maxlen=maxlen
        # if width:
        #     self.width=width
        self.meta=meta
        # self.controls.append(OneMessage("706386750","毕宿星的歌无人听晓，国王的褴衣随风飘摇，歌声默默地消逝在那，昏暗的卡尔克萨。我的灵魂已无法歌唱，我的歌像泪不再流淌，只有干涸和沉默在那，失落的卡尔克萨。降临吧！我们衣衫褴褛的王。",self.meta))
        # self.controls.append(OneMessage("496373158","毕宿星的歌无人听晓，国王的褴衣随风飘摇，歌声默默地消逝在那，昏暗的卡尔克萨。我的灵魂已无法歌唱，我的歌像泪不再流淌，只有干涸和沉默在那，失落的卡尔克萨。降临吧！我们衣衫褴褛的王。",self.meta))
        # self.controls.append(flet.Text(value="1231231231"))

    def append(self, user_id:str, message):
        # if user_id.startswith('?female?') or user_id.startswith('?male?'):
        #     user_id.lstrip('?female?').lstrip('?male?')
        self.controls.append(OneMessage(user_id,message,self.meta))
        if len(self.controls)>50:
            self.controls=self.controls[-50:]
        self.update()

class Speaking(flet.Row):
    def __init__(self):
        super().__init__(height=300)
        self.id=config.data["KP_id"]
        # self.message=message
        # print(self.get_fig(self.id))
        self.fig=ft.Container(
                # image_src=config.data[self.id]['fig'],
                image_fit=ft.ImageFit.CONTAIN,
                width=self.height-20,
                height=self.height-20,
                border_radius=ft.border_radius.all(5),
                )
        self.message=""
        self.text=ft.Text(value=self.message, theme_style=flet.TextThemeStyle.HEADLINE_MEDIUM,expand=1)
        self.name=ft.Text(value="", theme_style=flet.TextThemeStyle.HEADLINE_LARGE,height=100,color=flet.colors.WHITE)
        self.controls=[self.fig,flet.Column(controls=[self.name,self.text],expand=1)]
    
    # def get_fig(self):
    #     if os.path.exists(config.data["Path"]+"{}/fig.png".format(user_id)):
    #         return config.data["Path"]+"{}/fig.png".format(user_id)
    #     elif os.path.exists(config.data["Path"]+"{}/fig.jpg".format(user_id)):
    #         return config.data["Path"]+"{}/fig.jpg".format(user_id)
    #     elif os.path.exists(config.data["Path"]+"fig.png"):
    #         return config.data["Path"]+"fig.png"
    #     else:
    #         return config.data["Path"]+"fig.jpg"
    # 

    def update_(self,id:str,message):
        self.id=id
        self.message=message
        self.text.value=self.message

        if self.id==config.data["KP_id"]:
            self.name.value="KP"
            self.fig.image_src=config.data[self.id]['fig']
        elif self.id in config.PL_list:
            self.name.value=config.data[self.id]['name']
            self.fig.image_src=config.data[self.id]['fig']
        elif self.id in config.NPC_list:
            self.name.value=id
            self.fig.image_src=config.data[self.id]['fig']
        else:
            # print(id)
            # self.name.value=id
            if id.startswith('?'):
                self.name.value=id.lstrip('?')
                self.fig.image_src=config.data['default_female']['fig']
            else:
                self.name.value=id
                self.fig.image_src=config.data['default_male']['fig']
                # print(self.fig.image_src)


        # self.fig.image_src=config.data[self.id]['fig']

        self.update()
