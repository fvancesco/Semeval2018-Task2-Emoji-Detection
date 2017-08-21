# -*- coding: utf-8 -*-

'''
---- Emoji extractor-----
Given a file with one tweet per line, return two files with text without emois and correct label for semeval emoji detection 2018
WARNING! We skip the tweet if: 
	-the tweet do not contain the emojis that we use as labels
	-the tweet contains more than one type of emoji

Instructions:
1) Install emoji library (use fvancesco's version as at the moment carpedm20's original version has some issues) 
$ git clone https://github.com/fvancesco/emoji.git
$ cd emoji
$ sudo python setup.py install

2) Extract emojis from 
a. first param =  Path to file with tweets (one per line). It can contain the text of the tweets (one per line), or the twitter json(one per line). 
                  If it is the twitter json, please add the extention .json at the end.
b. second param = "us" or "es" to decide what label mapping to use

For example:
1.
For a file containng the text of american tweets (one per line): 
$ python emoji_extractor_semeval18.py tweets_us.txt us

2.
For a file containng the json of american tweets (one per line): 
$ python emoji_extractor_semeval18.py tweets_es.json us
'''

#from codecs import open
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import emoji
import json

def clean_text(text):
	#remove emojis, remove links, anonymize user mentions
	clean = ""
	text = emoji.replace_emoji(text, replacement=' ')
	for t in text.split(" "):
		if t.startswith('@') and len(t) > 1: 
			clean += "@user "
		elif t == '' or t.startswith('http'): 
			pass
		else:
			clean += t + " "
	return clean

def main():
	out_text = open(tweets_file+".text",'w')
	out_labels = open(tweets_file+".labels",'w')
	tot=0
	ok=0
	with open(tweets_file) as f_in:
		for line in f_in:
			if ".json" in tweets_file: 
				j = json.loads(line)
				text = j['text'].replace("\n","")
			else: 
				text = line 

			emo_list = emoji.emoji_list(text)
			emo_set = set([d['code'] for d in emo_list if 'code' in d])
			if len(emo_set) == 1:
				emo = emo_set.pop().encode('utf_8')
				if emo in mapping:
					ct= clean_text(text)
					out_text.write(ct+"\n")
					out_labels.write(mapping[emo]+"\n")
					ok+=1
					#print "-------------------------------"
					#print text
					#print clean_text(text)
					#print mapping[emo]
			if tot % 10000 == 0:
				print str(tot)
			tot+=1


	print str(ok) + " good examples out of " + str(tot)

	out_text.close()
	out_labels.close()


if __name__ == '__main__':

	args = sys.argv[1:]
	if len(args) == 2:
		tweets_file = args[0]
		lang = args[1]

		if 'us' in lang:
			mapping = { '❤':'0' , '😍':'1' , '😂':'2' , '💕':'3' , '😊':'4' , '😘':'5' , '💪':'6' , '😉':'7' , '👌':'8' , '🇪🇸':'9' , '😎':'10' , '💙':'11' , '💜':'12' , '😜':'13' , '💞':'14' , '✨':'15' , '🎶':'16' , '💘':'17' , '😁':'18' , '	':'19'}
		elif 'es' in lang:
			mapping = { '❤':'0' , '😍':'1' , '😂':'2' , '💕':'3' , '🔥':'4' , '😊':'5' , '😎':'6' , '✨':'7' , '💙':'8' , '😘':'9' , '📷':'10' , '🇺🇸':'11' , '☀':'12' , '💜':'13' , '😉':'14' , '💯':'15' , '😁':'16' , '🎄':'17' , '📸':'18' , '😜':'19'}
		else:
			sys.exit('Need to pass "us" or "es" to decide what labels to use')
		
		main()
  
	else:
		sys.exit('''
			Requires:
			- Path to files with tweets (text of the tweets one per line)
			- "us" or "es" to decide the labels to use'
			''')