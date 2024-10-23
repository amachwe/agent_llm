from sentence_transformers import SentenceTransformer, util
import pymongo
from matplotlib import pyplot as plt

client = pymongo.MongoClient()
collection = client.get_database("open_ai_test").get_collection("conversations")

data = {}
for conv in collection.find():
    if conv["conv_id"] not in data:
        data[conv["conv_id"]] = {}
    data[conv["conv_id"]][conv["loop"]] = conv["vector"]


for k, v in data.items():
    print(k, len(v))
    line = []
    for i in range(2, len(v)):
        line.append(util.pytorch_cos_sim(v[i], v[i-1])[0][0])

    plt.plot(line, label=k)
    line = []
plt.legend()
plt.show()
