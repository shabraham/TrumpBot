import numpy as np
import math


class model(object):
	
	def __init__(self,text,identifier): 
		self.bi_counts = {'<s>':{},'<\s>':{}}
		self.uni_counts = {}
		self.tokens_with = 0 #including the start and end tokens added to each example
		self.tokens_without = 0 #not counting the start and end tokens
		self.num_examples = 0
		self.text = text
		self.k = None
		self.id = identifier

		#self.parseTraining()
		print "parsing the training"

		typeLst = self.typeLstGen(self.text)
		print "generated typeLst..."

		# generate the uni_counts map... This is equivalent to a token list
		for typ in typeLst:
			if typ != "<\s>" and typ != "<s>":
				self.uni_counts[typ] = 0
		self.uni_counts["UNK"] = 0  # account for unknown words...
		print "generated uni_counts map"
		
		# now uni+counts is equivalent to a token list: (key,value) = (word,count)
		self.trainUni()
		print "successfully trained uni_counts"

		# now typeLst is equal to the modified typeLst after deleting 1 count words from our unigram model
		typeSet = set(self.uni_counts.keys())
		typeSet.add("<s>")
		typeSet.add("<\s>")

		# train the bigram model with respect to the words we set as unknown
		self.trainBi()		
		print "successfully trained bi_counts map"

		#self.bi_perplexity(text,0.05)
		#smoothing
		self.k_smooth()
		print "smoothed ;)"

	def k_smooth(self): 
		lst = np.linspace(0.01,1,100,endpoint=False)
		min_val = 5000000
		selected_k = 5000000
		heldOut_file = open(self.id + "heldOut.txt","r")
		heldOut = heldOut_file.readlines()
		heldOut_file.close()
		for i in lst:
			perplexVal = int(self.bi_perplexity(heldOut, i))
			print "here is your i " + str(i)
			print "here is your perplexVal " + str(perplexVal)
			if perplexVal < min_val:
				min_val = perplexVal
				selected_k = i

		print "here is your selected k for smoothing " + str(selected_k)
		self.k = selected_k
		return selected_k

	 
	 # select 10% of the training data for the "held out set" and 90% of the training data for the "training set"
	def parseTraining(self): 
	 	count = 0
	 	heldOut = []
	 	trainingSet = []
		for line in self.text:
			heldOut.append(line)
			trainingSet.append(line)
			count += 1
		
		with open(self.id + "heldOut.txt","wb") as f: 
			for key in heldOut:
				f.write(key)

		with open(self.id + "trainingSet.txt","wb") as f: 
			for key in trainingSet:
				f.write(key)


	#probability without smoothing --- funky 
	def prob(self,prev_word,word):
		#catch unknown words
		if not self.bi_counts.has_key(prev_word):
			return 0
		if not self.bi_counts.get(prev_word).has_key(word):
			word = 'UNK'

		if prev_word == "<s>" or prev_word == "<\s>":
			divisor = self.num_examples
		else:
			divisor = self.uni_counts[prev_word]

		if not self.bi_counts[prev_word].has_key(word):
			return 0
		return self.bi_counts[prev_word][word]/float(divisor)

	#probability with smoothing
	def prob_add_k(self,prev_word,word,K=None):
		#catch non-smoothed error
		if K == None:
			if self.k == None:
				print "k not known - please smooth model or pass in k value"
				return
			else:
				K = self.k

		#Voacb Size
		V = len(self.uni_counts) + 2

        #catch unknown words
		if not self.bi_counts.has_key(prev_word):
			return (K / (V*K))
		if not self.bi_counts.get(prev_word).has_key(word):
			word = 'UNK'

		if prev_word == "<s>" or prev_word == "<\s>":
			divisor = self.num_examples + (K*V)
		else:
			divisor = self.uni_counts[prev_word] + (K*V)

		return (self.bi_counts[prev_word][word] + K)/float(divisor)


	def bi_gen_text(self,prev_word):
		next_words = self.bi_counts[prev_word]
		items = []
		prob_dist = []

		if prev_word == "<\s>":
			return "<s>"
		if prev_word == "<s>":
			divisor = self.num_examples
		else:
			divisor = self.uni_counts[prev_word]
		
		for word in next_words:
			items.append(word)
			prob_dist.append(next_words[word]/float(divisor))
		return np.random.choice(items,p=prob_dist)

	def uni_gen_text(self):
		items = []
		prob_dist = []
		for word in self.uni_counts:
			items.append(word)
			prob_dist.append(self.uni_counts[word]/float(self.tokens_without))
		return np.random.choice(items,p=prob_dist)		

	def bi_writer(self,k):
		buff = []
		prev = "<s>"
		while len(buff) < k:
			buff.append(self.bi_gen_text(prev))
			prev = buff[-1]
			if buff[-1] == "<s>" or buff[-1] == "<\s>":
				buff.pop()
		
		s = ""
		for i in xrange(0,k):
			if i == k-1:
				s += buff[i] + "\n"
			else:
				s += buff[i] + " "
		return s		

	def uni_writer(self,k):
		buff = []
		while len(buff) < k:
			buff.append(self.uni_gen_text()) 
		
		s = ""
		for i in xrange(0,k):
			if i == k-1:
				s += buff[i] + "\n"
			else:
				s += buff[i] + " "
		return s

	# Generate a cohesive sentence of length k + length of prevSentence
	def biWriterSeed(self,prevSentence,k):
		buff = []
		prev = (prevSentence.strip().split(" "))[-1]
		while len(buff) < k:
			buff.append(self.bi_gen_text(prev))
			prev = buff[-1]
			while buff[-1] == "<s>" or buff[-1] == "<\s>":
				buff.pop()
		s = ""
		for i in xrange(0,k):
			if i == k-1:
				s += buff[i] + "\n"
			else:
				s += buff[i] + " "
		return prevSentence + " " + s	

	def clear(self):
		self.bi_counts = {'<s>':{},'<\s>':{}}
		self.uni_counts = {}
		self.tokens_with = 0
		self.tokens_without = 0
		self.num_examples = 0

	def print_models(self):
		print "\n\n*****uni_counts*****\n\n"
		for word in self.uni_counts:
			print "word ",word," counts ",self.uni_counts[word],"\n"
		print "\n\n*****bi_counts*****\n\n"
		for word in self.bi_counts:
			print "word ",word," word-counts ",self.bi_counts[word],"\n" 
		print "\ntokens with ",self.tokens_with," tokens without ",self.tokens_without,"\n"
		print "number of training examples ",self.num_examples,"\n"

	# save language models to a text file
	def serialize(self): 
		with open("unigram.txt","wb") as f: 
			for key in self.uni_counts:
				f.write(str(key) +" " + str(self.uni_counts[key]) + "\n")

		with open("bigram.txt","wb") as f: 
			for key in self.bi_counts:
				f.write(str(key) +" " + str(self.bi_counts[key]) + "\n")


	def typeLstGen(self,text): 
		# generate a token list
		typeLst = []
		wordSet = set()
		for line in text: 
			line = "<s> " + line[:-1] + " <\s>"
			words = line.lower().split(" ")
			for word in words: 
				if word not in wordSet:
					typeLst.append(word)
					wordSet.add(word)
		return typeLst

	def trainUni(self): 
		for line in self.text:
			if line[-1:] == "\n":
				line = "<s> " + line[:-1] + " <\s>"

			words = line.lower().split(" ")
			for i in xrange(1,len(words)):
				if words[i] != "<\s>":
					self.uni_counts[words[i]] = self.uni_counts[words[i]] + 1
			
			self.num_examples += 1
			self.tokens_with += len(words)
			self.tokens_without += (len(words)-2)

		# now do option 2 for handling unknown words: transform all count(1) tokens into unknowns
		# we then delete words with count 1 since we're assuming they're unknowns
		for word in self.uni_counts:
			self.uni_counts[word] -= 0.10
			self.uni_counts["UNK"] += 0.10

	def trainBi(self):
		for line in self.text:
			if line[-1:] == "\n":
				line = "<s> " + line[:-1] + " <\s>"
			words = line.lower().split(" ")

			for i in xrange(1,len(words)):
				if not self.bi_counts.has_key(words[i-1]):
					self.bi_counts[words[i-1]] = {}
				
				if self.bi_counts.get(words[i-1]).has_key(words[i]):
					self.bi_counts.get(words[i-1])[words[i]] += 1
				else:
					self.bi_counts.get(words[i-1])[words[i]] = 1

		# adding unk to our dict with an empty val
		self.bi_counts["UNK"] = {}
		# now add 0.1 (or however much we shave off) to each bigram entry that isn't unk
		for key in self.bi_counts:
			if key != "UNK":
				self.bi_counts.get(key)["UNK"] = 0.1

	def uni_perplexity(self, text):
		for line in text:
			if line[-1:] == "\n":
				line = line[:-1]

			words = line.lower().split(" ")
			prob_sum = 0.0
			count = 0
			for i in xrange(1,len(words)):
				if self.uni_counts.has_key(words[i]):
					prob_sum += -1.0 * math.log(self.uni_counts[words[i]]/self.tokens_without, 2)
				else:
					prob_sum += -1.0 * math.log(self.uni_counts["UNK"]/self.tokens_without, 2)
				count += 1

		inner_val = (1.0/count) * prob_sum
		return math.exp(inner_val)

	def bi_perplexity(self, text, k):
		count = 0
		hi = 0
		prob_sum = 0

		for line in text:
			if line[-1:] == "\n":
				line = "<s> " + line[:-1] + " <\s>"
			
			words = line.lower().split(" ")
			for i in xrange(1,len(words)):
				print "HERE IS YOUR WORD " + words[i]
				print "here is self.prob " + str(self.prob_add_k(words[i-1],words[i],k))
				prob_sum += (int) (1000 * math.log(1/self.prob_add_k(words[i-1],words[i],k)))
				#print "here is your prob sum " + str(prob_sum)
				count += 1

		float_prob_sum = float(prob_sum)/1000
		inner_val = (1.0/count) * float_prob_sum
		return math.exp(inner_val)
