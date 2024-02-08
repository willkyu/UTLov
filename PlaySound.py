from playsound import playsound
# from pydub.playback import play
# from pydub import AudioSegment
from aip import AipSpeech
import threading
import os
from queue import Queue
from openai import OpenAI
 
try:
	from .ConfigTool import *
except:
	from ConfigTool import *
 
tts = '毕宿星的歌无人听晓，国王的褴衣随风飘摇，歌声默默地消逝在那，昏暗的卡尔克萨。我的灵魂已无法歌唱，我的歌像泪不再流淌，只有干涸和沉默在那，失落的卡尔克萨。降临吧！我们衣衫褴褛的王。'
# print(len(tts))


speech_file_path = "./voice.mp3"



 

class SoundPlayer():
	def __init__(self, type='Baidu') -> None:
		self.type=type
		if self.type=='Baidu':
			api_info=config.data["BaiduAPI"]
			APP_ID = api_info["APP_ID"]
			API_KEY = api_info["API_KEY"]
			SECRET_KEY = api_info["SECRET_KEY"]
			self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
		elif self.type=='Openai':
			api_info=config.data["OpenaiAPI"]
			print(api_info["SECRET_KEY"])
			SECRET_KEY = api_info["SECRET_KEY"]
			self.client = OpenAI(api_key=config.data['OpenaiAPI'])
		self.current_thread=None
		self.queue=Queue(0)
		pass

	def __get_sound(self,message, voice_info):
		if self.type=='Baidu':
			voiceresult  = self.client.synthesis(text=message, lang='zh', ctp=1, options=voice_info)
			with open(speech_file_path, "wb") as f:
				f.write(voiceresult)
		elif self.type=='Openai':
			voiceresult = self.client.audio.speech.create(
					model=voice_info["model"],
					voice=voice_info["voice"],
					input=message
					)
			voiceresult.stream_to_file(speech_file_path)


	def __play_sound(self, id:str, message, update_fun):
		update_fun(id, message)
		voice_info=config.get_pc_config(id)
		if id in config.PL_list:
			voice_info=config.get_pc_config(id)['audio']
		elif id==config.data['KP_id']:
			voice_info=config.data['KP_audio']
		elif id in config.NPC_list:
			voice_info=config.data[id]['audio']
		elif id.startswith('?'):
			voice_info=config.data['default_female']['audio']
		else:
			voice_info=config.data['default_male']['audio']
		self.__get_sound(message[:100  ], voice_info)
		try:
			print('speaking...')
			playsound(speech_file_path)
			os.remove(speech_file_path)
			# play(AudioSegment.from_mp3('./voice.mp3'))
		except:
			print("Play sound error.")
		
		# with open("./voice.mp3", "wb") as f:
		# 	f.write(voiceresult)
		# print('speaking...')
		# playsound('./voice.mp3')
		# os.remove('./voice.mp3')
		if not self.queue.empty():
			self.current_thread=self.queue.get()
			
			self.current_thread.start()
	
	def play_sound(self, id, message, update_fun):
		# message=message[:100]
		self.queue.put(threading.Thread(target=self.__play_sound, args=(id, message, update_fun)))
		if self.current_thread is None or (not self.current_thread.is_alive()):
			self.current_thread=self.queue.get()
			self.current_thread.start()

if __name__ =="__main__":

	soundtest=SoundPlayer()
	soundtest.play_sound("test_id",tts,  1)
	# soundtest.play_sound(tts, config.data["PCs"][1]["audio"])
	# print('end?')
	# for i in range(4):
	# 	soundtest.play_sound(tts, config.data["PCs"][0]["audio"])
	# print('end..')
