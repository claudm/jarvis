import sys

import gapi
import commands

import speech_recognition as sr
import os



import subprocess

speech = gapi.Speech('en-uk')

if len(sys.argv)==2:
	if sys.argv[1] in list(gapi.languages.keys()):
		speech.lang = gapi.languages[sys.argv[1]]
	elif sys.argv[1] in list(gapi.languages.values()):
		speech.lang = sys.argv[1]

def recordAudio(language):
	r = sr.Recognizer()
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		print("Say something!")
		audio = r.listen(source)
		try:
		#	print("Speech was:" + r.recognize_google(audio))    # recognize speech using Google Speech Recognition
			print("Done listening!")
			return r.recognize_google(audio,language = language)    # recognize speech using Google Speech Recognition


		except LookupError:                            # speech is unintelligible
		    print("Could not understand audio")





def main():
	global speech
	translator = gapi.Translator(speech.lang, 'en-uk')
	try:
		# cfileName = psw.convert(fileName)
		phrase = recordAudio(speech.lang)
		# os.remove(fileName)
		# os.remove(cfileName)
		if phrase!=None:
			phrase = phrase.lower()
		# phrase = "abrir chrome"
		if len(phrase.strip())>0:
			print('text:',phrase)
			#psw.play(speech.getAudio(phrase))
			cmd = translator.translate(phrase)
			print('cmd:',cmd)	
			# import ipdb; ipdb.set_trace()
			commands.execute(cmd, speech)
	except Exception as e:
		print("Unexpected error:", sys.exc_info()[0], e)
	return True

while True:
	main()
