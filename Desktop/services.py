import socket 
import sys 
import os 
import pyautogui
import time

sensi_media = 5
def volume_up():
	for i in range (sensi_media):
		pyautogui.press('volumeup')
def volume_down():
	for i in range (sensi_media):
		pyautogui.press('volumedown')
def mute_media():
	pyautogui.press('volumemute')
def next_music():
	pyautogui.press('nexttrack')
def prev_music():
	pyautogui.press('prevtrack')
def play_music():
	pyautogui.press('playpause')

def search(string):
	pyautogui.press('win')
	pyautogui.write(string)
	pyautogui.press('enter')

def conTv():
	os.system('DisplaySwitch.exe /external')

def desconTv():
	os.system('DisplaySwitch.exe /extend')
		
def printFile(string):
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
	search(temp)
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
