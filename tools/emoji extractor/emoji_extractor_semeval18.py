# -*- coding: utf-8 -*-

'''
---- Emoji extractor-----
Given a file with one tweet per line, return two files: 1)list of texts without emois and 2) list of correct labels for semeval emoji detection 2018

a. first param =  Path to file with tweets (one per line). It can contain the text of the tweets (one per line), or the twitter json(one per line). 
                  If it is the twitter json, add the extention .json at the end.
b. second param = "us" or "es" to decide what label mapping to use

Usage example for a file containng the json of american tweets (one per line): 
$ python emoji_extractor_semeval18.py tweets_us.json us
'''

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import json
import re
import emojilib #from https://github.com/fvancesco/emoji

def clean_text(text):
	#remove emojis, remove links, anonymize user mentions
	clean = ""
	text = emojilib.replace_emoji(text, replacement=' ')
	text = re.sub( '\s+', ' ', text).strip()
	for t in text.split(" "):
		if t.startswith('@') and len(t) > 1: 
			clean += "@user "
		elif t.startswith('http'): 
			pass
		else:
			clean += t + " "
	#remove double spaces
	return clean

def main():
	out_text = open(tweets_file+".text",'w')
	out_labels = open(tweets_file+".labels",'w')
	out_ids = open(tweets_file+".ids",'w')
	tot=0
	ok=0
	with open(tweets_file) as f_in:
		for line in f_in:
			j = json.loads(line)
			tweet_id = j['id']
			text = j['text'].replace("\n","")
			emo_list = emojilib.emoji_list(text)
			emo_set = set([d['code'] for d in emo_list if 'code' in d])
			if len(emo_set) == 1:
				emo = emo_set.pop().encode('utf_8')
				if emo in mapping:
					ct= clean_text(text)
					out_text.write(ct+"\n")
					out_labels.write(mapping[emo]+"\n")
					out_ids.write(str(tweet_id)+"\n")
					ok+=1
			if tot % 10000 == 0:
				print(str(tot))
			tot+=1

	print(str(ok) + " good examples out of " + str(tot))

	out_text.close()
	out_labels.close()
	out_ids.close()


if __name__ == '__main__':

	args = sys.argv[1:]
	if len(args) == 2:
		tweets_file = args[0]
		lang = args[1]

		if 'us' in lang:
			mapping = { '❤':'0' , '😍':'1' , '😂':'2' , '💕':'3' , '🔥':'4' , '😊':'5' , '😎':'6' , '✨':'7' , '💙':'8' , '😘':'9' , '📷':'10' , '🇺🇸':'11' , '☀':'12' , '💜':'13' , '😉':'14' , '💯':'15' , '😁':'16' , '🎄':'17' , '📸':'18' , '😜':'19'}
		elif 'es' in lang:
			mapping = { '❤':'0' , '😍':'1' , '😂':'2' , '💕':'3' , '😊':'4' , '😘':'5' , '💪':'6' , '😉':'7' , '👌':'8' , '🇪🇸':'9' , '😎':'10' , '💙':'11' , '💜':'12' , '😜':'13' , '💞':'14' , '✨':'15' , '🎶':'16' , '💘':'17' , '😁':'18' , '	':'19'}
		else:
			sys.exit('Need to pass "us" or "es" to decide what labels to use')
		
		main()
  
	else:
		sys.exit('''
			Requires:
			- Path to files with tweets (text of the tweets one per line)
			- "us" or "es" to decide the labels to use'
			''')
