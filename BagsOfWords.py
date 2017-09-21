import os               #get the file from "path"
import codecs           #open files with different encoding
import collections, re  #implement bag of words
import operator         #sort dictionary



'''
#get all files in the directory and save into a list
def GetFilesFromPath(path):
    filenames = os.listdir(path)
    return filenames

#input filename; return dict with words and frequency
def BagOfWordsFetching(filename):
    dic = {}
    with codecs.open(path+"/"+filename, "r",encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        #get the bag of words from every line
        bagofwords = [ collections.Counter(re.findall(r'[a-zA-Z_]+', txt)) for txt in lines]
        #Sum bag of words of the file
        t = sum(bagofwords, collections.Counter())
        print('-----------------------------------------')
        print('type of Sum of collections counter: ')
        print(type(t))
        print('-----------------------------------------')
        dic = dict(t)
    f.closed
    return dic
def EntireDB_BagOfWords(AllFileBOW, file):
    BagsOfWords = sorted(dict(sum(AllFileBOW, collections.Counter())).items(), key=operator.itemgetter(1), reverse=True)
    with open(file, 'w') as f:
    for items in BagsOfWords:
        f.write(str(items)+'\n')
    f.closed

    return BagsOfWords

def main():
    print('#############################################')
    #Set the path that we're going to find the email contents
    path = 'CSDMC2010_SPAM/TRAIN_Content'
    filenames = GetFilesFromPath(path)

    AllFileBOW = []
    for filename in filenames:
        dic = BagOfWordsFetching(filename)
        AllFileBOW.append(dic)

    BagsOfWords = EntireDB_BagOfWords(AllFileBOW, 'BOW.txt')
    
    print('+++++++++++++++++++++++++++++++++++++++++++++++++')
    print('#############################################')
    print()

main()

'''

i=0
SumBOW=[]
BagsOfWords=[]
for filename in os.listdir(path):
    print(filename)
    #Open the files with different encoding
    with codecs.open(path+"/"+filename, "r",encoding='utf-8', errors='ignore') as f:
        # print('+++++++++++++++++++++++++++++++++++++++++++++++++')
        lines = f.readlines()
        # print(lines)

        #
        bagofwords = [ collections.Counter(re.findall(r'[a-zA-Z_]+', txt)) for txt in lines]
        # print('-------------------------------------------------')

        # sorted_dict = sorted(dict(sum(bagofwords, collections.Counter())).items(), key=operator.itemgetter(1), reverse=True)
        # SumBOW.append(sorted_dict)
        dic = sum(bagofwords, collections.Counter())
        SumBOW.append(dic)


        # for Bow in SumBOW:
        #     print(Bow)
        # print('+++++++++++++++++++++++++++++++++++++++++++++++++')
    i += 1
    # if i is 2:
    #     break
print('i = '+str(i))

#BagsOfWords = dict(sum(SumBOW, collections.Counter()))
BagsOfWords = sorted(dict(sum(SumBOW, collections.Counter())).items(), key=operator.itemgetter(1), reverse=True)
# print("Bags of words: ")
# print(BagsOfWords)


#write total data base into BOW.txt
with open('BOW.txt', 'w') as f:
    for items in BagsOfWords:
        f.write(str(items)+'\n')
    f.closed

print('+++++++++++++++++++++++++++++++++++++++++++++++++')
print('#############################################')
print()

# WierdList.sort()
# for item in WierdList:
#     print(item)
