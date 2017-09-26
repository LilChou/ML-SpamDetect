from sklearn import svm
import os
import collections, re


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

def classify(clf, path, TotalWordList, trainSpmLst):
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
			if clf.predict([lst])[0] == 'SPAM':
				if filename in trainSpmLst:
					TP += 1
				else:
					FP += 1
			elif clf.predict([lst])[0] == 'HAM':
				if filename in trainSpmLst:
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
	#get list of all words and list of each file's words
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
	###################### Take away rare words ######################
	i,j=0,0
	deleteList=[]
	for word in TotalWordDict:
		if TotalWordDict[word] < 300:
			deleteList.append(word)
			j+=1
			continue
		i+=1
	print("i = "+str(i)+"\tj = "+str(j))
	for word in deleteList:
		del TotalWordDict[word]
	# for word in stopword:
	# 	if word in TotalWordDict:
	# 		del TotalWordDict[word]
	print('done deleting')
	##################################################################
	for word in TotalWordDict:
		TotalWordList.append(word)


	for fileWordList in EachFileWordList:
		lst = []
		for item in TotalWordList:
			if item in fileWordList:
				lst.append("1")
			else:
				lst.append("0")
		EachFileWordExist.append(lst)
	return EachFileWordExist, TotalWordList


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
	print("Finish building Spm lst for Train & Test")
	##################################################################
	
	######################### Build X & Y ############################
	Y=[]
	for file in TrainSetFileNames:
		if file in trainSpmLst:
			Y.append("SPAM")
			# print("SPAM")
		else:
			Y.append("HAM")
	print("Finish building Y")

	
	X, TotalWordList = getWordExist(path+trainFolder, stopword)
	print("Finish building X and TotalWordList")
	# with open("XTrainFileWordExist.txt", 'w') as f:
	# 	for lst in X:
	# 		for item in lst:
	# 			f.write(str(item)+" ")
	# 		f.write('\n')
	# f.closed
	# with open("TotalWordList.txt", 'w') as f:
	# 	for item in TotalWordList:
	# 		f.write(str(item)+" ")
	# f.closed
	# print("Finish write in file")
	# return 

	# X=[]
	# with open("XTrainFileWordExist.txt") as f:
	# 	lines = f.readlines()
	# 	for line in lines:
	# 		lst=[]
	# 		items = line.split()
	# 		for item in items:
	# 			lst.append(item)
	# 		X.append(lst)
	# f.closed

	# TotalWordList=[]
	# with open('TotalWordList.txt') as f:
	# 	content = f.read()
	# 	items = content.split()
	# 	for item in items:
	# 		TotalWordList.append(item)
	# f.closed
	# print("Done reading the files")
	##################################################################
	clf = svm.SVC()
	clf.fit(X,Y)
	print("Done Fitting to SVM clf")
	print("---------------------------------------------------")
	print("Classify Train Set")
	classify(clf, path+trainFolder, TotalWordList, trainSpmLst)
	print("Classify Test Set")
	classify(clf, path+testFolder, TotalWordList, testSpmLst)
	print("---------------------------------------------------")

main()












