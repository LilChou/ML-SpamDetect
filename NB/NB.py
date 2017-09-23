import os               #get the file from "path"
import codecs           #open files with different encoding
import collections, re  #implement bag of words
import operator         #sort dictionary
import sys

def spamClassify(path, wordSpamRate, SpamList, PrS):
	filenames = os.listdir(path)
	n=0		#calculate num of files
	dspam=0		#calculate num of detected spam
	TP, FP, TN, FN = 0, 0, 0, 0
	for filename in filenames:
		pspam, pham = 1, 1
		dic = getBOW(filename, path)
		for key in dic:
			if key in wordSpamRate and wordSpamRate[key]!=1:
				# print("key="+str(key)+" SpamRate: "+str(wordSpamRate[key]))
				pspam *= dic[key]*wordSpamRate[key]
				pham *= dic[key]*(1-wordSpamRate[key])
		if pspam > pham:
			# print("Spam")
			if filename in SpamList:
				TP += 1
			else:
				FP += 1
			dspam += 1
		else:
			# print("Ham")
			if filename in SpamList:
				FN += 1
			else:
				TN += 1

		# print("pspam: "+str(pspam)+"\npham: "+str(pham))
		n += 1

	print('True Positive: '+str(TP))
	print('False Positive: '+str(FP))
	print('True Negative: '+str(TN))
	print('False Negative: '+str(FN))
	print()
	print('False Positive Rate: '+str(FP/n))
	print('False Negative Rate: '+str(FN/n))
	if (TP+FN) != 0:
		RC = TP/(TP+FN)
		print('Recall: '+str(RC))
	else:
		print('Recall: The Division of Recall is zero!!')
		RC = 0

	if (TP+FP) != 0:
		PC = TP/(TP+FP)
		print('Precision: '+str(PC))
	else:
		print('Precision: The Division of Precision is zero!!')
		PC = 0

	if (PC+RC) != 0:
		FS = 2*PC*RC/(PC+RC)
		print('F-Score: '+str(FS))
	else:
		print('F-Score: The Divisioni of F-Score is zero!!')
	# return 
	


def writeInFile(objs, file):
	with open(file, 'w') as f:
		f.write("{")
		for key in objs:
			f.write(" '"+key+"': "+str(objs[key])+",")
		f.write("}")
	f.closed

def spamRate(BOW, SpamBOW):
	SpamRate={}
	for key in BOW:
		if key in SpamBOW:
			SpamRate[key] = SpamBOW[key]/BOW[key]
	return SpamRate

#list of tuples to dictionary
def list2Dict(lList):
	BOW = {}
	for ttuple in lList:
		BOW[ttuple[0]] = ttuple[1]
	return BOW

def getSpamRate():
	BOW = getFrequency(sys.argv[1])
	SpamBOW = getFrequency(sys.argv[2])
	# print(BOW)
	wordSpamRate = spamRate(BOW, SpamBOW)
	print(wordSpamRate)
	writeInFile(wordSpamRate, sys.argv[3])
	print('++++++++++++++++++++++++++++++++++++++++++')

def getBOW(filename, folder):
	dic = {}
	with codecs.open(folder+"/"+filename, "r",encoding='utf-8', errors='ignore') as f:
		lines = f.readlines()
		#get the bag of words from every line
		bagofwords = [ collections.Counter(re.findall(r'[a-zA-Z_]+', txt)) for txt in lines]
		#Sum bag of words of the file
		dic = sum(bagofwords, collections.Counter())	
	f.closed
	return dic

def SumBOW(filenames, folder):
	BOW = []
	for filename in filenames:
		BOW.append(getBOW(filename, folder))
	BOW = sorted(dict(sum(BOW, collections.Counter())).items(), key=operator.itemgetter(1), reverse=True)
	return BOW

############################# main func starts here ################################
def main():
	#----------------- Get Train Folder ---------------------
	path = '../ML_SpamSets/'
	folder = input("The training folder: ")
	folder = path + folder
	if not os.path.exists(folder):
		print('The training folder '+folder+' does not exist, exit...')
		sys.exit()
	#get filenames in TRAINING Set
	TrainSetFileNames = os.listdir(folder)


	#----------------- Get Spam Folder ---------------------
	SpamListFile = input("The SpamList of the folder: ")
	if not os.path.exists(SpamListFile):
		print('The SpamList '+SpamListFile+' does not exist, exit...')
		sys.exit()
	#get Spam filenames in SpamListFile
	SpamList = []
	with open(SpamListFile) as f:
		lines = f.readlines()
		for line in lines:
			SpamList.append(line[:-1])
	f.closed
	print("Fininsh getting filelists")
	PrS=len(SpamList)/len(TrainSetFileNames)



	TrainBOW = list2Dict(SumBOW(TrainSetFileNames, folder))
	print("Fininsh getting TrainBOW")

	SpamBOW = list2Dict(SumBOW(SpamList, folder))
	print("Fininsh getting BOW")

	wordSpamRate = spamRate(TrainBOW, SpamBOW)
	print("Finish getting wordSpamRate")


	print('++++++++++++++++++++++++++++++++++++++++++')
	# print(TrainSetFileNames)
	# print(SpamList)
	# print(type(SpamList))
	# print(SpamBOW)
	# print(wordSpamRate)
	print('++++++++++++++++++++++++++++++++++++++++++')


	while(1):
		test=input("\n\nTest a folder of emails( or 'exit' ): ")
		if test == 'exit':
			break
		if not os.path.exists(path+test):
			print('The folder '+path+test+' does not exist')
			continue
		SpamListOfTest = input("The Spamlist of the test case: ")
		if not os.path.exists(SpamListOfTest):
			print('The file '+SpamListOfTest+' does not exist')
			continue

		SpamListClas = []
		with open(SpamListOfTest) as f:
			lines = f.readlines()
			for line in lines:
				SpamListClas.append(line[:-1])
		f.closed


		print('Classifying folder '+test)
		spamClassify(path+test, wordSpamRate, SpamListClas, PrS)




#############################  main func ends here  ################################

main()









