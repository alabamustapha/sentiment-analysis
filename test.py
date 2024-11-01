from web_scraper import WebScraper
from text_processor import TextProcessor
from sentiment_analyzer import SentimentAnalyzer
from visualizer import Visualizer
from file_manager import Filemanager

import os
from tabulate import tabulate

webpage_url = 'https://www.africa.engineering.cmu.edu/'

urls = [
    'https://www.africa.engineering.cmu.edu/',
    'https://www.africa.engineering.cmu.edu/about',
    'https://www.africa.engineering.cmu.edu/programs',
    'https://www.africa.engineering.cmu.edu/research',
    'https://www.africa.engineering.cmu.edu/news',
    'https://www.africa.engineering.cmu.edu/events',
]






web_scrapper = WebScraper(webpage_url)
web_scrapper.download_html()

title, paragraphs = web_scrapper.extract_content()

web_scrapper.save_text()

web_scrapper.scrape_multiple_pages(urls, item_name='article')


text_processor = TextProcessor()
paragraphs = text_processor.clean_text(paragraphs)


print("printing first 5 cleaned paragraphs")
print(paragraphs[:5])


sentiment_analyzer = SentimentAnalyzer()

print("testing the analyze_sentiment method")
sentiment_analyzer.analyze_sentiment()


print("testing the count_sentiments method")
counts = sentiment_analyzer.count_sentiments(paragraphs)


print("testing the summarize_sentiment method")
sentiment_analyzer.summarize_sentiment(paragraphs)

print("testing the plot_sentiment method")
visualizer = Visualizer()
visualizer.plot_sentiment(counts)

print("testing mulitple pages scraping")
web_scrapper.scrape_multiple_pages(urls, item_name='page')



# read all the text files in the store folder as a list of strings
folder_path = 'store'
text_files = [file for file in os.listdir(folder_path) if file.endswith('.txt')]

print("Testing the aggregate_texts from TextProcessor class")
text_processor = TextProcessor()
text_processor.aggregate_texts(text_files)




print("Testing the Sentiment Analysis For agregated content")

aggregate_file = Filemanager('aggregated_content.txt')
content = aggregate_file.read_file()

aggregated_sentiment_analyzer = SentimentAnalyzer()
sentiments = aggregated_sentiment_analyzer.sentiment_analysis(content)

print("Overall sentiment polarity of the aggregated content: ", sentiments["polarity"])
print("Overall sentiment subjectivity of the aggregated content: ", sentiments["subjectivity"])


print("Testting top_words method")
aggregate_file = Filemanager('aggregated_content.txt')
content = aggregate_file.read_file()

text_processor = TextProcessor()
top_words = text_processor.find_frequent_words(content, 10)

print("Top 10 words in the aggregated content: ")
print(tabulate(top_words, headers=["Word", "Frequency"], tablefmt="pretty"))


# make word cloud
visualizer = Visualizer()
visualizer.make_word_cloud(content)


dynamic_web_scraper = WebScraper()

# works with chrome driver.
dynamic_web_scraper.scrape_dynamic_content()

# test meta data extraction
dynamic_web_scraper.extract_metadata()


# test keyword search
webscraper = WebScraper()
webscraper.keyword_search('the')




