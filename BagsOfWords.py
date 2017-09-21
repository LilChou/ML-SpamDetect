import os               #get the file from "path"
import codecs           #open files with different encoding
import collections, re  #implement bag of words
import operator         #sort dictionary



#get all files in the directory and save into a list
def GetFilesFromPath(path):
    filenames = os.listdir(path)
    return filenames

#input filename; return dict with words and frequency
def BagOfWordsFetching(path, filename):
    dic = {}
    with codecs.open(path+"/"+filename, "r",encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        #get the bag of words from every line
        bagofwords = [ collections.Counter(re.findall(r'[a-zA-Z_]+', txt)) for txt in lines]
        #Sum bag of words of the file
        t = sum(bagofwords, collections.Counter())
        # print('-----------------------------------------')
        # # print('type of Sum of collections counter: ')
        # # print(type(t))
        # print('-----------------------------------------')
        # dic = dict(t)
        dic = t
    f.closed
    return dic
def EntireDB_BagOfWords(AllFileBOW, file):
    BagsOfWords = sorted(dict(sum(AllFileBOW, collections.Counter())).items(), key=operator.itemgetter(1), reverse=True)
    
    #write the total BOW into file
    with open(file, 'w') as f:
        for items in BagsOfWords:
            f.write(str(items)+'\n')
    f.closed

    return BagsOfWords

def main():
    print('#############################################')
    #Set the path that we're going to find the email contents
    path = 'CSDMC2010_SPAM/tt'
    filenames = GetFilesFromPath(path)
    i=0
    AllFileBOW = []
    for filename in filenames:
        dic = BagOfWordsFetching(path, filename)
        AllFileBOW.append(dic)

    BagsOfWords = EntireDB_BagOfWords(AllFileBOW, 'BOW.txt')
    
    print('+++++++++++++++++++++++++++++++++++++++++++++++++')
    print('#############################################')
    print()

main()
