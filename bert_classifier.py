import pandas as pd

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

unis_ordered = ['Georg-August-Universität Göttingen', 'University of Cambridge', 'Philipps-Universität Marburg', 'University of California, Berkeley', 'Princeton University', 'Eötvös Loránd University', 'University of Szeged', 'École Normale Supérieure', 'California Institute of Technology', 'University of London', 'Université de Paris', 'Lomonosov Moscow State University', 'Harvard University', 'Hebrew University of Jerusalem', 'Universiteit Leiden', 'Københavns Universitet', 'Scuola Normale Superiore di Pisa', 'Cornell University', 'Columbia University', 'Universität Basel', 'Massachusetts Institute of Technology', 'Rijksuniversiteit Groningen', 'New York University', 'Universität Berlin', 'University of Pittsburgh', 'Stockholm University', 'The Johns Hopkins University', 'University of Tokyo', 'University of Oxford', 'Universität Wien', 'University of Illinois at Urbana-Champaign', 'Johann Wolfgang Goethe-Universität Frankfurt am Main', 'University of Edinburgh', 'Universitetet i Oslo', 'Rice University', 'Victoria University of Manchester', 'Yale University', 'University of Texas at Austin', 'Martin-Luther-Universität Halle-Wittenberg', 'St. Petersburg State University', 'Université Paris IV-Sorbonne', 'University of Lwów', 'Uniwersytet Warszawski', 'Università di Roma La Sapienza', 'The University of Chicago', 'Universität Zürich', 'Faculté des Sciences, Paris', 'University of Wisconsin-Madison', 'Ludwig-Maximilians-Universität München', 'Universität Hamburg', 'ETH Zürich', 'Università di Pisa', 'Rheinische Friedrich-Wilhelms-Universität Bonn', 'Università degli Studi di Padova', 'Brown University', 'Ruprecht-Karls-Universität Heidelberg', 'Helsingin yliopisto', 'Friedrich-Alexander-Universität Erlangen-Nürnberg', 'École Normale Supérieure Paris', 'Humboldt-Universität zu Berlin', 'Universität Breslau', 'University of Toronto', 'Universität Leipzig', 'Università di Bologna', 'Westfälische Wilhelms-Universität Münster', 'École Polytechnique', 'Justus-Liebig-Universität Gießen', 'University of Warwick', 'Universität Königsberg', 'Uppsala Universitet', 'University of Pennsylvania', 'Tokyo Imperial University', 'Stanford University', 'University of St. Andrews', 'Universiteit van Amsterdam', 'University of Turin', 'University of Michigan']

MODEL_TO_USE = 'bert_classifier'

tokenizer = AutoTokenizer.from_pretrained(MODEL_TO_USE, local_files_only=True)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_TO_USE, local_files_only=True)

def tokenizer_truncate(input, **kwargs):
    return tokenizer(input, truncation=True, padding=True, **kwargs)

pipe = pipeline(task='text-classification', model=model, tokenizer=tokenizer_truncate)
predictions = pipe(input('Sup? '))

y_pred = []

for i, el in enumerate(predictions):
    y_pred.append(model.config.label2id[el['label']])

y_pred = [unis_ordered[y] for y in y_pred]

print(y_pred)
