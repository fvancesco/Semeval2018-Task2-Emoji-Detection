Emoji extractor
===== 

Given a file with one tweet per line, return two files:
	
* file.text, includes all the tweets of the input file, where emojis and links are removed, and mentions are anonymizided with "@user"
* file.labels, includes the label of each tweet of the previous file, in the same order. The labels are number from 0 to 19, as specified in the task.
	
WARNING! We skip the tweet if: 
	
* the tweet do not contain the emojis that we use as labels
* the tweet contains more than one type of emoji

Instructions
-----------------
1. **Install emoji library** 

*(use fvancesco's version, as we use specific funcions implemented there)* 

```bash
$ git clone https://github.com/fvancesco/emoji.git
$ cd emoji
$ sudo python setup.py install
```

2. **Extract emojis**

	* First param =  Path to file with tweets (one per line). It can contain the text of the tweets (one per line), or the twitter json (one per line).  If you pass the twitter json, please add the extention .json at the end of the filename.

	* Second param = "us" or "es" to decide what label mapping to use

For example:

For a file containng the text of the american tweets (one per line): 

```bash
$ python emoji_extractor_semeval18.py tweets_us.txt us
```
For a file containng the json of the american tweets (one per line): 

```bash
$ python emoji_extractor_semeval18.py tweets_us.json us
```
