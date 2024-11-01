import requests
from bs4 import BeautifulSoup
import nltk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from file_manager import Filemanager
from text_processor import TextProcessor


from nltk.corpus import stopwords
nltk.download('stopwords')  


# 
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
