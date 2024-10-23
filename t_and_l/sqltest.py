from transformers import TapexTokenizer, BartForConditionalGeneration
import pandas as pd

tk = TapexTokenizer.from_pretrained("microsoft/tapex-large-finetuned-wtq")
model = BartForConditionalGeneration.from_pretrained("microsoft/tapex-large-finetuned-wtq")

data = {
    "year": [1896, 1900, 1904, 2004, 2008, 2012, 2023],
    "city": ["athens", "paris", "st. louis", "athens", "beijing", "london", "paris"]
}
table = pd.DataFrame.from_dict(data)

# tapex accepts uncased input since it is pre-trained on the uncased corpus
query = "how many times did paris host the Olympic Games?"
encoding = tk(table=table, query=query, return_tensors="pt")

outputs = model.generate(**encoding)

print(tk.batch_decode(outputs, skip_special_tokens=True))
