import socket 
import sys 
import os 
import pyautogui
import time
import unidecode
sensi_media = 5
def up_media():
	for i in range (sensi_media):
		pyautogui.press('volumeup')
def down_media():
	for i in range (sensi_media):
		pyautogui.press('volumedown')
def mute_media():
	pyautogui.press('volumemute')
def next_media():
	pyautogui.press('nexttrack')
def back_media():
	pyautogui.press('prevtrack')
	pyautogui.press('prevtrack')
def repeat_media():
	pyautogui.press('prevtrack')
def play_media():
	pyautogui.press('playpause')

def windowsSearch(string):
	pyautogui.press('win')
	pyautogui.write(unidecode.unidecode(string))
	pyautogui.press('enter')

def conTv():
	os.system('DisplaySwitch.exe /external')

def desconTv():
	os.system('DisplaySwitch.exe /extend')
		
def printFile(self,string):
	temp =string
	t = temp.split()
	try:
		n = int(t[0].replace('duas','2'))
		del (t[0])
		temp = ''
		for word in t:
			temp += " " + word
		
	except:
		n =1
	windowsSearch(temp)
	time.sleep(6)
	for i in range(n):
		pyautogui.press('enter')
		time.sleep(1)
		pyautogui.hotkey('ctrl', 'p')
		pyautogui.press('enter')
		time.sleep(3)
	pyautogui.hotkey('alt', 'f4')

def shutdownPC():
	os.system('shutdown -s')
