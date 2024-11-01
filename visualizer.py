import nltk
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud


from nltk.corpus import stopwords
nltk.download('stopwords')  


class Visualizer:

    def plot_sentiment(self, counts):
        """
        Create a bar plot of sentiment analysis results.

        Args:
            counts (dict): Dictionary containing sentiment counts.
        """
        # Capitalize the first letter of each sentiment label
        labels =  [k.capitalize() for k in counts.keys()]
        values = counts.values()
        
        sns.barplot(x=list(labels), y=list(values))
        plt.title('Sentiment Analysis')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        plt.show()

    def make_word_cloud(self, text):
        """
        Generate and display a word cloud from the given text.

        Args:
            text (str): The text to generate the word cloud from.
        """
        # get English stopwords
        stop_words = set(stopwords.words('english'))
        
        # Generate the word cloud
        wordcloud = WordCloud(width = 800, height = 800, stopwords=stop_words, background_color ='white', min_font_size = 10).generate(text) 

        plt.figure(figsize = (8, 8), facecolor = None) 
        plt.imshow(wordcloud) 
        plt.axis("off") 
        plt.tight_layout(pad = 0) 

        plt.show()


