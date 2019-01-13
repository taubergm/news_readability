import sqlite3
import textstat
import nltk
import re
import csv 
from textblob import TextBlob
from afinn import Afinn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
afinn = Afinn()

# NOTE - the textstat lib sentence count function doesn't work. I fixed it by using the nltk sentence tokenizer 

def get_story_lengths(story):
	num_words = 0 
	num_sentences = 0
	num_chars = 0
	sentences = nltk.sent_tokenize(story)
	for sent in sentences:

		num_sentences = num_sentences + 1
		#words = nltk.word_tokenize(sent)
		words = tokenizer.tokenize(sent)
		num_words = num_words + len(words)
		for word in words:
			num_chars = num_chars + len(list(word))

	return (num_chars, num_words, num_sentences)


def get_vader_sentiment(story):
	analyzer = SentimentIntensityAnalyzer()
	total_sentiment = 0
	num_sentences = 0
	sentences = nltk.sent_tokenize(story)
	for sent in sentences:
		num_sentences = num_sentences + 1
		sentiment = analyzer.polarity_scores(sent)['compound']
		total_sentiment = total_sentiment + sentiment

	avg_vs = total_sentiment/num_sentences

	return avg_vs

#def get_afinn_sentiment(story):

news_data = {}
row = {}
row['publication'] = ""
row['num_chars'] = 0 
row['num_words'] = 0 
row['num_sentences'] = 0 
row['avg_word_length'] = 0
row['avg_sent_length'] = 0
row['num_stories'] = 0
row['avg_headline_length'] = 0 
row['avg_words_per_story'] = 0 
row['avg_flesch_reading_ease_score'] = 0 
row['avg_flesch_kincaid_grade'] = 0 
row['avg_smog_reading_ease_score'] = 0 
row['avg_text_standard_score'] = 0 
row['avg_dale_chall_readability_score'] = 0 
row['avg_gunning_fog_score'] = 0
row['avg_automated_readability_index'] = 0  
row['worst_readability_score'] = 0 
row['worst_readability_headline'] = 0
row['worst_sentiment_score'] = 0 
row['worst_sentiment_headline'] = 0
row['best_readability_score'] = 0 
row['best_readability_headline'] = 0
row['best_sentiment_score'] = 0 
row['best_sentiment_headline'] = 0
row['avg_textblob_sentiment'] = 0
row['avg_afinn_sentiment'] = 0
row['avg_vader_sentiment'] = 0
row['avg_vader_headline_sentiment'] = 0

news_data['nyt'] = row
news_data['cnn'] = row.copy()
news_data['fox'] = row.copy()
news_data['msnbc'] = row.copy()
news_data['vox'] = row.copy()
news_data['wsj'] = row.copy()
news_data['latimes'] = row.copy()
news_data['bostonglobe'] = row.copy()
news_data['dailycaller'] = row.copy()
news_data['usatoday'] = row.copy()
news_data['rt'] = row.copy()
news_data['npr'] = row.copy()
news_data['huffpo'] = row.copy()
news_data['politico'] = row.copy()
news_data['buzzfeed'] = row.copy()
news_data['breitbart'] = row.copy()
news_data['nypost'] = row.copy()
news_data['washingtonpost'] = row.copy()
news_data['bbc'] = row.copy()
news_data['guardian'] = row.copy()
news_data['infowars'] = row.copy()

headline = ""
story = ""
url = ""

def set_newsdict_values(news_dict, story_stats):
	news_dict['num_stories'] 	= news_dict['num_stories'] + 1
	news_dict['num_chars'] 		= news_dict['num_chars'] + story_stats['num_chars']
	news_dict['num_words'] 		= news_dict['num_words'] + story_stats['num_words']
	news_dict['num_sentences'] 	= news_dict['num_sentences'] + story_stats['num_sentences']

	# sum these for now, average them at the end (not great I know)
	news_dict['avg_headline_length'] 				= news_dict['avg_headline_length'] + story_stats['avg_headline_length']
	news_dict['avg_flesch_reading_ease_score'] 		= news_dict['avg_flesch_reading_ease_score'] + story_stats['flesch_reading_ease_score']
	news_dict['avg_flesch_kincaid_grade'] 			= news_dict['avg_flesch_kincaid_grade'] + story_stats['flesch_kincaid_grade']
	news_dict['avg_smog_reading_ease_score'] 		= news_dict['avg_smog_reading_ease_score'] + story_stats['smog_reading_ease_score']
	news_dict['avg_text_standard_score'] 			= news_dict['avg_text_standard_score'] + story_stats['text_standard_score']
	news_dict['avg_dale_chall_readability_score'] 	= news_dict['avg_dale_chall_readability_score'] + story_stats['dale_chall_readability_score']
	news_dict['avg_gunning_fog_score'] 				= news_dict['avg_gunning_fog_score'] + story_stats['gunning_fog_score']
	news_dict['avg_automated_readability_index'] 	= news_dict['avg_automated_readability_index'] + story_stats['automated_readability_index']
	news_dict['avg_textblob_sentiment'] 			= news_dict['avg_textblob_sentiment'] + story_stats['textblob_sentiment']
	news_dict['avg_afinn_sentiment'] 				= news_dict['avg_afinn_sentiment'] + story_stats['afinn_sentiment']
	news_dict['avg_vader_sentiment'] 				= news_dict['avg_vader_sentiment'] + story_stats['vader_sentiment']
	news_dict['avg_vader_headline_sentiment'] 		= news_dict['avg_vader_headline_sentiment'] + story_stats['vader_headline_sentiment']

	# new worst sentiment discovered
	if (story_stats['vader_sentiment'] < news_dict['worst_sentiment_score']):
		news_dict['worst_sentiment_score'] = story_stats['vader_sentiment']
		news_dict['worst_sentiment_headline'] = story_stats['worst_sentiment_headline']
		
	# new worst readability discovered
	if (story_stats['text_standard_score'] > news_dict['worst_readability_score']):
		news_dict['worst_readability_score'] = story_stats['text_standard_score']
		news_dict['worst_readability_headline'] = story_stats['worst_readability_headline']
	
	# new best sentiment discovered
	if (story_stats['vader_sentiment'] > news_dict['best_sentiment_score']):
		news_dict['best_sentiment_score'] = story_stats['vader_sentiment']
		news_dict['best_sentiment_headline'] = story_stats['best_sentiment_headline']
		
	# new best readability discovered
	if (story_stats['text_standard_score'] < news_dict['best_readability_score']):
		news_dict['best_readability_score'] = story_stats['text_standard_score']
		news_dict['best_readability_headline'] = story_stats['best_readability_headline']



	print(news_dict['num_stories'])



# call these on all news sources

sqlite_file = '/Users/michaeltauberg/projects/NewsScraper/newsdb_v2.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


# eg select * from Headlines where url like "%cnn.com%"
#c.execute('SELECT * FROM {tn} WHERE {cn} like "%cnn.com%"'\
#        .format(tn="Headlines", cn="url"))
#all_rows = c.fetchall()
# seems faster to do specific queuries  than python regex]##
## ------
#c.execute('SELECT * FROM {tn}'\
#        .format(tn="Headlines"))



def get_news_data(publication):

	if (publication == "nyt"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.nytimes.com%"'\
	        .format(tn="Headlines", cn="url"))
	elif (publication == "cnn"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%cnn.com%"'\
	        .format(tn="Headlines", cn="url"))
	elif (publication == "fox"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.foxnews.com%"'\
	        .format(tn="Headlines", cn="url"))
	elif (publication == "msnbc"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.msnbc.com%"'\
	        .format(tn="Headlines", cn="url"))
	elif (publication == "vox"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.vox.com%"'\
	        .format(tn="Headlines", cn="url"))
	elif (publication == "wsj"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.wsj.com%"'\
	        .format(tn="Headlines", cn="url"))
	elif (publication == "latimes"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.latimes.com%"'\
	        .format(tn="Headlines", cn="url"))	
	elif (publication == "bostonglobe"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.bostonglobe.com%"'\
	        .format(tn="Headlines", cn="url"))	
	elif (publication == "dailycaller"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%dailycaller.com%"'\
	        .format(tn="Headlines", cn="url"))	
	elif (publication == "usatoday"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.usatoday.com%"'\
	        .format(tn="Headlines", cn="url"))	
	elif (publication == "rt"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.rt.com%"'\
	        .format(tn="Headlines", cn="url"))	
	elif (publication == "npr"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.npr.org%"'\
	        .format(tn="Headlines", cn="url"))	
	elif (publication == "huffpo"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.huffingtonpost.com%"'\
	        .format(tn="Headlines", cn="url"))	
	elif (publication == "politico"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.politico.com%"'\
	        .format(tn="Headlines", cn="url"))	
	elif (publication == "buzzfeed"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.buzzfeednews.com%"'\
	        .format(tn="Headlines", cn="url"))	
	elif (publication == "breitbart"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.breitbart.com%"'\
	        .format(tn="Headlines", cn="url"))	
	elif (publication == "infowars"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.infowars.com%"'\
	        .format(tn="Headlines", cn="url"))	
	elif (publication == "nypost"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%nypost.com%"'\
	        .format(tn="Headlines", cn="url"))	
	elif (publication == "washingtonpost"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.washingtonpost.com%"'\
	        .format(tn="Headlines", cn="url"))
	elif (publication == "bbc"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%bbc.co%"'\
	        .format(tn="Headlines", cn="url"))	
	elif (publication == "guardian"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.theguardian.com%"'\
	        .format(tn="Headlines", cn="url"))	
	
	all_rows = c.fetchall()

	i = 0
	for row in all_rows:
		url = row[3] 
		#try:
		#	headline = row[4].decode('utf-8') 
		#except:
		#	headline = row[4]
		if (isinstance(row[4], str)):
			headline = row[4]
		else:
			headline = row[4].decode('utf-8') # some headlines got in as bytes for some reason
		story = row[5]

		
		if (len(story) < 1000): # skip really short articles -> these screw up statistics
			continue
		if (detect(headline) != 'en'):  # skip stories that aren't in english (some chinese got through)
			continue

		story_stats = {}


		story_stats['flesch_kincaid_grade'] = textstat.flesch_kincaid_grade(story)
		story_stats['flesch_reading_ease_score'] = textstat.flesch_reading_ease(story)
		story_stats['smog_reading_ease_score'] = textstat.smog_index(story)
		story_stats['text_standard_score'] = textstat.text_standard(story, float_output=True)
		story_stats['dale_chall_readability_score'] = textstat.dale_chall_readability_score(story)
		story_stats['gunning_fog_score'] = textstat.gunning_fog(story)
		story_stats['automated_readability_index'] = textstat.automated_readability_index(story)
		story_stats['avg_headline_length'] = len(tokenizer.tokenize(headline))
		story_stats['textblob_sentiment'] = TextBlob(story).sentiment.polarity
		story_stats['afinn_sentiment'] = afinn.score(story)
		story_stats['vader_sentiment'] = get_vader_sentiment(story)
		story_stats['worst_readability_headline'] = headline
		story_stats['worst_sentiment_headline'] = headline
		story_stats['best_readability_headline'] = headline
		story_stats['best_sentiment_headline'] = headline
		story_stats['vader_headline_sentiment'] = get_vader_sentiment(headline)

		#num_words = textstat.lexicon_count(story, removepunct=True)  # number of words
		#num_sentences = textstat.sentence_count(story)  # number of sentences from base textstate is wrong
		(story_stats['num_chars'], story_stats['num_words'], story_stats['num_sentences']) = get_story_lengths(story)

		#if re.match("cn.nytimes.com.*", url) is not None:
		#	continue
		

		if (publication == "nyt"):
			print('NYT')
			#print(headline, url)
			news_data['nyt']['publication'] = "nyt"
			set_newsdict_values(news_data['nyt'], story_stats)
		#elif re.match(".*cnn.com.*", url) is not None:
		elif (publication == "cnn"):
			print('CNN')
			#print(headline, url)
			news_data['cnn']['publication'] = "cnn"
			set_newsdict_values(news_data['cnn'], story_stats)
		#elif re.match(".foxnews.com%", url) is not None:
		elif (publication == "fox"):
			print('FOX')
			#print(headline, url)
			news_data['fox']['publication'] = "fox"
			set_newsdict_values(news_data['fox'], story_stats)
		elif (publication == "msnbc"):
			print('MSNBC')
			#print(headline, url)
			news_data['msnbc']['publication'] = "msnbc"
			set_newsdict_values(news_data['msnbc'], story_stats)
		elif (publication == "vox"):
			print('VOX')
			#print(headline, url)
			news_data['vox']['publication'] = "vox"
			set_newsdict_values(news_data['vox'], story_stats)
		elif (publication == "wsj"):
			print('WSJ')
			#print(headline, url)
			news_data['wsj']['publication'] = "wsj"
			set_newsdict_values(news_data['wsj'], story_stats)
		elif (publication == "latimes"):
			print('LATIMES')
			#print(headline, url)
			news_data['latimes']['publication'] = "latimes"
			set_newsdict_values(news_data['latimes'], story_stats)
		elif (publication == "bostonglobe"):
			print('bostonglobe')
			#print(headline, url)
			news_data['bostonglobe']['publication'] = "bostonglobe"
			set_newsdict_values(news_data['bostonglobe'], story_stats)
		elif (publication == "dailycaller"):
			print('dailycaller')
			#print(headline, url)
			news_data['dailycaller']['publication'] = "dailycaller"
			set_newsdict_values(news_data['dailycaller'], story_stats)
		elif (publication == "usatoday"):
			print('usatoday')
			#print(headline, url)
			news_data['usatoday']['publication'] = "usatoday"
			set_newsdict_values(news_data['usatoday'], story_stats)
		elif (publication == "rt"):
			print('rt')
			#print(headline, url)
			news_data['rt']['publication'] = "rt"
			set_newsdict_values(news_data['rt'], story_stats)
		elif (publication == "npr"):
			print('npr')
			#print(headline, url)
			news_data['npr']['publication'] = "npr"
			set_newsdict_values(news_data['npr'], story_stats)
		elif (publication == "huffpo"):
			print('huffpo')
			#print(headline, url)
			news_data['huffpo']['publication'] = "huffpo"
			set_newsdict_values(news_data['huffpo'], story_stats)
		elif (publication == "politico"):
			print('politico')
			#print(headline, url)
			news_data['politico']['publication'] = "politico"
			set_newsdict_values(news_data['politico'], story_stats)
		elif (publication == "buzzfeed"):
			print('buzzfeed')
			#print(headline, url)
			news_data['buzzfeed']['publication'] = "buzzfeed"
			set_newsdict_values(news_data['buzzfeed'], story_stats)
		elif (publication == "breitbart"):
			print('breitbart')
			#print(headline, url)
			news_data['breitbart']['publication'] = "breitbart"
			set_newsdict_values(news_data['breitbart'], story_stats)
		elif (publication == "infowars"):
			print('infowars')
			#print(headline, url)
			news_data['infowars']['publication'] = "infowars"
			set_newsdict_values(news_data['infowars'], story_stats)
		elif (publication == "nypost"):
			print('nypost')
			#print(headline, url)
			news_data['nypost']['publication'] = "nypost"
			set_newsdict_values(news_data['nypost'], story_stats)
		elif (publication == "washingtonpost"):
			print('washingtonpost')
			#print(headline, url)
			news_data['washingtonpost']['publication'] = "washingtonpost"
			set_newsdict_values(news_data['washingtonpost'], story_stats)
		elif (publication == "bbc"):
			print('bbc')
			#print(headline, url)
			news_data['bbc']['publication'] = "bbc"
			set_newsdict_values(news_data['bbc'], story_stats)
		elif (publication == "guardian"):
			print('guardian')
			#print(headline, url)
			news_data['guardian']['publication'] = "guardian"
			set_newsdict_values(news_data['guardian'], story_stats)

# word clouds 



get_news_data("nyt")
get_news_data("fox")
get_news_data("cnn")
get_news_data("msnbc")
get_news_data("vox")
get_news_data("wsj")
get_news_data("latimes")
get_news_data("bostonglobe")
get_news_data("dailycaller")
get_news_data("usatoday")
get_news_data("rt")
get_news_data("npr")
get_news_data("huffpo")
get_news_data("politico")
get_news_data("buzzfeed")
get_news_data("breitbart")
get_news_data("infowars")
get_news_data("nypost")
get_news_data("washingtonpost")
get_news_data("bbc")
get_news_data("guardian")


def average_dict_values(news_dict):
	try:
		news_dict['avg_word_length'] = news_dict['num_chars']/news_dict['num_words']
		news_dict['avg_sent_length'] = news_dict['num_words']/news_dict['num_sentences'] 
		news_dict['avg_words_per_story'] = news_dict['num_words']/news_dict['num_stories']
		news_dict['avg_headline_length'] = news_dict['avg_headline_length'] / news_dict['num_stories']
		news_dict['avg_flesch_kincaid_grade'] = news_dict['avg_flesch_kincaid_grade'] / news_dict['num_stories']
		news_dict['avg_flesch_reading_ease_score'] = news_dict['avg_flesch_reading_ease_score'] / news_dict['num_stories']
		news_dict['avg_smog_reading_ease_score'] = news_dict['avg_smog_reading_ease_score'] / news_dict['num_stories']
		news_dict['avg_text_standard_score'] = news_dict['avg_text_standard_score'] / news_dict['num_stories']
		news_dict['avg_dale_chall_readability_score'] = news_dict['avg_dale_chall_readability_score'] / news_dict['num_stories']
		news_dict['avg_gunning_fog_score'] = news_dict['avg_gunning_fog_score'] / news_dict['num_stories']
		news_dict['avg_automated_readability_index'] = news_dict['avg_automated_readability_index'] / news_dict['num_stories']
		news_dict['avg_textblob_sentiment'] = news_dict['avg_textblob_sentiment'] / news_dict['num_stories']
		news_dict['avg_afinn_sentiment'] = news_dict['avg_afinn_sentiment'] / news_dict['num_stories']
		news_dict['avg_vader_sentiment'] = news_dict['avg_vader_sentiment'] / news_dict['num_stories']
		news_dict['avg_vader_headline_sentiment'] = news_dict['avg_vader_headline_sentiment'] / news_dict['num_stories']
	except:
		print("averaging failed. Some value is 0")

# average the values that were running sums so fae
average_dict_values(news_data['nyt'])
average_dict_values(news_data['fox'])
average_dict_values(news_data['cnn'])
average_dict_values(news_data['msnbc'])
average_dict_values(news_data['vox'])
average_dict_values(news_data['wsj'])
average_dict_values(news_data['latimes'])
average_dict_values(news_data['bostonglobe'])
average_dict_values(news_data['dailycaller'])
average_dict_values(news_data['usatoday'])
average_dict_values(news_data['rt'])
average_dict_values(news_data['npr'])
average_dict_values(news_data['huffpo'])
average_dict_values(news_data['politico'])
average_dict_values(news_data['buzzfeed'])
average_dict_values(news_data['breitbart'])
average_dict_values(news_data['infowars'])
average_dict_values(news_data['nypost'])
average_dict_values(news_data['washingtonpost'])
average_dict_values(news_data['bbc'])
average_dict_values(news_data['guardian'])

# print to csv
# output stats csv definition
output_csv_name = "news_stats_v4.csv"
fieldnames = [
                'publication', 'num_stories', 'num_sentences', 'num_words', 'num_chars',
                'avg_word_length', 'avg_sent_length', 'avg_story_sentiment', 
                'avg_headline_length',	'avg_words_per_story', 'avg_flesch_reading_ease_score', 
                'avg_smog_reading_ease_score', 'avg_text_standard_score', 'avg_dale_chall_readability_score', 
                'avg_gunning_fog_score', 'avg_automated_readability_index', 'worst_readability_score',
                'worst_readability_headline', 'avg_textblob_sentiment',
                'avg_afinn_sentiment', 'avg_vader_sentiment', 'avg_vader_headline_sentiment',
                'worst_sentiment_score', 'worst_sentiment_headline', 'best_sentiment_score',
                'best_sentiment_headline', 'best_readability_score', 'best_readability_headline',
                'avg_flesch_kincaid_grade'
             ]

with open(output_csv_name, 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames)
    dict_writer.writeheader()

    for key in news_data.keys():
    	print(news_data[key])
    	#try:
    	dict_writer.writerow(news_data[key])
    	#except:
    	#	print("couldn't write row data")



# find Friedman articles
#19/52 sentences of his are hard to read
# do trump's tweets for fun




