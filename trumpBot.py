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
	p_f = open("../../tweets.csv","r")
	# n_f = open("../SentimentDataset/Train/neg.txt","r")	
	p_text = p_f.readlines()
	# n_text = n_f.readlines()
	
	#initialize models
	p_model = n_gram.model(p_text,"pos")
	# n_model = n_gram.model(n_text,"neg")
	# n_model = None
	# n_model = n_gram.model(p_text)

	#train models -- converting all strings to lowercase
	#p_model.train(p_text)
	#n_model.train(n_text)
	
	# save the models to a file
	p_model.serialize()
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
    
	return p_model

# 1: positive review, 0: negative review
# tup: first value is the positive model, second is the negative model
def generateReviews(tup): 
	pos_model = tup
	#neg_model = tup[1]

	posLst = []
	posLst.append(pos_model.bi_writer(10))
	posLst.append(pos_model.bi_writer(50))
	posLst.append(pos_model.bi_writer(100))
	posLst.append("****** Generating Seeding Sentences ******")
	posLst.append(pos_model.biWriterSeed("Mexicans",1))
	posLst.append(pos_model.biWriterSeed("I really",10))
	posLst.append("****** Generating Unigram Models ******")
	posLst.append(pos_model.uni_writer(10))
	posLst.append(pos_model.uni_writer(50))
	posLst.append(pos_model.uni_writer(100))

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

	with open("posGenBiText.txt","wb") as f: 
		for ele in posLst:
			f.write(ele +"\n")

	with open("negGenBiText.txt","wb") as f: 
		for ele in negLst:
			f.write(ele +"\n")

def main():
	tup = sentiment()
	generateReviews(tup)
	#uni_s = uni_writer()
	#print "____________uniWriter____________"
	#print uni_s
	#bi_s = bi_writer()
	#print "____________biWriter____________"
	#print bi_s
    

main()
print "nigga we made it"

