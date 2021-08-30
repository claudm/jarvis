# -*- coding: utf-8 -*-
#gapi.py: google api
#by ROCHA, Rodrigo Caetano

import re
import json
import string

import urllib.request, urllib.error, urllib.parse
try:
	import urllib2 as request
	from urllib.parse import quote
	from urllib.request import urlopen
except:
	from urllib import request
	from urllib.parse import quote
	from urllib.request import urlopen

def _randstr(size=6, chars=string.ascii_uppercase + string.digits):
	import random
	return ''.join(random.choice(chars) for _ in range(size))

languages = {'afrikaans':'af', 'albanian':'sq', 'amharic':'am', 'arabic':'ar', 'armenian':'hy', 'azerbaijani':'az', 'basque':'eu', 'belarusian':'be', 'bengali':'bn', 'bihari':'bh', 'bulgarian':'bg', 'burmese':'my', 'catalan':'ca', 'cherokee':'chr', 'chinese':'zh', 'chinese_simplified':'zh-cn', 'chinese_traditional':'zh-tw', 'croatian':'hr', 'czech':'cs', 'danish':'da', 'dhivehi':'dv', 'dutch':'nl', 'english':'en-uk', 'esperanto':'eo', 'estonian':'et', 'filipino':'tl', 'finnish':'fi', 'french':'fr', 'galician':'gl', 'georgian':'ka', 'german':'de', 'greek':'el', 'guarani':'gn', 'gujarati':'gu', 'hebrew':'iw', 'hindi':'hi', 'hungarian':'hu', 'icelandic':'is', 'indonesian':'id', 'inuktitut':'iu', 'irish':'ga', 'italian':'it', 'japanese':'ja', 'kannada':'kn', 'kazakh':'kk', 'khmer':'km', 'korean':'ko', 'kurdish':'ku', 'kyrgyz':'ky', 'laothian':'lo', 'latvian':'lv', 'lithuanian':'lt', 'macedonian':'mk', 'malay':'ms', 'malayalam':'ml', 'maltese':'mt', 'marathi':'mr', 'mongolian':'mn', 'nepali':'ne', 'norwegian':'no', 'oriya':'or', 'pashto':'ps', 'persian':'fa', 'polish':'pl', 'portuguese':'pt-br', 'punjabi':'pa', 'romanian':'ro', 'russian':'ru', 'sanskrit':'sa', 'serbian':'sr', 'sindhi':'sd', 'sinhalese':'si', 'slovak':'sk', 'slovenian':'sl', 'spanish':'es', 'swahili':'sw', 'swedish':'sv', 'tajik':'tg', 'tamil':'ta', 'tagalog':'tl', 'telugu':'te', 'thai':'th', 'tibetan':'bo', 'turkish':'tr', 'ukranian':'uk', 'urdu':'ur', 'uzbek':'uz', 'uighur':'ug', 'vietnamese':'vi', 'welsh':'cy', 'yiddish':'yi'}

class Speech:
	def __init__(self, lang):
		self.lang = lang

	def getText(self, fileName, show_all = False):
		key = "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"

		file_upload = fileName
		if not file_upload.endswith('.flac'):
			file_upload = "%s.flac" % file_upload
		audio = open(file_upload, "rb").read()

		url = "http://www.google.com/speech-api/v2/recognize?client=chromium&lang=%s&key=%s" % (self.lang, key)
		header = {"Content-Type": "audio/x-flac; rate=8000"}

		req = request.Request(url, data = audio, headers = header)
		# check for invalid key response from the server
		try:
			response = request.urlopen(req)
		except:
			raise KeyError("Server wouldn't respond (invalid key or quota has been maxed out)")
		response_text = response.read().decode("utf-8")

		# ignore any blank blocks
		actual_result = []
		for line in response_text.split("\n"):
			if not line: continue
			result = json.loads(line)["result"]
			if len(result) != 0:
				actual_result = result[0]

		# make sure we have a list of transcriptions
		if "alternative" not in actual_result:
			raise LookupError("Speech is unintelligible")

		# return the best guess unless told to do otherwise
		if not show_all:
			for prediction in actual_result["alternative"]:
				if "confidence" in prediction:
					return prediction["transcript"]
			raise LookupError("Speech is unintelligible")

		spoken_text = []

		# check to see if Google thinks it's 100% correct
		default_confidence = 0
		if len(actual_result["alternative"])==1: default_confidence = 1

		# return all the possibilities
		for prediction in actual_result["alternative"]:
			if "confidence" in prediction:
				spoken_text.append({"text":prediction["transcript"],"confidence":prediction["confidence"]})
			else:
				spoken_text.append({"text":prediction["transcript"],"confidence":default_confidence})
		return spoken_text

#	def getText(self, fileName):
#		url = "http://www.google.com/speech-api/v1/recognize?lang=%s" % self.lang
#		file_upload = fileName
#		if not file_upload.endswith('.flac'):
#			file_upload = "%s.flac" % file_upload
#		audio = open(file_upload, "rb").read()
#		header = {"Content-Type": "audio/x-flac; rate=8000"}
#		data = request.Request(url, audio, header)
#		post = urlopen(data)
#		response = post.read()
#		response = response.strip()
#		response = response.strip('\n')
#		if len(response)>0:
#			#print '*'+response+'*'
#			if '\n' in response:
#				bestPhrase = None
#				conf = 0
#				for strresp in response.split('\n'):
#					resp = json.loads(strresp)
#					if str(resp['status'])!='5' or len(resp['hypotheses']):
#						for hypothesis in resp['hypotheses']:
#							if float(hypothesis['confidence'])>conf:
#								bestPhrase = hypothesis['utterance']
#								conf = float(hypothesis['confidence'])
#				return bestPhrase
#			else:
#				resp = json.loads(response)
#				if str(resp['status'])!='5' or len(resp['hypotheses']):
#					conf = 0
#					phrase = None
#					for hypothesis in resp['hypotheses']:
#						if float(hypothesis['confidence'])>conf:
#							phrase = hypothesis['utterance']
#							conf = float(hypothesis['confidence'])
#					return phrase
#				else:
#					return None
#		else:
#			return None

	def getAudio(self, text):
		text = self._convertTextAsLinesOfText(text)
		fileName = '.'+_randstr(size=10)+'.mp3'
		self._downloadAudioFile(text, self.lang, open(fileName, 'w'))
		return fileName

	def _convertTextAsLinesOfText(self, text):
		""" This converts string or file to a usable chunk or several
		chunks - each smaller than 100 characters.
		"""
		# Sanitizes the text.
		text = text.replace('\n', ' ')
		text_list = re.split('(\,|\.|\;|\:)', text)

		# Splits a text into chunks
		text_lines = []
		for idx, val in enumerate(text_list):
			if idx % 2 == 0:
				text_lines.append(val)
			else:
				# Combines the string + the punctuation.
				joined_text = ''.join((text_lines.pop(), val))

				# Checks if the chunk still needs splitting.
				if len(joined_text) < 100:
					text_lines.append(joined_text)
				else:
					subparts = re.split('( )', joined_text)
					temp_string = ""
					temp_array = []
					for part in subparts:
						temp_string += part
						if len(temp_string) > 80:
							temp_array.append(temp_string)
							temp_string = ""
					#append final part
					temp_array.append(temp_string)
					text_lines.extend(temp_array)
		return text_lines

	def _downloadAudioFile(self, text_lines, language, audio_file):
		"""
		Downloads an MP3 from Google Translate.
		*.mp3 content is based on text and language codes parsed
		from command line or passed in via simplespeech().
		"""
		SAVE_SOUND = False
		for idx, line in enumerate(text_lines):
			query_params = {"tl": language, "q": line, "total": len(text_lines), "idx": idx}
			url = "http://translate.google.com/translate_tts?ie=UTF-8" + "&" + self._unicode_urlencode(query_params)
			headers = {"Host": "translate.google.com", "User-Agent": "Mozilla 5.20"}
			req = request.Request(url, '', headers)
			#sys.stdout.write('.')
			#sys.stdout.flush()
			if len(line) > 0:
				try:
					response = urlopen(req)
					SAVE_SOUND = True
				except request.HTTPError as e:
					print(('resp Error: {}'.format(e)))
			if SAVE_SOUND:
				try:
					audio_file.write(response.read())
				except:
					SAVE_SOUND = False
					print(('failed to save good response as: {}'.format(audio_file.name)))
		#if SAVE_SOUND:
		#    print('Saved MP3 to {}'.format(audio_file.name))
		#if idx > 0:
		#    print('it enunciates {} lines of text'.format(idx+1))
		audio_file.close()

	def _unicode_urlencode(self,params):
		"""
		Encodes params to be injected into a url.
		"""
		if isinstance(params, dict):
			params = list(params.items())
		from urllib.parse import urlencode
		return urlencode([(k, isinstance(v, str) and v.encode('utf-8') or v) for k, v in params])

class Translator:
	string_pattern = r"\"(([^\"\\]|\\.)*)\""
	match_string =re.compile(
		r"\,?\["
		+ string_pattern + r"\,"
		+ string_pattern + r"\,"
		+ string_pattern + r"\,"
		+ string_pattern
		+r"\]")

	def __init__(self, from_lang, to_lang,):
		self.from_lang = from_lang
		self.to_lang = to_lang

	def html_decode(self,s):
		"""
		Returns the ASCII decoded version of the given HTML string. This does
		NOT remove normal HTML tags like <p>.
		"""
		htmlCodes= (("'",""),("'",'"'),('>','>'),('<','<'),('&','&'))
		for code in htmlCodes:
		    s = s.replace(code[1], code[0])
		return s

	def translate(self,to_translate):

		agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
		before_trans = 'class="result-container">'
		link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (self.to_lang, self.from_lang, to_translate.replace(" ", "+"))
		request = urllib.request.Request(link, headers=agents)
		page = urllib.request.urlopen(request).read().decode('utf8')
		result = page[page.find(before_trans)+len(before_trans):]
		result = result.split("<")[0]
        
		#return self.html_decode(result)
		return result

	def _unescape(self, text):
		return json.loads('"%s"' % text)

if __name__ == "__main__":
	tr = Translator('en-uk', 'pt-br')
	print(tr.translate('hello world'))
	sp = Speech('en-uk')
#	filename = sp.getAudio('hello world')

	# import psw
	# psw.play(filename)
	# import os
	# os.remove(filename)

	print(sp.getText('browser.flac'))
