from sentiment_analyzer import SentimentAnalyzer
from file_manager import Filemanager
from text_processor import TextProcessor
from web_scraper import WebScraper
import pandas as pd

# list of african countries 
africa_countries = [
    "Angola", "Benin", "Botswana", "Burkina Faso", 
    "Burundi", "Cameroon", "Cape Verde", 
    "Central African Republic", "Chad", "Comoros", 
    "Congo (Brazzaville)", "Congo (Kinshasa)", 
    "Côte d'Ivoire", "Djibouti", "Egypt", 
    "Equatorial Guinea", "Eritrea", 
    "Eswatini (formerly Swaziland)", "Ethiopia", 
    "Gabon", "Gambia", "Ghana", "Guinea", 
    "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", 
    "Libya", "Madagascar", "Malawi", "Mali", 
    "Mauritania", "Mauritius", "Morocco", "Mozambique", 
    "Namibia", "Niger", "Nigeria", "Rwanda", 
    "São Tomé and Principe", "Senegal", "Seychelles", 
    "Sierra Leone", "Somalia", "South Africa", 
    "South Sudan", "Sudan", "Tanzania", 
    "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"
    ]


scraper = WebScraper() #scraper object

file = Filemanager() #file object

text_processor = TextProcessor() #text_processor object

sentiment_analyzer = SentimentAnalyzer() #sentiment_analyzer object


# scrape content for each country into individual html files
for country in africa_countries:
    
    country_file_name = f"countries/{country}.html"
    scraper.scrape_dynamic_content(url="https://www.wikipedia.org/", search_query=f"{country}", input_el_id="searchInput", file_name=country_file_name)   
    


# create a data store for exracted content
country_data = []

# infomation keys
country_info_keys = ["Country", "Number of Paragraphs", "Frequent Words", "Frequent Word Count", "Word Count", "Polarity", "Subjectivity"]

# list of interesting words to search for in the country content
word_search_list = ["war","poverty","corruption","insecurity","crime", "art", "tourism"]


# extract content from each country file and add it to the data store
for country in africa_countries:

    country_file_name = f"countries/{country}.html" #country html file

    country_summary_txt = f"countries/{country}_summary.txt" #country summary text file
    
    # extract content from the country html file
    title, paragraphs = scraper.extract_content(file_name=country_file_name)

    # clean the extracted content paragraphs
    paragraphs = text_processor.clean_text(paragraphs)

    # summarize the cleaned content and save to a text file
    sentiment_analyzer.summarize_sentiment(paragraphs, country_summary_txt)

    
    # join the paragraphs to form a single string of cleaned content
    country_content = '\n'.join(paragraphs)

    # get sentiment analysis of the country content
    sentiments = sentiment_analyzer.sentiment_analysis(country_content)

    # get the top 10 frequent words and counts in the country content
    frequent_word = text_processor.find_frequent_words(country_content, 10)
    
    # extract the top 10 frequent words
    words = [word[0] for word in frequent_word]

    # extract the top 10 frequent word counts
    frequent_word_count = [str(word[1]) for word in frequent_word]


    # concatenate the frequent words and counts into a single string
    country_frequent_word = ','.join(words)
    country_frequent_word_count = ','.join(frequent_word_count)
    
    # get the word count of the country content
    country_word_count = len(country_content.split(' '))
    
    
    #country information
    country_info = [country, len(paragraphs), country_frequent_word, country_frequent_word_count, country_word_count, sentiments["polarity"], sentiments["subjectivity"]]
    

    search_counts = []
    
    for search in word_search_list:
        search_count = scraper.keyword_search(search,file_name=country_file_name)
        search_counts.append(search_count)
    
    total_country_info = country_info + search_counts
    country_data.append(total_country_info)
    

# saving all data to a csv file
pd.DataFrame(country_data, columns=country_info_keys + word_search_list).to_csv("countries.csv", index=False)
    


