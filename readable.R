if (!require(ggplot2)) {
  install.packages("ggplot2", repos="http://cran.us.r-project.org")
}
library("ggplot2")
if (!require(plyr)) {
  install.packages("plyr", repos="http://cran.us.r-project.org")
}
library(plyr)
if (!require(data.table)) {
  install.packages("data.table", repos="http://cran.us.r-project.org")
}
library(data.table)
if (!require(waffle)) {
  install.packages("waffle", repos="http://cran.us.r-project.org")
}
library(waffle)
if (!require(ggthemes)) {
  install.packages("ggthemes", repos="http://cran.us.r-project.org")
}
library(ggthemes)

workingDir = '/Users/michaeltauberg/projects/NewsScraper/'
#csvName = "news_stats_color.csv"
csvName = "news_stats_v4_color.csv"
data_name = "readable"
setwd(workingDir)

dt = read.csv(csvName)

# fix politico colors


# SENTIMENT
# ---------
data_name = "vader"
dt = dt[order(dt$avg_vader_sentiment, decreasing=TRUE),]
colors = as.character(dt$color)
names(colors) = as.character(dt$publication)
dt$publication = factor(dt$publication, levels = dt$publication[order(dt$avg_vader_sentiment, decreasing=TRUE)])
p = ggplot(dt, aes(x=publication, y=avg_vader_sentiment, fill=publication)) + geom_bar(stat="identity") 
p = p + ggtitle("News Publication by Story Sentiment")
p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
p = p + theme(axis.text=element_text(size=14), axis.title=element_text(size=14,face="bold"))
p = p + xlab("publication") + ylab("sentiment") 
p = p + scale_fill_manual(values=colors) + guides(fill=FALSE)
ggsave(filename = sprintf("./%s.png", data_name) , plot=p, width=10, height=7)

data_name = "afinn"
dt = dt[order(dt$avg_afinn_sentiment, decreasing=TRUE),]
dt$publication = factor(dt$publication, levels = dt$publication[order(dt$avg_afinn_sentiment, decreasing=TRUE)])
p = ggplot(dt, aes(x=publication, y=avg_afinn_sentiment, fill=publication)) + geom_bar(stat="identity") 
p = p + ggtitle("News Publication by Story Sentiment")
p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
p = p + theme(axis.text=element_text(size=14), axis.title=element_text(size=14,face="bold"))
p = p + xlab("publication") + ylab("sentiment") 
p = p + scale_fill_manual(values=colors) + guides(fill=FALSE)
ggsave(filename = sprintf("./%s.png", data_name) , plot=p, width=10, height=7)

data_name = "textblob"
dt = dt[order(dt$avg_textblob_sentiment, decreasing=TRUE),]
dt$publication = factor(dt$publication, levels = dt$publication[order(dt$avg_textblob_sentiment, decreasing=TRUE)])
p = ggplot(dt, aes(x=publication, y=avg_textblob_sentiment, fill=publication)) + geom_bar(stat="identity") 
p = p + ggtitle("News Publication by Story Sentiment")
p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
p = p + theme(axis.text=element_text(size=14), axis.title=element_text(size=14,face="bold"))
p = p + xlab("publication") + ylab("sentiment") 
p = p + scale_fill_manual(values=colors) + guides(fill=FALSE)
ggsave(filename = sprintf("./%s.png", data_name) , plot=p, width=10, height=7)

data_name = "headline_sentiment"
dt = dt[order(dt$avg_vader_headline_sentiment, decreasing=TRUE),]
dt$publication = factor(dt$publication, levels = dt$publication[order(dt$avg_vader_headline_sentiment, decreasing=TRUE)])
p = ggplot(dt, aes(x=publication, y=avg_vader_headline_sentiment,fill=publication)) + geom_bar(stat="identity") 
p = p + ggtitle("News Publication by Avg Headline Sentiment")
p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
p = p + theme(axis.text=element_text(size=14), axis.title=element_text(size=14,face="bold"))
p = p + xlab("publication") + ylab("headline sentiment") 
p = p + scale_fill_manual(values=colors) + guides(fill=FALSE)
ggsave(filename = sprintf("./%s.png", data_name) , plot=p, width=10, height=7)



# Words/Sentences
# ---------------

# remove nytimes, wsj, latimes, bostonglobe, wapo since they have paywalls
dt2 = dt[dt$publication != "nyt",]
dt2 = dt2[dt2$publication != "wsj",]
dt2 = dt2[dt2$publication != "latimes",]
dt2 = dt2[dt2$publication != "bostonglobe",]
dt2 = dt2[dt2$publication != "washingtonpost",]
dt2 = dt2[dt2$publication != "msnbc",]

data_name = "avg_words_per_story"
dt2 = dt2[order(dt2$avg_words_per_story, decreasing=TRUE),]
dt2$publication = factor(dt2$publication, levels = dt2$publication[order(dt2$avg_words_per_story, decreasing=TRUE)])
p = ggplot(dt2, aes(x=publication, y=avg_words_per_story, fill=publication)) + geom_bar(stat="identity") 
p = p + ggtitle("News Publication by Average Words per Story")
p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
p = p + theme(axis.text=element_text(size=14), axis.title=element_text(size=14,face="bold"))
p = p + xlab("publication") + ylab("avg words per story") 
p = p + scale_fill_manual(values=colors) + guides(fill=FALSE)
ggsave(filename = sprintf("./%s.png", data_name) , plot=p, width=10, height=7)


# nypost is my favorite
# buzzfeed vs nypost - both effective
library(scales)
data_name = "avg_headline_length"
#headlines = dt[dt$publication != "infowars",]
dt = dt[order(dt$avg_headline_length, decreasing=TRUE),]
dt$publication = factor(dt$publication, levels = dt$publication[order(dt$avg_headline_length, decreasing=TRUE)])
p = ggplot(dt, aes(x=publication, y=avg_headline_length, fill=publication)) + geom_bar(stat="identity") 
p = p + ggtitle("News Publication by Average Headline Length (in words)")
p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
p = p + theme(axis.text=element_text(size=14), axis.title=element_text(size=14,face="bold"))
p = p + xlab("publication") + ylab("avg num words per headline") 
p = p + scale_fill_manual(values=colors) + guides(fill=FALSE)
p = p + scale_y_continuous(limits=c(min(dt$avg_headline_length), max(dt$avg_headline_length)), oob = rescale_none)
ggsave(filename = sprintf("./%s.png", data_name) , plot=p, width=10, height=7)

# other fun facts?
data_name = "avg_word_length"
dt = dt[order(dt$avg_word_length, decreasing=TRUE),]
dt$publication = factor(dt$publication, levels = dt$publication[order(dt$avg_word_length, decreasing=TRUE)])
p = ggplot(dt, aes(x=publication, y=avg_word_length, fill=publication)) + geom_bar(stat="identity")
#p = p + geom_point() + geom_line() 
p = p + ggtitle("News Publication by Average Word Length (characters)")
p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
p = p + theme(axis.text=element_text(size=14), axis.title=element_text(size=14,face="bold"))
p = p + xlab("publication") + ylab("avg word length") 
p = p + scale_y_continuous(limits=c(min(dt$avg_word_length), max(dt$avg_word_length)), oob = rescale_none)
p = p + scale_fill_manual(values=colors) + guides(fill=FALSE)
ggsave(filename = sprintf("./%s.png", data_name) , plot=p, width=10, height=7)

data_name = "avg_sent_length"
dt = dt[order(dt$avg_sent_length, decreasing=TRUE),]
dt$publication = factor(dt$publication, levels = dt$publication[order(dt$avg_sent_length, decreasing=TRUE)])
p = ggplot(dt, aes(x=publication, y=avg_sent_length, fill=publication)) 
#p = p + geom_point() + geom_line() 
p = p + geom_bar(stat="identity")
p = p + ggtitle("News Publication by Average Sentence Length (words)")
p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
p = p + theme(axis.text=element_text(size=14), axis.title=element_text(size=14,face="bold"))
p = p + xlab("publiation") + ylab("avg sentence length") 
p = p + scale_fill_manual(values=colors) + guides(fill=FALSE)
p = p + scale_y_continuous(limits=c(min(dt$avg_sent_length), max(dt$avg_sent_length)), oob = rescale_none)
ggsave(filename = sprintf("./%s.png", data_name) , plot=p, width=10, height=7)



# READABILITY
# ---------------
dt = dt[dt$publication != "infowars", ]
data_name = "avg_smog_reading_ease_score"
dt = dt[order(dt$avg_smog_reading_ease_score, decreasing=TRUE),]
dt$publication = factor(dt$publication, levels = dt$publication[order(dt$avg_smog_reading_ease_score, decreasing=TRUE)])
p = ggplot(dt, aes(x=publication, y=avg_smog_reading_ease_score, fill=publication)) 
#p = p + geom_point() + geom_line() 
p = p + geom_bar(stat="identity")
p = p + ggtitle("News Publication by Average Readability")
p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
p = p + theme(axis.text=element_text(size=14), axis.title=element_text(size=14,face="bold"))
p = p + xlab("publication") + ylab("avg readability") 
p = p + scale_fill_manual(values=colors) + guides(fill=FALSE)
p = p + scale_y_continuous(limits=c(min(dt$avg_smog_reading_ease_score), max(dt$avg_smog_reading_ease_score)), oob = rescale_none)
ggsave(filename = sprintf("./%s.png", data_name) , plot=p, width=10, height=7)

# The Dale–Chall formula uses 'hard words'
data_name = "avg_dale_chall_readability_score"
dt = dt[order(dt$avg_dale_chall_readability_score, decreasing=TRUE),]
dt$publication = factor(dt$publication, levels = dt$publication[order(dt$avg_dale_chall_readability_score, decreasing=TRUE)])
p = ggplot(dt, aes(x=publication, y=avg_dale_chall_readability_score, fill=publication)) 
#p = p + geom_point() + geom_line() 
p = p + geom_bar(stat="identity")
p = p + ggtitle("News Publication by Average Readability")
p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
p = p + scale_fill_manual(values=colors) + guides(fill=FALSE)
p = p + theme(axis.text=element_text(size=14), axis.title=element_text(size=14,face="bold"))
p = p + xlab("publication") + ylab("avg readability") 
p = p + scale_y_continuous(limits=c(min(dt$avg_dale_chall_readability_score), max(dt$avg_dale_chall_readability_score)), oob = rescale_none)
ggsave(filename = sprintf("./%s.png", data_name) , plot=p, width=10, height=7)


# gunning-fog = Grade level= 0.4 * ( (average sentence length) + (percentage of Hard Words) )
#Hard Words = words with more than two syllables
data_name = "avg_gunning_fog_score"
dt = dt[order(dt$avg_gunning_fog_score, decreasing=TRUE),]
dt$publication = factor(dt$publication, levels = dt$publication[order(dt$avg_gunning_fog_score, decreasing=TRUE)])
p = ggplot(dt, aes(x=publication, y=avg_gunning_fog_score, fill=publication)) 
#p = p + geom_point() + geom_line() 
p = p + geom_bar(stat="identity")
p = p + ggtitle("News Publication by Average Readability")
p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
p = p + theme(axis.text=element_text(size=14), axis.title=element_text(size=14,face="bold"))
p = p + xlab("publication") + ylab("avg readability") 
p = p + scale_fill_manual(values=colors) + guides(fill=FALSE)
p = p + scale_y_continuous(limits=c(min(dt$avg_gunning_fog_score), max(dt$avg_gunning_fog_score)), oob = rescale_none)
ggsave(filename = sprintf("./%s.png", data_name) , plot=p, width=10, height=7)


data_name = "avg_flesch_kincaid_grade"
dt = dt[order(dt$avg_flesch_kincaid_grade, decreasing=TRUE),]
dt$publication = factor(dt$publication, levels = dt$publication[order(dt$avg_flesch_kincaid_grade, decreasing=TRUE)])
p = ggplot(dt, aes(x=publication, y=avg_flesch_kincaid_grade, fill=publication)) 
#p = p + geom_point() + geom_line() 
p = p + geom_bar(stat="identity")
p = p + ggtitle("News Publication by Average Readability")
p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
p = p + theme(axis.text=element_text(size=14), axis.title=element_text(size=14,face="bold"))
p = p + xlab("publication") + ylab("avg readability") 
p = p + scale_fill_manual(values=colors) + guides(fill=FALSE)
p = p + scale_y_continuous(limits=c(min(dt$avg_flesch_kincaid_grade), max(dt$avg_flesch_kincaid_grade)), oob = rescale_none)
ggsave(filename = sprintf("./%s.png", data_name) , plot=p, width=10, height=7)

data_name = "avg_text_standard_score"
dt = dt[order(dt$avg_text_standard_score, decreasing=TRUE),]
dt$publication = factor(dt$publication, levels = dt$publication[order(dt$avg_text_standard_score, decreasing=TRUE)])
p = ggplot(dt, aes(x=publication, y=avg_text_standard_score, fill=publication)) 
#p = p + geom_point() + geom_line() 
p = p + geom_bar(stat="identity")
p = p + ggtitle("News Publication by Average Readability")
p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
p = p + theme(axis.text=element_text(size=14), axis.title=element_text(size=14,face="bold"))
p = p + xlab("publication") + ylab("avg readability") 
p = p + scale_fill_manual(values=colors) + guides(fill=FALSE)
p = p + scale_y_continuous(limits=c(min(dt$avg_text_standard_score), max(dt$avg_text_standard_score)), oob = rescale_none)
ggsave(filename = sprintf("./%s.png", data_name) , plot=p, width=10, height=7)



# worst / best 
# ---------------
dt$worst_sentiment_headline




# word clouds
if (!require(wordcloud)) {
  install.packages("wordcloud", repos="http://cran.us.r-project.org")
}
if (!require(tm)) {
  install.packages("tm", repos="http://cran.us.r-project.org")
}
if (!require(slam)) {
  install.packages("slam", repos="http://cran.us.r-project.org")
}
if (!require(SnowballC)) {
  install.packages("SnowballC", repos="http://cran.us.r-project.org")
}
if (!require(RSQLite)) {
  install.packages("RSQLite", repos="http://cran.us.r-project.org")
}
library(wordcloud)
library(SnowballC)
library(ggplot2)
library(lubridate)

# library(RSQLite)
# con <- dbConnect(drv=RSQLite::SQLite(), dbname="newsdb_v4.sqlite")
# tables <- dbListTables(con)
# tables <- tables[tables != "sqlite_sequence"]
# 
# nyt = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%www.nytimes.com%\" limit 5000")
# fox = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%www.foxnews.com%\"")
# cnn = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%cnn.com%\"")
# msnbc = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%www.msnbc.com%\"")
# 
# buzzfeed = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%buzzfeednews.com%\"")
# vox = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%vox.com%\"")
# rt = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%rt.com%\"")
# huffpo = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%huffington%\"")
# politico = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%politico%\"")
# dc = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%dailycaller%\"")
# breitbart = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%breitbart%\"")
# infowars = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%infowars%\"")
# guardian = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%guardian%\"")
# 
# wapo = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%washingtonpost.com%\"")
# wsj = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%www.wsj.com%\"")
# npr = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%npr.com%\"")
# bbc = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%bbc%\"")
# usa = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%www.usatoday.com%\"")
# latimes = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%latimes%\"")
# bostonglobe = dbGetQuery(conn=con, statement="SELECT * FROM Headlines where url like \"%bostonglobe%\"")

dt = read.csv("all_headlines_clean.csv")
dt = dt[!duplicated(dt[,c('headline')], fromLast=FALSE),] #fromlast to get highest value in "weeks_on_list" field

nyt = dt[grep("www.nytimes.com", dt$link),]
fox = dt[grep("foxnews.com", dt$link),]
cnn = dt[grep("cnn.com", dt$link),] 
msnbc = dt[grep("msnbc.com", dt$link),]

breitbart = dt[grep("breitbart.com", dt$link),] 
infowars = dt[grep("infowars.com", dt$link),]
dc = dt[grep("dailycaller", dt$link),]

npr = dt[grep("npr.org", dt$link),]
wapo = dt[grep("washingtonpost.com", dt$link),]
wsj = dt[grep("wsj.com", dt$link),]
usa = dt[grep("usatoday.com", dt$link),]
nypost = dt[grep("nypost", dt$link),]

politico = dt[grep("politico", dt$link),]
huffpo = dt[grep("huffingtonpost", dt$link),]
buzzfeed = dt[grep("buzzfeed", dt$link),]
vox = dt[grep("vox.com", dt$link),]

latimes = dt[grep("latimes", dt$link),]
bostonglobe = dt[grep("bostonglobe", dt$link),]
bbc = dt[grep("bbc.co", dt$link),]
guardian = dt[grep("guardian.com", dt$link),]
rt = dt[grep("www.rt.com", dt$link),]

GenerateWordClouds <- function(stories, data_name, color) {
  words = Corpus(VectorSource(stories))
  corpus <- tm_map(words, content_transformer(tolower))
  
  words = tm_map(words, stripWhitespace)
  words = tm_map(words, tolower)
  
  #badwords = c("the", "and", "a")
  #words = tm_map(words, removeWords, badwords)
  #png(sprintf("%s_simple_wordcloud.png", data_name))
  #wordcloud(words, max.words = 120, random.order=FALSE, colors=brewer.pal(nrow(dt_uniq),"Dark2"))
  #dev.off()
  
  complete_stopwords = c(stopwords('english'), "opinion", "new", "york", "times", "cnn", "msnbc", "fox", "news")
  complete_stopwords = c(complete_stopwords, "com", "http", "https", "-", "—", "\"", "will", "”", "says", "page", "found")
  complete_stopwords = c(complete_stopwords, "page", "404", "error", "said", "read", "“", "via", "–", "’s", "‘", "’")
  complete_stopwords = c(complete_stopwords, "video", "report", "error", "said", "read", "via", "wsj:", "|", "x80", "xe2")
  complete_stopwords = c(complete_stopwords, "'re", "npr", "'s", "x99s", "x99", "s", "\\'", "xc3", "x93", "--", "politico")  
  # Generate wordcloud removing all stop words
  #par(mar = rep(0, 4))
  png(sprintf("%s_stopwords_wordcloud.png", data_name), width = 500, height = 500)
  
  words = tm_map(words, removeWords, complete_stopwords)
  set.seed(1)
  #par(mfrow = c(1,2))
  wordcloud(words, max.words = 75, random.order=FALSE, scale=c(8,.3), colors=brewer.pal(8,"Dark2"), rot.per=0.35)
  
  dev.off()
  
  dtm = TermDocumentMatrix(words)
  m = as.matrix(dtm)
  v = sort(rowSums(m),decreasing=TRUE)
  d = data.frame(word = rownames(m), 
                 freq = rowSums(m), 
                 row.names = NULL)
  #d = data.frame(word = names(v),freq=v)
  d = d[order(d$freq, decreasing=TRUE),]
  d$word = factor(d$word, levels = d$word[order(d$freq, decreasing=TRUE)])
  
  top_words = d[1:40,]
  p = ggplot(top_words, aes(x=word, y=freq, fill=data_name)) + geom_bar(stat="identity") 
  p = p + ggtitle(sprintf("%s - Top Words", toupper(data_name)))
  p = p + theme(plot.title = element_text(hjust = 0.5))
  p = p + theme(axis.text.x=element_text(angle=90, hjust=1,face="bold"))
  p = p + theme(axis.text=element_text(size=16,face="bold"), axis.title=element_text(size=13), axis.title.x=element_blank())
  p = p + theme(plot.title = element_text(size=18,face="bold"))
  #p = p + xlab("Word")
  p = p + scale_fill_manual(values = c(color)) + guides(fill=FALSE)
  p = p + ylab("Number of Uses") 
  
  #p = p + scale_y_continuous(limits = c(0, 1200)) + scale_x_continuous(limits = c(0, 1000))
  ggsave(filename = sprintf("./%s_top40.png", data_name) , plot=p, width=8, height=9)
}


GenerateWordClouds(nyt$headline, "nyt", "black")           
GenerateWordClouds(fox$headline, "fox", "red")   
GenerateWordClouds(cnn$headline, "cnn", "orange")  
GenerateWordClouds(msnbc$headline, "msnbc", "blue")

GenerateWordClouds(wapo$headline, "wapo", "black")           
GenerateWordClouds(wsj$headline, "wsj", "red")   
GenerateWordClouds(npr$headline, "npr", "orange")  
GenerateWordClouds(usa$headline, "usa", "blue")
GenerateWordClouds(nypost$headline, "nypost", "blue")

GenerateWordClouds(politico$headline, "politico", "black")           
GenerateWordClouds(huffpo$headline, "huffpo", "red")   
GenerateWordClouds(buzzfeed$headline, "buzzfeed", "orange")  
GenerateWordClouds(vox$headline, "vox", "blue")

GenerateWordClouds(latimes$headline, "latimes", "orange")  
GenerateWordClouds(bostonglobe$headline, "bostonglobe", "blue")

GenerateWordClouds(dc$headline, "dc", "orange")  
GenerateWordClouds(breitbart$headline, "breitbart", "blue")
GenerateWordClouds(infowars$headline, "infowars", "blue")
GenerateWordClouds(rt$headline, "rt", "blue")
# 
