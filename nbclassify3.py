    import sys
    import math
    testtextfile = open(sys.argv[1])
    #testtextfile = open("test-text.txt")
    nbmodeltext = open("nbmodel.txt")
    learnList = []
    priorDict = {}
    conditionalProbDict = {}
    reviewsDict = {}

    vocabDict = {}
    count = 0
    for line in nbmodeltext:
        if count in [1 , 2 , 3 , 4]:
            li = line.split('\t')
            priorDict[li[0]] = li[1].strip('\n')
        if count > 7:
            li = line.split('\t')
            probabList = [li[1],li[2],li[3],li[4].strip('\n')]
            conditionalProbDict[li[0]]= probabList
            vocabDict.setdefault(li[0])
        count += 1

    for line in testtextfile:
        words = line.split(' ', 1)
        reviewsDict[words[0]] = words[1].lower()
    testtextfile.close()

    #Output File
    f = open("nboutput.txt" , "w+")
    classes = ["positive" , "negative" , "deceptive" , "truthful"]

    for l in reviewsDict.items():
        score = []
        W = []
        line = l[1]
        line = line.replace('.', ' ')
        line = line.replace(',', ' ')
        line = line.replace('/', ' ')
        words = line.split()
        for word in words:
            word = word.strip('?:!.,\'<>;-_@ %$&"()#*')
            if word in vocabDict:
                W.append(word)
        i = 0
        for c1 in classes:
            scoreValue = (math.log(float(priorDict[c1]) , 10))
            for word in W:
                tempList = conditionalProbDict[word]
                scoreValue += math.log(float(tempList[i]) , 10)
            score.append(scoreValue)
            i += 1
        f.write(l[0] + " ")
        if score[2] > score[3]:
            f.write("deceptive" + " ")
        else:
            f.write("truthful" + " ")
        if score[0] > score[1]:
            f.write("positive")
        else:
            f.write("negative")
        f.write("\n")


