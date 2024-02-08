import flet as ft
import os
import time

try:
    from .ConfigTool import *
    # from .PCs_info import PCs_info
except:
    # from PCs_info import PCs_info
    from ConfigTool import *

style1=ft.TextThemeStyle.BODY_MEDIUM
style2=ft.TextThemeStyle.BODY_LARGE
style3=ft.TextThemeStyle.TITLE_LARGE
style4=ft.TextThemeStyle.HEADLINE_SMALL

# textcolor=ft.colors.WHITE

def if_Image(name:str):
    if name.endswith('.png') or name.endswith('.jpg'):
        return True
    return False

class PCStatus(ft.Container):
    def __init__(self, pc_id):
        super().__init__()
        self.height=120
        # self.width=400
        self.bgcolor=ft.colors.with_opacity(0.5, ft.colors.WHITE)
        self.border_radius=ft.border_radius.all(10)

        self.pc_id=pc_id
        self.config=config.get_pc_config(pc_id)
        # self.pc_info=PCs_info(config.PL_list).config[pc_id]
        # print(self.get_avatar())
        self.avatar=ft.Container(
                bgcolor=ft.colors.RED,
                image_src=self.config['avatar'],
                image_opacity=1.0,
                image_fit=ft.ImageFit.COVER,
                width=100,
                height=100,
                border_radius=ft.border_radius.all(5),
                )
                
        # self.if_crazy=False
        self.status='正常'
        self.info=ft.Row(controls=[
            ft.Text(value=config.get_pc_name(self.pc_id), theme_style=style4),
            ft.Text(value="【{}】".format(self.status), theme_style=style2, color=ft.colors.WHITE)
        ], spacing=3)
        self.hp=OneStatus(self.pc_id,'hp')
        self.san=OneStatus(self.pc_id,'san')
        self.mp=OneStatus(self.pc_id,'mp')
        self.content=ft.Row(controls=[ft.Container(width=0),self.avatar,ft.Column(controls=[
            self.info,
            ft.Row(controls=[self.hp,ft.Text(value="职业: "+self.config['job'], theme_style=style2, color=ft.colors.WHITE)],spacing=10),
            ft.Row(controls=[self.san,self.mp],spacing=10)
        ])],spacing=10)

    # def get_avatar(self):
    #     if os.path.exists(config.data["Path"]+"{}/avatar.png".format(self.pc_id)):
    #         return config.data["Path"]+"{}/avatar.png".format(self.pc_id)
    #     elif os.path.exists(config.data["Path"]+"{}/avatar.jpg".format(self.pc_id)):
    #         return config.data["Path"]+"{}/avatar.jpg".format(self.pc_id)
    #     elif os.path.exists(config.data["Path"]+"avatar.png"):
    #         return config.data["Path"]+"avatar.png"
    #     else:
    #         return config.data["Path"]+"avatar.jpg"

    def set_status(self,status:str):
        self.status=status
        self.info.controls[1].value="【{}】".format(status)
        self.info.controls[1].color= ft.colors.RED if self.status!='正常' else ft.colors.WHITE
        self.avatar.image_opacity=1.0 if self.status=='正常' else 0.6
        self.info.update()
        config.update_pc_status(self.pc_id,'status',status)
    
    def set_hp(self,hp):
        self.hp.set(hp)
        config.update_pc_status(self.pc_id,'hp',hp)
    def set_hpmax(self,hpmax):
        self.hp.setmax(hpmax)
        config.update_pc_status(self.pc_id,'hpmax',hpmax)
    def set_san(self,san):
        self.san.set(san)
        config.update_pc_status(self.pc_id,'san',san)
    def set_sanmax(self,sanmax):
        self.san.setmax(sanmax)
        config.update_pc_status(self.pc_id,'sanmax',sanmax)
    def set_mp(self,mp):
        self.mp.set(mp)
        config.update_pc_status(self.pc_id,'mp',mp)
    def set_mpmax(self,mpmax):
        self.mp.setmax(mpmax)
        config.update_pc_status(self.pc_id,'mpmax',mpmax)



class OneStatus(ft.Text):
    def __init__(self, pc_id, type='hp'):
        super().__init__()
        self.type=type
        self.pc_id=pc_id
        self.now=config.data[pc_id]['status'][type]
        self.max=config.data[pc_id]['status'][type+'max']
        self.theme_style=style3
        self.value="{}: {}/{}".format(self.type.upper(),self.now,self.max)

    def set(self,value):
        self.now=value
        self.__update()
    def setmax(self,value):
        self.max=value
        self.__update()
    def __update(self):
        self.value="{}: {}/{}".format(self.type,self.now,self.max)
        self.update()

class ChooseBG(ft.Dropdown):
    def __init__(self,width=380):
        super().__init__(expand=0,width=width)
        self.path=config.data["Path"]+"bg/"
        self.get_all_bg(0)
        self.hint_text="Choose background."
        self.on_focus=self.get_all_bg
        # self.bgcolor=ft.colors.GREY
        self.filled=True
        self.border=0
        # self.width=240

    def get_all_bg(self,e):
        self.options=[ft.dropdown.Option(bg) for bg in os.listdir(self.path) if if_Image(bg)]
    
    def get_value(self):
        return self.path+self.value



class OneMessage(ft.Container):
    def __init__(self, pc_id:str, message, small=False):
        super().__init__()
        # self.height=80
        # self.expand=1
        # self.bgcolor=ft.colors.with_opacity(0.5, ft.colors.WHITE)
        # self.border_radius=ft.border_radius.all(10)
        ifname=False
        self.pc_id=pc_id
        if self.pc_id.isdigit() or self.pc_id in config.NPC_list or self.pc_id=='dice_bot':
            # print(message)
            image_src=config.data[self.pc_id]['avatar'] if self.pc_id in config.data else self.get_ob_avatar()
        else:
            self.pc_id=self.pc_id.lstrip('?')
            # image_src=config.data[config.data['KP_id']]['avatar']
            image_src=config.data['Path']+'npc/default_avatar.png' if os.path.exists(config.data['Path']+'npc/default_avatar.png') else config.data['Path']+'npc/default_avatar.jpg'
            ifname=True
            pass
        # self.config=config.get_pc_config(pc_id)
        # self.pc_info=PCs_info(config.PL_list).config[pc_id]
        # print(self.get_avatar())
        avatar_size=30 if small else 50
        text_style=style2 if small else style3
        space_width=80 if small else 120
        text_width=300 if small else 500
        self.avatar=ft.Container(
                image_src=image_src,
                image_fit=ft.ImageFit.COVER,
                width=avatar_size,
                height=avatar_size,
                border_radius=ft.border_radius.all(3),
                )
        # self.bubble=ft.Container(
        #         bgcolor=ft.colors.with_opacity(0.85, ft.colors.WHITE)
        # )           
        self.text=ft.Text(value=(self.pc_id+':\n' if ifname else '')+message,theme_style=text_style,expand=1,text_align=ft.TextAlign.LEFT)   
        self.space= ft.Container(width=space_width)
        
        self.content=ft.Row(
            controls=[self.avatar,
                ft.Container(content=self.text,alignment=ft.alignment.top_left,width=text_width),
                self.space] if self.pc_id!=config.data['KP_id'] else 
                [self.space,ft.Container(content=self.text,
                alignment=ft.alignment.top_right,width=text_width),
                self.avatar],
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=1,
            alignment=ft.MainAxisAlignment.END if self.pc_id==config.data['KP_id'] else ft.MainAxisAlignment.START
            )

        # self.content=ft.Row(controls=[self.avatar,self.text] if pc_id!=config.data['KP_id'] else [self.text,self.avatar])

    def get_avatar(self):
        if os.path.exists(config.data["Path"]+"{}/avatar.png".format(self.pc_id)):
            return config.data["Path"]+"{}/avatar.png".format(self.pc_id)
        elif os.path.exists(config.data["Path"]+"{}/avatar.jpg".format(self.pc_id)):
            return config.data["Path"]+"{}/avatar.jpg".format(self.pc_id)
        elif os.path.exists(config.data["Path"]+"avatar.png"):
            return config.data["Path"]+"avatar.png"
        else:
            return config.data["Path"]+"avatar.jpg"

    def get_ob_avatar(self):
        if not os.path.exists(config.data['Path']+'ob/{}/avatar.jpg'.format(self.pc_id)):
            download_avatar(self.pc_id,config.data['Path']+'ob/{}/avatar.jpg'.format(self.pc_id))
        while not os.path.exists(config.data['Path']+'ob/{}/avatar.jpg'.format(self.pc_id)):
            time.sleep(0.2)
        
        return config.data['Path']+'ob/{}/avatar.jpg'.format(self.pc_id)
        