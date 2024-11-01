from textblob import TextBlob
from file_manager import Filemanager


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
            


        
