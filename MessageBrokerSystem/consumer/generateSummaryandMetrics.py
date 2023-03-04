from rouge import Rouge 
import pprint

import evaluate
from evaluate import load
rouge = evaluate.load('rouge')


from transformers import pipeline
from transformers import BertTokenizer, BertForSequenceClassification

model = BertForSequenceClassification.from_pretrained("Goutham-Vignesh/ContributionSentClassification-scibert")

tokenizer=BertTokenizer.from_pretrained('Goutham-Vignesh/ContributionSentClassification-scibert')
text_classification = pipeline('text-classification', model=model, tokenizer=tokenizer)

def summaryGenerator(sentences):
    generated_summary=""
    for line in sentences:
        prediction = text_classification(line)
        if prediction[0]['label']=="LABEL_1":
            generated_summary=generated_summary+line

    print( "GENERATED SUMMARY ")
    print(generated_summary)
    return generated_summary


def summaryMetrics(summary,abstract):
    results = rouge.compute(predictions=[summary], references=[abstract])
    print(results)
    return results
    
    