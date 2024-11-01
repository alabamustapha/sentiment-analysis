import requests
from bs4 import BeautifulSoup
import re
from textblob import TextBlob
import os
from collections import Counter
import nltk
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from nltk.corpus import stopwords
nltk.download('stopwords')  



class WebScraper:
    def __init__(self, url=None):
        self.__url = url

    @property
    def url(self):
        return self.__url
    
    @url.setter
    def url(self, url):
        self.__url = url
    
    def download_html(self, file_name='webpage.html'):

        file = Filemanager(file_name)

        try:
            print(f"Downloading page content from: {self.url}")
            response = requests.get(self.url)

            if response.status_code != 200:
                print("Unable to download page content")
                return
            
            print(f"Saving page content to: {file_name}")
            file.write_file(response.text)

            print("Download completed successfully")

            
        except Exception as e:
            print("Unable to download page content")
            print(e)

    def extract_content(self, file_name='webpage.html'):

        paragraphs = []
        title = None

        try:
            print(f"Extracting content from: {file_name}")
            file = Filemanager(file_name)
            page_content = file.read_file()

            print(f"Parsing page content")  
            page_soup = BeautifulSoup(page_content, 'html.parser')
            
            print(f"Extracting page title")
            title = page_soup.title.string.strip()
            print(f"Page title extracted: {title}")
            
            print(f"Extracting paragraphs")
            paragraphs = page_soup.find_all('p')

            print("Cleaning extra spaces before and after paragraphs, removing empty paragraphs")
            paragraphs = [p.text.strip() for p in paragraphs if p.text.strip() != '']

            print(f"Paragraphs extracted, total paragraphs: {len(paragraphs)}")
                
        except Exception as e:
            print("Unable to extract content")
            print(e)
        
        return title, paragraphs
    

    def save_text(self, file_name='extracted_content.txt', from_file='webpage.html'):
        
        all_p = ""

        try:
            title, paragraphs = self.extract_content(from_file)
            print(f"Saving extracted content to: {file_name}")

            file = Filemanager(file_name)

            title = title.strip()
            file.write_file(title + '\n\n')

            # clean paragraphs before saving
            paragraphs = TextProcessor().clean_text(paragraphs)

            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                all_p += paragraph + '\n\n'
            
            # save all paragraphs using append mode
            file.write_file(all_p, mode='a')
        
            print("Content saved successfully")
        except Exception as e:
            print("Unable to save extracted content")
            print(e)

    def scrape_multiple_pages(self, urls, item_name='article'):

        for i, url in enumerate(urls):
            page_html = f"{item_name}{i+1}.html"
            file_name = f"{item_name}{i+1}.txt"
            
            self.url = url #update url

            # download page as html
            self.download_html(page_html)

            # extract content from html
            self.save_text(file_name, page_html)

            # delete the html file
            file = Filemanager(page_html)
            file.delete_file()



    def scrape_dynamic_content(self, url="https://www.wikipedia.org/", search_query="Africa", input_el_id="searchInput", file_name="dynamic_content.html"):
        
        
        try:
            # open the browser
            driver = webdriver.Chrome()

            # open the url
            driver.get(url)

            # search for the search box and enter the search query
            if search_query is not None:
                try:
                    # wait until all element loads
                    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, input_el_id)))

                    search_box = driver.find_element(By.ID, input_el_id)
                    search_box.send_keys(search_query)
                    search_box.send_keys(Keys.RETURN)

                    # wait for the page to load
                    driver.implicitly_wait(10)
                except Exception as e:
                    print("Unable to perform search")
                    print(e)

            # get the page content
            page_content = driver.page_source

            # save the page content to a file
            output_file = Filemanager(file_name)
            output_file.write_file(page_content)
            
            # close the browser
            driver.quit()

            return file_name
        
        except Exception as e:
            print("Unable to scrape {url} using search query: {search_query}")
            print(e)
    
    

    def extract_metadata(self, file_name='dynamic_content.html', output_file='metadata.txt'):

        meta_data = {}

        output_file = Filemanager(output_file)

        try:
            print(f"Extracting metadata from: {file_name}")
            file = Filemanager(file_name)
            page_content = file.read_file()

            print(f"Parsing page content")  
            page_soup = BeautifulSoup(page_content, 'html.parser')
            
            meta_tags = page_soup.find_all('meta')

            

            output_file.write_file("Page Metadata\n\n")

            for tag in meta_tags:
                tag_keys = tag.attrs.keys()
                tag_keys = [key for key in tag_keys if key != 'content']
                for key in tag_keys:
                    if key not in meta_data:
                        meta_data[key] = []
                    meta_data[key].append((tag[key], tag.get('content')))

                    
            for key, values in meta_data.items():
                
                output_file.write_file(f"{key.capitalize()}\n", mode='a')
                
                for i, value in enumerate(values):
                    tag_content =  value[1] if value[1] is not None else ""
                    output_file.write_file(f"{i+1}. {value[0]}: {tag_content}\n", mode='a')
                output_file.write_file("\n", mode='a')

            print("Metadata extracted and saved successfully")
                
        except Exception as e:
            print("Unable to extract metadata")
            print(e)

        return None


    def keyword_search(self, keyword="the", file_name='webpage.html'):

        keyword_count = 0

        try:
            print(f"Extracting content from: {file_name}")
            file = Filemanager(file_name)
            page_content = file.read_file()

            text_analysis = TextProcessor()
            clean_page_content = text_analysis.clean_text([page_content])[0]

            keyword_count = clean_page_content.count(keyword.lower())

            print(f"Keyword '{keyword}' count: {keyword_count}")

        except Exception as e:
            print("Unable to extract content")
            print(e)
        
        return keyword_count
   

class TextProcessor:
    
    
    def clean_text(self, paragraphs):
        
        cleaned_paragraphs = []
        
        for paragraph in paragraphs:
            #remove html tags
            paragraph = BeautifulSoup(paragraph, 'html.parser').get_text()
            
            #remove special characters using regex
            paragraph = re.sub(r'[^a-zA-Z0-9\s]', '', paragraph)

            # remove extra spaces
            paragraph = re.sub(r'\s+', ' ', paragraph)
           
            #convert to lowercase
            paragraph = paragraph.lower()
            
            cleaned_paragraphs.append(paragraph)
        
        return cleaned_paragraphs
    
    
    
    def aggregate_texts(self, file_names, output_file='aggregated_content.txt'):  
        
        output_file = Filemanager(output_file)
        
        file_manager = Filemanager()
        aggregated_content = ""

        for file_name in file_names:
            print(f"Reading content from: {file_name}")
            file_manager.file_name = file_name
            content = file_manager.read_file()
            print(f"Content read successfully, content length: {len(content)}")
            aggregated_content += content + '\n\n'

        output_file.write_file(aggregated_content)

        return aggregated_content

    
    def find_frequent_words(self, aggregated_content, top_n=10):
        text_blob = TextBlob(aggregated_content.lower()) 
        stop_words = set(stopwords.words('english'))

        filtered_words = [word for word in text_blob.words if word not in stop_words]  
        
        word_counts = Counter(filtered_words)
        
        top_words = word_counts.most_common(top_n)
        
        return top_words
    

class SentimentAnalyzer:
        
        
        def analyze_sentiment(self, file_name='extracted_content.txt'):
            
            try:

                file = Filemanager(file_name)
                
                paragraphs = file.read_file(lines=True)
                
                paragraphs = [p.strip() for p in paragraphs if p.strip() != '']

                for i, paragraph in enumerate(paragraphs):

                    blob = TextBlob(paragraph)
                    polarity = blob.sentiment.polarity
                    subjectivity = blob.sentiment.subjectivity

                    print(f"Paragraph {i+1}: {paragraph}")
                    print(f"Sentiment Polarity: {polarity}")
                    print(f"Sentiment Subjectivity: {subjectivity}")
                    print()
            except Exception as e:
                print("Unable to analyze sentiment")
                print(e)

        
        def count_sentiments(self, paragraphs = []):
          
            sentiment_counts = {
                'positive': 0,
                'negative': 0,
                'neutral': 0
            }

            try:
                for paragraph in paragraphs:
                    blob = TextBlob(paragraph)
                    if blob.sentiment.polarity > 0:
                        sentiment_counts['positive'] += 1
                    elif blob.sentiment.polarity < 0:
                        sentiment_counts['negative'] += 1
                    else:
                        sentiment_counts['neutral'] += 1
                
                print("Sentiment Counts:")
                print(f"Positive: {sentiment_counts['positive']}")
                print(f"Negative: {sentiment_counts['negative']}")
                print(f"Neutral: {sentiment_counts['neutral']}")
                
            except Exception as e:
                print("Unable to count sentiments")
                print(e)

            return sentiment_counts

        
        def summarize_sentiment(self, paragraphs,file_name = "sentiment_summary.txt"):

            file = Filemanager(file_name)

            file.write_file("Sentiment Summary\n\n")
            file.write_file(f"Total number of paragraphs analyzed: {len(paragraphs)}\n\n", mode='a')
            
            
            sentiment_counter = self.count_sentiments(paragraphs)

            # polarity counts
            file.write_file(f"Positive: {sentiment_counter['positive']}\n\n", mode='a')
            file.write_file(f"Negative: {sentiment_counter['negative']}\n\n", mode='a')
            file.write_file(f"Neutral: {sentiment_counter['neutral']}\n\n", mode='a')

            
            blobs = [TextBlob(paragraph).sentiment for paragraph in paragraphs]

            polarities = [blob.polarity for blob in blobs]
            subjectivities = [blob.subjectivity for blob in blobs]
            
            if len(paragraphs) > 0:
                avg_polarity = sum(polarities)/len(polarities)
                avg_subjectivity = sum(subjectivities)/len(subjectivities)
            else:
                avg_polarity = 0
                avg_subjectivity = 0
            
            
            file.write_file(f"The average polarity: {avg_polarity:.3f}\n\n", mode='a')
            file.write_file(f"The average subjectivity: {avg_subjectivity:.3f}", mode='a')

        def sentiment_analysis(self, content):
            blob = TextBlob(content)

            return {
                "polarity": f"{blob.sentiment.polarity:.3f}", 
                "subjectivity": f"{blob.sentiment.subjectivity:.3f}"
            }
        
class Visualizer:

    def plot_sentiment(self, counts):
        
        labels =  [k.capitalize() for k in counts.keys()]
        values = counts.values()
        
        sns.barplot(x=list(labels), y=list(values))
        plt.title('Sentiment Analysis')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        plt.show()

    def make_word_cloud(self, text):
        
        stop_words = set(stopwords.words('english'))

        wordcloud = WordCloud(width = 800, height = 800, stopwords=stop_words, background_color ='white', min_font_size = 10).generate(text) 

        plt.figure(figsize = (8, 8), facecolor = None) 
        plt.imshow(wordcloud) 
        plt.axis("off") 
        plt.tight_layout(pad = 0) 

        plt.show()


class Filemanager:
    def __init__(self, file_name=None, folder='store'):
        self.__file_name = file_name
        self.__folder = folder

    @property
    def file_name(self):
        return self.__file_name
    
    @file_name.setter
    def file_name(self, file_name):
        self.__file_name = file_name
    
    @property
    def folder(self):
        return self.__folder
    
    @folder.setter
    def folder(self, folder):
        self.__folder = folder

    def read_file(self, lines=False):
        content = None

        try:
            with open(f"{self.folder}/{self.file_name}", 'r', encoding="utf-8") as file:
                if lines:
                    content = file.readlines()
                else:
                    content = file.read()
                
        except Exception as e:
            print("Unable to read file")
            print(e)
        
        return content
    
    def write_file(self, content, mode='w'):
        try:
            with open(f"{self.folder}/{self.file_name}", mode, encoding="utf-8") as file:
                file.write(content)
        except Exception as e:
            print("Unable to write file")
            print(e)

    def delete_file(self):
        try:
            os.remove(f"{self.folder}/{self.file_name}")
        except Exception as e:
            print("Unable to delete file")
            print(e)
        

