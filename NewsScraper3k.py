import feedparser as fp
import json
import newspaper
from newspaper import Article
from time import mktime
from datetime import datetime
import csv
import sqlite3

#create news database
conn = sqlite3.connect('newsdb_v4.sqlite')
conn.text_factory = bytes
cur = conn.cursor()

# Make some fresh tables using executescript()

try:
    cur.executescript('''

    CREATE TABLE Headlines (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        date    TEXT, 
        authors TEXT,
        url     TEXT UNIQUE,
        headline TEXT,
        keywords TEXT,
        summary TEXT,
        content TEXT
    );

    ''')
except:
    print("database already exists")




# Set the limit for number of articles to download
LIMIT = 100

data = {}
data['newspapers'] = {}

currentDT = datetime.now()
script_date = str(currentDT.year) + "_" + str(currentDT.month) + "_" + str(currentDT.day) 
print(script_date)

# Loads the JSON files with news sites
with open('NewsPapers.json') as data_file:
    companies = json.load(data_file)

count = 1

csv_articles  = []
# Iterate through each news company
for company, value in companies.items():
    # If a RSS link is provided in the JSON file, this will be the first choice.
    # Reason for this is that, RSS feeds often give more consistent and correct data.
    # If you do not want to scrape from the RSS-feed, just leave the RSS attr empty in the JSON file.
    if 'rss' in value:
        d = fp.parse(value['rss'])
        print("Downloading articles from ", company)
        newsPaper = {
            "rss": value['rss'],
            "link": value['link'],
            "articles": []
        }
        for entry in d.entries:
            # Check if publish date is provided, if no the article is skipped.
            # This is done to keep consistency in the data and to keep the script from crashing.
            if hasattr(entry, 'published'):
                if count > LIMIT:
                    break
                article = {}
                article['link'] = entry.link
                date = entry.published_parsed
                try:
                    article['published'] = datetime.fromtimestamp(mktime(date))
                except:
                    print("no date")
                try:
                    content = Article(entry.link)
                    content.download()
                    content.parse()
                except Exception as e:
                    # If the download for some reason fails (ex. 404) the script will continue downloading
                    # the next article.
                    print(e)
                    print("continuing...")
                    continue
                article['title'] = content.title
                article['text'] = content.text
                article['date'] = content.publish_date
                article['authors'] = '-'.join(content.authors)
                article['headline'] = content.title
                content.nlp()
                article['keywords'] = '-'.join(content.keywords)
                article['summary'] = content.summary 

                # put this in a db
                cur.execute('''INSERT OR REPLACE INTO Headlines
                (date, authors, url, headline, keywords, summary, content) 
                VALUES ( ?, ?, ?, ?, ?, ?, ?)''', 
                ( article['date'], article['authors'], article['link'], article['headline'], article['keywords'], 
                    article['summary'], article['text'] ) )
                conn.commit()



                
                csv_article  = {}
                csv_article['headline'] = content.title
                csv_article['date'] = content.publish_date
                csv_article['authors'] = ':'.join(content.authors)
                csv_article['link'] = content.url
                csv_articles.append(csv_article)

                #print article['title'] 
                
                
                newsPaper['articles'].append(article)
                print(count, "articles downloaded from", company, ", url: ", entry.link)
                count = count + 1
    else:
        # This is the fallback method if a RSS-feed link is not provided.
        # It uses the python newspaper library to extract articles
        print("Building site for ", company)
        paper = newspaper.build(value['link'], memoize_articles=False)
        newsPaper = {
            "link": value['link'],
            "articles": []
        }
        noneTypeCount = 0
        for content in paper.articles:
            if count > LIMIT:
                break
            try:
                content.download()
                content.parse()
            except Exception as e:
                print(e)
                print("continuing...")
                continue
            # Again, for consistency, if there is no found publish date the article will be skipped.
            # After 10 downloaded articles from the same newspaper without publish date, the company will be skipped.
            if content.publish_date is None:
                print(count, " Article has date of type None...")
                noneTypeCount = noneTypeCount + 1
                if noneTypeCount > 10:
                    print("Too many noneType dates, aborting...")
                    noneTypeCount = 0
                    break
                count = count + 1
                continue
            article = {}
            article['title'] = content.title
            article['text'] = content.text
            article['authors'] = ':'.join(content.authors)
            article['link'] = content.url
            article['date'] = content.publish_date
            article['headline'] = content.title
            content.nlp()
            article['keywords'] = '-'.join(content.keywords)
            article['summary'] = content.summary 
             # put this in a db
            cur.execute('''INSERT OR REPLACE INTO Headlines
            (date, authors, url, headline, keywords, summary, content) 
            VALUES ( ?, ?, ?, ?, ?, ?, ?)''', 
            ( article['date'], article['authors'], article['link'], article['headline'], article['keywords'], 
                article['summary'], article['text'] ) )
            conn.commit()

            try:
                article['published'] = content.publish_date.isoformat()
            except:
                print("bad date")

            csv_article  = {}
            csv_article['headline'] = content.title
            csv_article['authors'] = ':'.join(content.authors)
            try:
                csv_article['date'] = content.publish_date.isoformat()
            except:
                print("bad date")

            csv_article['link'] = content.url

            csv_articles.append(csv_article)


            newsPaper['articles'].append(article)


           
            print(count, "articles downloaded from", company, " using newspaper, url: ", content.url)
            count = count + 1
            noneTypeCount = 0
    count = 1
    data['newspapers'][company] = newsPaper

# Finally it saves the articles as a JSON-file.
#try:
#    with open('scraped_articles2.json', 'w') as outfile:
#        json.dump(data, outfile)
#except Exception as e: print(e)

OUTFILE = "headlines_%s.csv" % script_date
with open(OUTFILE, 'w') as output_file:
    keys = ['headline', 'date', 'authors', 'link']
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    for row in csv_articles:
        try:
            dict_writer.writerow(row)
        except:
            print("couldn't write row data")
    





