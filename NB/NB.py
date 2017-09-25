import os
import collections
import re

stopword = [
	'of',
	'a','an',
	'for',
	'by',
	'with',
	'and',
	'in','out',
	'the',
	'as',
	'about',
	'to',
	'up',
	'on','at',
]

def evaluation(TP, FP, TN, FN):
	print('-----------------------------------------------------')
	print('True Positive: '+str(TP)+'\tFalse Positive: '+str(FP))
	print('True Negative: '+str(TN)+'\tFalse Negative: '+str(FN))
	print()
	if (FP+TN) != 0:
		FPR = FP/(FP+TN)
		print('False Positive Rate: '+str(round(FPR, 4)))
	else:
		print("The Division of False Positive Rate is zero!!")

	if (FN+TP) != 0:
		FNR = FN/(FN+TP)
		print('False Negative Rate: '+str(round(FNR, 4)))
	else:
		print("The Division of Talse Negative Rate is zero!!")

	if (TP+FN) != 0:
		RC = TP/(TP+FN)
		print('Recall: '+str(round(RC, 4)))
	else:
		print('Recall: The Division of Recall is zero!!')
		RC = 0

	if (TP+FP) != 0:
		PC = TP/(TP+FP)
		print('Precision: '+str(round(PC, 4)))
	else:
		print('Precision: The Division of Precision is zero!!')
		PC = 0

	if (PC+RC) != 0:
		FS = 2*PC*RC/(PC+RC)
		print('F-Score: '+str(round(FS, 4)))
	else:
		print('F-Score: The Divisioni of F-Score is zero!!')
	print('-----------------------------------------------------')


def classify(path, PrWS, PrWH, SpmLst, PS):
	filenames = os.listdir(path)
	TP, FP, TN, FN = 0, 0, 0, 0
	for file in filenames:
		PSpam, PHam = 1, 1
		with open(path+'/'+file, "r", encoding='utf-8', errors='ignore') as f:
			lines = f.readlines()
			bagofwords = [ collections.Counter(re.findall(r'[a-zA-Z_]+', txt)) for txt in lines]
			dic = dict(sum(bagofwords, collections.Counter()))
			for word in dic:
				if word in stopword:
					continue
				if word not in PrWS:
					continue
				PSpam *= PrWS[word]
				PHam *= PrWH[word]
			PSpam *= PS
			PHam *= (1-PS)
			if PSpam>PHam:
				if file in SpmLst:
					TP += 1
				else:
					FP += 1
			else:
				if file in SpmLst:
					FN += 1
				else:
					TN += 1
	evaluation(TP, FP, TN, FN)

#return a dictionary of (word: spamrate)
def getWordSpamRate(path, trainSpmLst, numtrainSpm, numtrainHam):
	TrainSetFileNames = os.listdir(path)
	spamDic={}	#Each word appears in how many spam files
	totalDic={}	#Each word appears in how many files
	i=0
	################### Calculate spamDic & totalDic #################
	for file in TrainSetFileNames:
		dic = {}
		with open(path+'/'+file, "r", encoding='utf-8', errors='ignore') as f:
			lines = f.readlines()
			bagofwords = [ collections.Counter(re.findall(r'[a-zA-Z_]+', txt)) for txt in lines]
			dic = dict(sum(bagofwords, collections.Counter()))
			# print(dic)

			if file in trainSpmLst:	spm = 1
			else:	spm = 0
			for word in dic:
				if word in totalDic:
					totalDic[word] += 1
				else:
					totalDic[word] = 1
				if spm:
					if word in spamDic:
						spamDic[word] += 1
					else:
						spamDic[word] = 1
		f.closed
		i += 1
		
		# if i == 4: break
	
	############ Calculate each word's pr(W|S) & pr(W|H) #############
	PrWS={}
	PrWH={}
	p = len(totalDic)
	mspam, mham = 0, 0
	for word in totalDic:
		if (word in spamDic) and (totalDic[word] != spamDic[word]):
			#Word in both spam and ham
			PrWS[word] = round(spamDic[word]/numtrainSpm, 4)
			PrWH[word] = round((totalDic[word]-spamDic[word])/numtrainHam, 4)
		elif (word in spamDic) and (totalDic[word] == spamDic[word]):
			#All in spam, m estimate for ham
			PrWS[word] = round(spamDic[word]/numtrainSpm, 4)
			PrWH[word] = round((1/2)/(numtrainHam+1), 4)
		else:
			#All in ham, m estimate for spam
			PrWS[word] = round((1/2)/(numtrainSpm+1), 4)
			PrWH[word] = round(totalDic[word]/numtrainHam, 4)
	##################################################################

	############# write it to a file so it will be faster ############
	with open('wordSpamHamRate.txt', 'w') as f:
		for word in totalDic:
			f.write(str(PrWS[word])+"\t"+str(PrWH[word])+"\t"+word+"\n")
	f.closed
	##################################################################

	return PrWS, PrWH

def main():
	path = '../ML_SpamSets/'
	trainFolder = 'Tr'
	testFolder = 'Te'
	TrainSetFileNames = os.listdir(path + trainFolder)
	TestSetFileNames = os.listdir(path + testFolder)
	################## Build Spm Lst for Train&Test ##################
	trainSpmLst, numtrainSpm = [], 0
	testSpmLst, numtestSpm = [], 0
	with open("../ML_SpamSets/SPAM.label") as f:
		lines = f.readlines()
		for line in lines:
			items = line.split()
			if items[0] is '0':
				if items[1].find('TRAIN', 0) != -1:
					trainSpmLst.append(items[1])
					numtrainSpm += 1
				elif items[1].find('TEST', 0) != -1:
					testSpmLst.append(items[1])
					numtestSpm += 1
	f.closed
	##################################################################

	########## Return two dictionary of (word: spamrate) #############
	# PrWS, PrWH = getWordSpamRate(path+trainFolder, trainSpmLst, numtrainSpm, (len(TrainSetFileNames)-numtrainSpm))
	
	PrWS, PrWH = {}, {}
	with open("wordSpamHamRate.txt") as f:
		lines = f.readlines()
		for line in lines:
			items = line.split()
			PrWS[items[2]] = float(items[0])
			PrWH[items[2]] = float(items[1])
	f.closed
	##################################################################
	print("Classify Training Set")
	classify(path+trainFolder, PrWS, PrWH, trainSpmLst, (numtrainSpm/len(TrainSetFileNames)))
	print("Classify Testing Set")
	classify(path+testFolder, PrWS, PrWH, testSpmLst, (numtestSpm/len(TestSetFileNames)))
	print("########################## ALL DONE ##########################")
main()










