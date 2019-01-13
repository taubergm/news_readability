
import sqlite3
import nltk
from gensim.models import Word2Vec
import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import RegexpTokenizer
from wordcloud import WordCloud

tokenizer = RegexpTokenizer(r'\w+')

sqlite_file = '/Users/michaeltauberg/projects/NewsScraper/newsdb_v2.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

def get_news_data(publication):

	headlines = []
	content = []
	corpus = ""

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
	elif (publication == "infowars"):
		c.execute('SELECT * FROM {tn} WHERE {cn} like "%www.infowars.com%"'\
	        .format(tn="Headlines", cn="url"))	
	all_rows = c.fetchall()


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

		
		headline = headline.lower()
		words = tokenizer.tokenize(headline)
		headlines.append(words)

		#sentences = nltk.sent_tokenize(story)
		#for sent in sentences:
		#	sent = sent.lower()
		#	words = tokenizer.tokenize(sent)
		#	content.append(words)


	#create a big string of all headlines to make word clouds  
	headlines = []
	for row in all_rows:
		headline = str(row[4])
		#print(headline)
		headlines.append(headline)
	
	words = ''.join(headlines)
	print(len(words))
	

	wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(words)
		
	return (headlines,content)


def plot_tuples(data, source, subject):

    
    fig = plt.figure()

    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]
    y_pos = np.arange(len(x_val))
    #plt.plot(x_val,y_val)
    #plt.plot(x_val,y_val,'or')

    #print(y_pos)
    print(y_val)
    print(x_val)
    plt.bar(y_pos, y_val, align='center', alpha=0.5, figure=fig)    
    plt.ylabel('Similarity', figure=fig)
    plt.xticks(y_pos, x_val, figure=fig)
    plt.xticks(rotation=90, figure=fig)
    plt.title(source + ' Words like ' + '\'' + subject + '\'', figure=fig)
    #plt.show()
    #plt.savefig(title + '.png', bbox_inches='tight')
    fig.savefig(source + '_' + subject + '.png', bbox_inches='tight')




(headlines,content) = get_news_data('nyt')
#print(content)
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'nyt', 'trump')

(headlines,content) = get_news_data('cnn')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'cnn', 'trump')

(headlines,content) = get_news_data('fox')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'fox' , 'trump')

(headlines,content) = get_news_data('msnbc')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'msnbc' , 'trump')

(headlines,content) = get_news_data('vox')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'vox' , 'trump')

(headlines,content) = get_news_data('wsj')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'wsj' , 'trump')

(headlines,content) = get_news_data('latimes')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'latimes' , 'trump')

(headlines,content) = get_news_data('bostonglobe')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'bostonglobe' , 'trump')

(headlines,content) = get_news_data('dailycaller')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'dailycaller', 'trump')

(headlines,content) = get_news_data('usatoday')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'usatoday' , 'trump')


(headlines,content) = get_news_data('rt')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'rt' , 'trump')

(headlines,content) = get_news_data('npr')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'npr', 'trump')

(headlines,content) = get_news_data('huffpo')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'huffpo', 'trump')

(headlines,content) = get_news_data('politico')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'politico', 'trump')

(headlines,content) = get_news_data('buzzfeed')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'buzzfeed', 'trump')

(headlines,content) = get_news_data('breitbart')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'breitbart', 'trump')


(headlines,content) = get_news_data('infowars')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'infowars', 'trump')

(headlines,content) = get_news_data('nypost')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'nypost', 'trump')

(headlines,content) = get_news_data('washingtonpost')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'washingtonpost', 'trump')

(headlines,content) = get_news_data('bbc')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'bbc', 'trump')

(headlines,content) = get_news_data('guardian')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'guardian', 'trump')

(headlines,content) = get_news_data('infowars')
model_ted = Word2Vec(sentences=content, size=100, window=6, min_count=4, workers=4, sg=0)
trump = (model_ted.wv.most_similar('trump', topn=5))
print(trump)
plot_tuples(trump, 'infowars', 'trump')

