from bs4 import BeautifulSoup
import re
from textblob import TextBlob
from collections import Counter
import nltk
from file_manager import Filemanager


from nltk.corpus import stopwords
nltk.download('stopwords')  


class TextProcessor:
    
    
    def clean_text(self, paragraphs):
        """
        Clean and preprocess a list of paragraphs.
        
        Args:
            paragraphs (list): List of text paragraphs to clean.
        
        Returns:
            list: Cleaned paragraphs.
        """
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
        """
        Aggregate content from multiple files into a single file.
        
        Args:
            file_names (list): List of file names to aggregate.
            output_file (str): Name of the output file.
        
        Returns:
            str: Aggregated content.
        """
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
        """
        Find the most frequent words in the aggregated content.
        
        Args:
            aggregated_content (str): The text content to analyze.
            top_n (int): Number of top frequent words to return.
        
        Returns:
            list: Top N most frequent words and their counts.
        """
        text_blob = TextBlob(aggregated_content.lower()) 
        stop_words = set(stopwords.words('english'))
        
        # Filter out stopwords
        filtered_words = [word for word in text_blob.words if word not in stop_words]  
        
        word_counts = Counter(filtered_words)
        
        top_words = word_counts.most_common(top_n)
        
        return top_words
    
