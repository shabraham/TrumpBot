import n_gram

f = open("../SentimentDataset/Train/pos.txt","r")
text = f.readlines()

model = n_gram.model()
model.train(text)

print "\n\n*****uni_writer*****\n\n"
print model.uni_writer(100)
print "\n\n*****bi_writer*****\n\n"
print model.bi_writer(100)
