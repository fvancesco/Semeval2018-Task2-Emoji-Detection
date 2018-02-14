Quick start:

1) In crawler.properties set you personal twitter keys (we suggest to add more than one twitter app to speed up the process: with only one app it will take about two days to download all the tweets)

2) In crawler.properties set up the up one of the two files containing the list of twitter IDs:
	- train_us_semeval18.ids
	- train_es_semeval18.ids

3) Run the crawler with:
java -cp './twitter-crawler-0.4.jar:./lib/*' org.backingdata.twitter.crawler.rest.TwitterRESTTweetIDlistCrawler crawler.properties

More info at:  
https://github.com/fra82/twitter-crawler/blob/master/semeval2018task2TwitterCrawlerHOWTO.md

————————————————————————————————————
To get the twitter keys:
1) Create a Twitter user account
2) Go to https://apps.twitter.com/ and log in with your Twitter user account.
3) Click “Create New App” and fill out the form, agree to the terms, and click “Create your Twitter application”
4) In the next page, click on “Keys and Access Tokens” tab, and copy your “API key” and “API secret”. Scroll down and click “Create my access token”, and copy your “Access token” and “Access token secret”.