import os
import sys
import collections
import re
from sklearn import svm


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

def classify(clf, path, TotalWordList, SpmLst):
	filenames = os.listdir(path)
	TP, FP, TN, FN = 0, 0, 0, 0
	for filename in filenames:
		lst=[]
		with open(path+'/'+filename, "r", encoding='utf-8', errors='ignore') as f:
			lines = f.readlines()
			bagofwords = [ collections.Counter(re.findall(r'[a-zA-Z_]+', txt)) for txt in lines]
			dic = dict(sum(bagofwords, collections.Counter()))
			for word in TotalWordList:
				if word in dic:
					lst.append("1")
				else:
					lst.append("0")
			if clf.predict([lst])[0] == '0':
				if filename in SpmLst:
					TP += 1
				else:
					FP += 1
			elif clf.predict([lst])[0] == '1':
				if filename in SpmLst:
					FN += 1
				else:
					TN += 1
			else:
				print(filename+" GOT THIS clf: "+ clf.predict([lst])[0])
	evaluation(TP, FP, TN, FN)


def getWordExist(path, stopword):
	TrainSetFileNames = os.listdir(path)
	EachFileWordList = []
	TotalWordList = []
	TotalWordDict = {}
	EachFileWordExist = []
	############## get list of all words and list of each file's words #############
	for file in TrainSetFileNames:
		dic = {}
		lst = []
		with open(path+'/'+file, "r", encoding='utf-8', errors='ignore') as f:
			lines = f.readlines()
			bagofwords = [ collections.Counter(re.findall(r'[a-zA-Z_]+', txt)) for txt in lines]
			dic = sum(bagofwords, collections.Counter())
			EachFileWordList.append(dic)
		f.closed
	TotalWordDict = dict(sum(EachFileWordList, collections.Counter()))
	############################# Take away rare words #############################
	i,j=0,0
	deleteList=[]
	for word in TotalWordDict:
		if TotalWordDict[word] < 300:
			deleteList.append(word)
			j+=1
			continue
		i+=1
	# print("i = "+str(i)+"\tj = "+str(j))
	for word in deleteList:
		del TotalWordDict[word]
	# for word in stopword:
	# 	if word in TotalWordDict:
	# 		del TotalWordDict[word]
	# print('done deleting')
	################################################################################
	for word in TotalWordDict:
		TotalWordList.append(word)

	############################# Set Features in X ################################
	for fileWordList in EachFileWordList:
		lst = []
		for item in TotalWordList:
			if item in fileWordList:
				lst.append("1")
			else:
				lst.append("0")
		EachFileWordExist.append(lst)
	return EachFileWordExist, TotalWordList


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
	spamLabel = input("Please enter spam label file\n(contains both and only train & test spams): ")
	checkFileExist(spamLabel)

	######################### Build Spm Lst for Train&Test #########################
	trainSpmLst = []
	SpmLst = []
	with open(spamLabel) as f:
		lines = f.readlines()
		for line in lines:
			items = line.split()
			if items[0] is '0':
				if items[1] in TrainSetFileNames:
					trainSpmLst.append(items[1])
				SpmLst.append(items[1])
	f.closed
	print("The Spam List is built")

	############################## Set Classifier ##################################
	# clf = setClf()
	print("Be patient to the classifier setting")
	Y=[]
	for file in TrainSetFileNames:
		if file in trainSpmLst:
			Y.append("0")
			# print("SPAM")
		else:
			Y.append("1")
	X, TotalWordList = getWordExist(trainFolder, stopword)
	clf = svm.SVC()
	clf.fit(X,Y)
	print("The Classifier is all set")

	############################## Start the test ##################################
	while True:
		inputFolder = input("Enter the train or test folder to evaluate\n or type 'exit' to leave: ")
		if inputFolder == "exit":
			sys.exit()
		if not os.path.exists(inputFolder):
			print("The folder "+inputFolder+" does not exist")
			continue
		print("-----------------------------------------------------")
		print("Classify "+inputFolder)
		classify(clf, inputFolder, TotalWordList, SpmLst)
		print("########################## ALL DONE ##########################")
		
	



main()