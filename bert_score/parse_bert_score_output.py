import re
print("Bert-P,", "Bert-R,", "Bert-F1")
for i in range(1,6):
    with open("./bert_score/" + str(i)) as f:
        line = f.readline()
        line = line.replace("\n", "")
        bert_scores = " ".join(line.split(" ")[1:])

        bert_scores = re.split("[: ]", bert_scores)
        bert_scores = list(filter(lambda x:len(x)!=0, bert_scores))

        scores = bert_scores[1::2]
        print(",".join(scores))
