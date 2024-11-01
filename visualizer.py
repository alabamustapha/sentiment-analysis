import nltk
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud


from nltk.corpus import stopwords
nltk.download('stopwords')  


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


