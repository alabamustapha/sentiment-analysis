from sentiment import SentimentAnalyzer, TextProcessor, WebScraper, Visualizer, Filemanager
# list of african countries 
africa_countries = ["Nigeria", "Rwanda", "Congo", "South Africa", "Kenya", "Ghana", "Tanzania", "Uganda", "Zambia", "Zimbabwe", "Mali", "Morocco", "Algeria", "Tunisia", "Egypt", "Libya", "Sudan", "South Sudan", "Somalia", "Ethiopia", "Eritrea", "Djibouti", "Chad", "Cameroon", "Central African Republic", "Gabon", "Equatorial Guinea", "Cape Verde", "Sao Tome and Principe", "Gambia", "Senegal", "Guinea-Bissau", "Guinea", "Sierra Leone", "Liberia", "Ivory Coast", "Burkina Faso", "Togo", "Benin", "Niger", "Mauritania", "Western Sahara", "Mauritius", "Comoros", "Seychelles", "Madagascar", "Mozambique", "Malawi", "Zambia", "Angola", "Namibia", "Botswana", "Lesotho", "Swaziland", "Burundi", "Uganda", "Rwanda", "Burundi", "Tanzania", "Kenya", "Somalia", "Djibouti", "Eritrea", "Ethiopia", "Sudan", "South Sudan", "Uganda", "Rwanda", "Burundi", "Tanzania", "Kenya", "Somalia", "Djibouti", "Eritrea", "Ethiopia", "Sudan", "South Sudan", "Uganda", "Rwanda", "Burundi", "Tanzania", "Kenya", "Somalia", "Djibouti", "Eritrea", "Ethiopia", "Sudan", "South Sudan", "Uganda", "Rwanda", "Burundi", "Tanzania", "Kenya", "Somalia", "Djibouti", "Eritrea", "Ethiopia", "Sudan", "South Sudan", "Uganda", "Rwanda", "Burundi", "Tanzania", "Kenya", "Somalia", "Djibouti", "Eritrea"]


# scrape the wiki content for each country to a file 
scraper = WebScraper()
file = Filemanager()
text_processor = TextProcessor()
sentiment_analyzer = SentimentAnalyzer()
country_sentiment_summary = []


# for country in africa_countries[:5]:
#     country_file_name = f"countries/{country}.html"
#     scraper.scrape_dynamic_content(url="https://www.wikipedia.org/", search_query=f"{country}", input_el_id="searchInput", file_name=country_file_name)
    
    
    
for country in africa_countries[:5]:
    country_file_name = f"countries/{country}.html"
    country_summary_txt = f"countries/{country}_summary.txt"
    title, paragraphs = scraper.extract_content(file_name=country_file_name)
    paragraphs = text_processor.clean_text(paragraphs)
    sentiment_analyzer.summarize_sentiment(paragraphs, country_summary_txt)
    # for each country get summary of sentiment and put in a dictionary
    country_content = '\n'.join(paragraphs)
    sentiments = sentiment_analyzer.sentiment_analysis(country_content)
    frequent_word = text_processor.find_frequent_words(country_content, 10)
    
    words = [word[0] for word in frequent_word]
    frequent_word_count = [str(word[1]) for word in frequent_word]
    # print(word_count)
    words_new = ','.join(words)
    frequent_word_count_new = ','.join(frequent_word_count)
    word_count = len(country_content.split(' '))
    # print(f"word_count : {word_count}")
    
    word_search_list = ["war","poverty","corruption","insecurity","crime", "art", "tourism"]
    search_counts = []
    for search in word_search_list:
        search_count = scraper.keyword_search(search,file_name=country_file_name)
        search_counts.append(search_count)
    
    print(list(zip(word_search_list, search_counts)))
    country_sentiment_summary.append([country, len(paragraphs), words_new, frequent_word_count_new, word_count, sentiments["polarity"], sentiments["subjectivity"]])
    
    
    
    
print (country_sentiment_summary)
    


# plot the polarity bargraph for each country

# plot the subjectivity bargraph for each country

# plot polarity against subjectivity for each country


# search for key words - war, poverty, corruption, insecurity, crime


