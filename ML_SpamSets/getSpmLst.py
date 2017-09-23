import sys

def main():
	SpmTrainLst=[]
	SpmTestLst=[]
	SpmTrain=0
	SpmTest=0
	file = sys.argv[1]
	fSpmTrain = sys.argv[2]
	fSpmTest = sys.argv[3]
	print('######################################################')
	with open(file) as f:
		lines = f.readlines()
		for line in lines:
			items = line.split()
			if items[0] is '0':
				# print("Is Spam")
				if items[1].find('TRAIN') != -1:
					SpmTrainLst.append(items[1])
					# print("Is TRAIN")
					SpmTrain += 1
				elif items[1].find('TEST') != -1:
					SpmTestLst.append(items[1])
					# print("Is TEST")
					SpmTest += 1
				else:
					print("Can't recognize the file "+items[1])
					return
		print("SpmTrain: "+str(SpmTrain)+"\nSpmTest: "+str(SpmTest))
	f.closed
	print('######################################################')

	with open(fSpmTrain, 'w') as f:
		for item in SpmTrainLst:
			f.write(item+'\n')
	f.closed
	with open(fSpmTest, 'w') as f:
		for item in SpmTestLst:
			f.write(item+'\n')
	f.closed
	print('all done')
main()