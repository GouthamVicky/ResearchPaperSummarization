from rouge import Rouge 
import pprint
rouge = Rouge()


from transformers import pipeline
from transformers import BertTokenizer, BertForSequenceClassification

model = BertForSequenceClassification.from_pretrained("GouthamVicky/ContributionSentClassification-scibert")

tokenizer=BertTokenizer.from_pretrained('GouthamVicky/ContributionSentClassification-scibert')
text_classification = pipeline('text-classification', model=model, tokenizer=tokenizer)

def summaryGenerator(sentences):
    generated_summary=""
    for line in sentences:
        prediction = text_classification(line)
        if prediction[0]['label']=="LABEL_1":
            generated_summary=generated_summary+line

    print( "GENERATED SUMMARY ")
    print(generated_summary)
    


def summaryMetrics(summary,abstract):
    rouge = Rouge()
    scores = rouge.get_scores(summary, abstract)

    print("Rouge Score for the Generated Summary compared with Abstract of the paper")
    print("\n")
    pprint.pprint(scores)
    
    return scores