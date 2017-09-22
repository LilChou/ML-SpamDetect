import os               #get the file from "path"
import codecs           #open files with different encoding
import collections, re  #implement bag of words
import operator         #sort dictionary
import sys

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

def getBOW(filenames, folder):
	BOW = []
	for filename in filenames:
		dic = {}
		with codecs.open(folder+"/"+filename, "r",encoding='utf-8', errors='ignore') as f:
			lines = f.readlines()
			#get the bag of words from every line
			bagofwords = [ collections.Counter(re.findall(r'[a-zA-Z_]+', txt)) for txt in lines]
			#Sum bag of words of the file
			dic = sum(bagofwords, collections.Counter())
		f.closed
		BOW.append(dic)
	BOW = sorted(dict(sum(BOW, collections.Counter())).items(), key=operator.itemgetter(1), reverse=True)
	return BOW

############################# main func starts here ################################
#----------------- Get Train Folder ---------------------
path = '../CSDMC2010_SPAM/'
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




# TrainBOW = list2Dict(getBOW(TrainSetFileNames, folder))
# print("Fininsh getting TrainBOW")

# SpamBOW = list2Dict(getBOW(SpamList, folder))
# print("Fininsh getting BOW")

# wordSpamRate = spamRate(TrainBOW, SpamBOW)
# print("Finish getting wordSpamRate")

while(1):
	print("enter 'exit' to shut the program")
	test=input("Test a folder of emails( or 'exit' ): ")
	if test == 'exit':
		break
	print('Classifying folder '+test)
	

print('++++++++++++++++++++++++++++++++++++++++++')
# print(TrainSetFileNames)
# print(SpamList)
# print(SpamBOW)
# print(wordSpamRate)
print('++++++++++++++++++++++++++++++++++++++++++')
# BagsOfWords = 

#############################  main func ends here  ################################










