import os
import sys
import collections
import re
import math

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
		print('F-Score: The Division of F-Score is zero!!')
	print('-----------------------------------------------------')

def classify(path, PrWS, PrWH, SpmLst, PS):
	filenames = os.listdir(path)
	TP, FP, TN, FN = 0, 0, 0, 0
	ClassifiedList=[]
	for file in filenames:
		PSpam, PHam = 0, 0
		with open(path+'/'+file, "r", encoding='utf-8', errors='ignore') as f:
			lines = f.readlines()
			bagofwords = [ collections.Counter(re.findall(r'[a-zA-Z_]+', txt)) for txt in lines]
			dic = dict(sum(bagofwords, collections.Counter()))
			for word in dic:
				if word in stopword:
					continue
				if word not in PrWS:
					continue
				PSpam += math.log(PrWS[word])
				PHam += math.log(PrWH[word])
			PSpam += math.log(PS)
			PHam += math.log((1-PS))
			if PSpam>PHam:
				ClassifiedList.append(0)
				if file in SpmLst:
					TP += 1
				else:
					FP += 1
			else:
				ClassifiedList.append(1)
				if file in SpmLst:
					FN += 1
				else:
					TN += 1
		f.closed
	dstdir = input("Enter a file to save the result\n or enter '0' for not saving into a file: ")
	if dstdir != '0':
		i=0
		with open(dstdir, 'w+') as f:
			for file in filenames:
				f.write(str(ClassifiedList[i])+' '+file+'\n')
				i += 1
	eva = input("Do you want to evaluate the performance?\n Only if the emails are in SPAM.label\n '1' for yes or '0' for no: ")
	if eva == '1':
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
	###################### Take away rare words ######################
	i, j=0, 0
	deleteList=[]
	for word in totalDic:
		if totalDic[word] < int(0.005*len(TrainSetFileNames)+10):
			deleteList.append(word)
			j+=1
			continue
		if word in stopword:
			deleteList.append(word)
			j+=1
			continue
		i+=1
	print("i = "+str(i)+"\tj = "+str(j))
	for word in deleteList:
		del totalDic[word]
	print('done deleting')
	##################################################################

	############ Calculate each word's pr(W|S) & pr(W|H) #############
	PrWS={}
	PrWH={}
	p = len(totalDic)
	mspam, mham = 0, 0
	i, j=0, 0
	deleteList=[]
	for word in totalDic:
		if (word in spamDic) and (totalDic[word] != spamDic[word]):
			#Word in both spam and ham
			t = round(spamDic[word]/numtrainSpm, 4)
			if (t>0.3) and (t<0.7):
				deleteList.append(word)
				j+=1
				continue
			PrWS[word] = t
			PrWH[word] = round((totalDic[word]-spamDic[word])/numtrainHam, 4)
			i+=1
		elif (word in spamDic) and (totalDic[word] == spamDic[word]):
			#All in spam, m estimate for ham
			t = round(spamDic[word]/numtrainSpm, 4)
			if (t>0.3) and (t<0.7):
				deleteList.append(word)
				j+=1
				continue
			PrWS[word] = t
			PrWH[word] = round((1/2)/(numtrainHam+1), 4)
			i+=1
		else:
			#All in ham, m estimate for spam
			t = round((1/2)/(numtrainSpm+1), 4)
			if (t>0.3) and (t<0.7):
				deleteList.append(word)
				j+=1
				continue
			PrWS[word] = t
			PrWH[word] = round(totalDic[word]/numtrainHam, 4)
			i+=1
	for word in deleteList:
		del totalDic[word]
	deleteList=[]
	print('done deleting for useless pr')	
	
	##################################################################

	############# write it to a file so it will be faster ############
	# with open('wordSpamHamRate.txt', 'w') as f:
	# 	for word in totalDic:
	# 		f.write(str(PrWS[word])+"\t"+str(PrWH[word])+"\t"+word+"\n")
	# f.closed
	##################################################################

	return PrWS, PrWH

def checkFileExist(file):
	if not os.path.exists(file):
		print("The file/folder "+file+" does not exist, exit...")
		sys.exit()

def main():
	input("\n Before You start, make sure the folder you enter is the\n output folder of ExtractContent.py with your origin emails.\n Press 'Enter' to continue\n")
	############################# Get train folder #################################
	trainFolder = input("Please enter a train folder: ")
	checkFileExist(trainFolder)
	TrainSetFileNames = os.listdir(trainFolder)

	############################## Get Spam label ##################################
	spamLabel = input("Please enter a spam label file\n(contains both and only train & test spams): ")
	checkFileExist(spamLabel)

	######################### Build Spm Lst for Train&Test #########################
	trainSpmLst, numtrainSpm = [], 0
	SpmLst, numtestSpm = [], 0
	with open(spamLabel) as f:
		lines = f.readlines()
		for line in lines:
			items = line.split()
			if items[0] is '0':
				if items[1] in TrainSetFileNames:
					trainSpmLst.append(items[1])
					numtrainSpm += 1
				else:
					numtestSpm += 1
				SpmLst.append(items[1])
	f.closed
	print("The Spam List is built")
	############################## Set Classifier ##################################
	# clf = setClf()
	PrWS, PrWH = getWordSpamRate(trainFolder, trainSpmLst, numtrainSpm, (len(TrainSetFileNames)-numtrainSpm))
	print("Got the word spam Rate")
	# print("The Classifier is all set")

	############################## Start the test ##################################
	while True:
		inputFolder = input("Enter the train or test folder to evaluate\n or type 'exit' to leave: ")
		if inputFolder == "exit":
			sys.exit()
		if not os.path.exists(inputFolder):
			print("The folder "+inputFolder+" does not exist")
			continue
		SetFileNames = os.listdir(inputFolder)
		if inputFolder == trainFolder:
			trainSpm = numtrainSpm
		else:
			trainSpm = numtestSpm
		print("-----------------------------------------------------")
		print("Classify "+inputFolder)
		classify(inputFolder, PrWS, PrWH, SpmLst, (trainSpm/len(SetFileNames)))
		print("########################## ALL DONE ##########################")
		
	



main()