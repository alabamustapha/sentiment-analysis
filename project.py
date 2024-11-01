from sentiment import SentimentAnalyzer, TextProcessor, WebScraper, Visualizer, Filemanager
# list of african countries 
africa_countries = ["Nigeria", "Rwanda", "Congo", "South Africa", "Kenya", "Ghana", "Tanzania", "Uganda", "Zambia", "Zimbabwe", "Mali", "Morocco", "Algeria", "Tunisia", "Egypt", "Libya", "Sudan", "South Sudan", "Somalia", "Ethiopia", "Eritrea", "Djibouti", "Chad", "Cameroon", "Central African Republic", "Gabon", "Equatorial Guinea", "Cape Verde", "Sao Tome and Principe", "Gambia", "Senegal", "Guinea-Bissau", "Guinea", "Sierra Leone", "Liberia", "Ivory Coast", "Burkina Faso", "Togo", "Benin", "Niger", "Mauritania", "Western Sahara", "Mauritius", "Comoros", "Seychelles", "Madagascar", "Mozambique", "Malawi", "Zambia", "Angola", "Namibia", "Botswana", "Lesotho", "Swaziland", "Burundi", "Uganda", "Rwanda", "Burundi", "Tanzania", "Kenya", "Somalia", "Djibouti", "Eritrea", "Ethiopia", "Sudan", "South Sudan", "Uganda", "Rwanda", "Burundi", "Tanzania", "Kenya", "Somalia", "Djibouti", "Eritrea", "Ethiopia", "Sudan", "South Sudan", "Uganda", "Rwanda", "Burundi", "Tanzania", "Kenya", "Somalia", "Djibouti", "Eritrea", "Ethiopia", "Sudan", "South Sudan", "Uganda", "Rwanda", "Burundi", "Tanzania", "Kenya", "Somalia", "Djibouti", "Eritrea", "Ethiopia", "Sudan", "South Sudan", "Uganda", "Rwanda", "Burundi", "Tanzania", "Kenya", "Somalia", "Djibouti", "Eritrea"]


# scrape the wiki content for each country to a file 
scraper = WebScraper()
file = Filemanager()
text_processor = TextProcessor()
sentiment_analyzer = SentimentAnalyzer()

# make a directory to store the files

for country in africa_countries[:5]:
    scraper.scrape_dynamic_content(url="https://www.wikipedia.org/", search_query=f"{country}", input_el_id="searchInput", file_name=f"countries/{country}.html")
    sentiment_analyzer.summarize_sentiment(file_name=f"countries/{country}.html", output_file=f"countries/{country}_summary.txt")
# for each country get sumary of sentiment and put in a dictionary


# plot the polarity bargraph for each country

# plot the subjectivity bargraph for each country

# plot polarity against subjectivity for each country

# get frequency of words in the summary of each country

# get the most common words accross all countries

# search for key words - war, poverty, corruption, insecurity, crime