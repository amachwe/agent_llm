from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer, util
import torch

#device = torch.device("cuda")

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-xxl")

voc = tokenizer.get_vocab()

    
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-xxl", trust_remote_code=True)

# # text to compare
# sen1 = "Apples are very cheap."
# sen2 = "Apple iphones are very cheap."
# sen3 = "apples are very cheap."

# # tokenise
# t_sen1 = tokenizer.encode(sen1, return_tensors="pt")
# t_sen2 = tokenizer.encode(sen2, return_tensors="pt")

# rev_vocab = {v:k for k,v in voc.items()}

# # check tokens and compare against vocab
# print(t_sen1)
# for t in t_sen1.tolist()[0]:
#     print(rev_vocab[t], " - ", t)
    
# print(t_sen2)
# for t in t_sen2.tolist()[0]:
#     print(rev_vocab[t], " - ", t)

# #sentence transformer
# stm = SentenceTransformer("all-MiniLM-L6-v2")
# v_sen1 = stm.encode(sen1)
# v_sen2 = stm.encode(sen2)
# v_sen3 = stm.encode(sen3)

# print("s1 - s2", util.cos_sim(v_sen1,v_sen2))
# print("s1 - s3", util.cos_sim(v_sen1,v_sen3))




data = """
(:Person {born: 1964,name: "Keanu Reeves"})	[:ACTED_IN {roles: ["Neo"]}]	(:Movie {tagline: "Welcome to the Real World",title: "The Matrix",released: 1998})
(:Person {born: 1967,name: "Carrie-Anne Moss"})	[:ACTED_IN {roles: ["Trinity"]}]	(:Movie {tagline: "Welcome to the Real World",title: "The Matrix",released: 1998})
(:Person {born: 1961,name: "Laurence Fishburne"})	[:ACTED_IN {roles: ["Morpheus"]}]	(:Movie {tagline: "Welcome to the Real World",title: "The Matrix",released: 1998})
(:Person {born: 1960,name: "Hugo Weaving"})	[:ACTED_IN {roles: ["Agent Smith"]}]	(:Movie {tagline: "Welcome to the Real World",title: "The Matrix",released: 1998})
(:Person {born: 1967,name: "Andy Wachowski"})	[:DIRECTED]	(:Movie {tagline: "Welcome to the Real World",title: "The Matrix",released: 1998})
(:Person {born: 1965,name: "Lana Wachowski"})	[:DIRECTED]	(:Movie {tagline: "Welcome to the Real World",title: "The Matrix",released: 1998})
(:Person {born: 1952,name: "Joel Silver"})	[:PRODUCED]	(:Movie {tagline: "Welcome to the Real World",title: "The Matrix",released: 1998})
(:Person {born: 1978,name: "Emil Eifrem"})	[:ACTED_IN {roles: ["Emil"]}]	(:Movie {tagline: "Welcome to the Real World",title: "The Matrix",released: 1998})
"""
prompt = tokenizer.encode(f"Which actor played Morpheus? Given the RDF data: {data} ", return_tensors="pt")

res = model.generate(prompt, max_length=1000, num_return_sequences=1)
print(tokenizer.decode(res[0], skip_special_tokens=True))


