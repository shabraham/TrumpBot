import n_gram
import random
import sys

# README:
# To run, navigate to the directory with your src folder and sentimentDataset folder and type
# python src/main.py

#sentiment takes two command line args: positive training data, negative training data
def sentiment():
	
	# readin training data - assuming your in the project directory:
	# function call: python src/main.py pos.txt neg.txt
	# p_f = open("SentimentDataset/Train/" + sys.argv[1],"r")
	# n_f = open("SentimentDataset/Train/" + sys.argv[2],"r")
	tweets = open("tweets9000.csv","r")
	# n_f = open("../SentimentDataset/Train/neg.txt","r")	
	tweet_lines = tweets.readlines()
	# n_text = n_f.readlines()
	
	#initialize models
	model = n_gram.model(tweet_lines)
	#print model.bi_counts
	#print model.uni_counts
	# n_model = n_gram.model(n_text,"neg")
	# n_model = None
	# n_model = n_gram.model(p_text)

	#train models -- converting all strings to lowercase
	#p_model.train(p_text)
	#n_model.train(n_text)
	
	# save the models to a file
	# model.serialize()
	#n_model.serialize()

	#print p_model.bi_writer(5) 
	#print n_model.bi_writer(50)
	'''
	output = ["<s>"]
	for i in xrange(0,20+1):
		output.append(p_model.bi_gen_text(output[i]))

	s = ""
	for i in xrange(1,20+1):
		s += output[i]
		
	print s
	'''
    
	return model

# 1: positive review, 0: negative review
# tup: first value is the positive model, second is the negative model
def generateBot(tup): 
	print "Input a one word topic you want Trump to make a comment about: "
	question = raw_input()
	question = question.strip()
	trump_model = tup

	trumpLst = []
	trumpLst.append(trump_model.bi_writer(28))
	trumpLst.append("****** Generating Seeding Sentences ******")
	trumpLst.append(trump_model.triWriterSeed("crooked hillary",26))
	trumpLst.append(trump_model.triWriterSeed("make america",10))
	trumpLst.append(trump_model.biWriterSeed(question,27))
	# posLst.append("****** Generating Unigram Models ******")
	# posLst.append(pos_model.uni_writer(10))
	# posLst.append(pos_model.uni_writer(50))
	# posLst.append(pos_model.uni_writer(100))

	# negLst = []
	# negLst.append(neg_model.bi_writer(10))
	# negLst.append(neg_model.bi_writer(50))
	# negLst.append(neg_model.bi_writer(100))
	# negLst.append("****** Generating Seeding Sentences ******")
	# negLst.append(neg_model.biWriterSeed("Once upon a",1))
	# negLst.append(neg_model.biWriterSeed("I really",10))
	# negLst.append("****** Generating Unigram Models ******")
	# negLst.append(neg_model.uni_writer(10))
	# negLst.append(neg_model.uni_writer(50))
	# negLst.append(neg_model.uni_writer(100))

	with open("trumpGenBiText.txt","wb") as f: 
		for ele in trumpLst:
			f.write(ele +"\n")

	# with open("negGenBiText.txt","wb") as f: 
	# 	for ele in negLst:
	# 		f.write(ele +"\n")

def main():
	tup = sentiment()
	generateBot(tup)
	#uni_s = uni_writer()
	#print "____________uniWriter____________"
	#print uni_s
	#bi_s = bi_writer()
	#print "____________biWriter____________"
	#print bi_s
    

main()
print "nigga we made it"

