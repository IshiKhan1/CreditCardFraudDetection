# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 03:56:09 2023

@author: DELL
"""

import csv
import random
import math
def loadCsv(filename):
    lines = csv.reader(open(filename, "r"))
    dataset = list(lines)
    for i in range(len(dataset)):
        dataset[i] = [float(x) for x in dataset[i]]
    return dataset
 
def splitDataset(dataset, splitRatio):
    trainSize = int(len(dataset) * splitRatio)
    trainSet = []
    copy = list(dataset)
    while len(trainSet) < trainSize:
        index = random.randrange(len(copy))
        trainSet.append(copy.pop(index))
    return [trainSet, copy]
 
def separateByClass(dataset):
    separated = {}
    for i in range(len(dataset)):
        vector = dataset[i]
        if (vector[-1] not in separated):
            separated[vector[-1]] = []
        separated[vector[-1]].append(vector)
    return separated
 
def mean(numbers):
    return sum(numbers)/float(len(numbers))
 
def stdev(numbers):
    avg = mean(numbers)
    variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
    return math.sqrt(variance)
 
def summarize(dataset):
    summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
    del summaries[-1]
    return summaries
 
def summarizeByClass(dataset):
    separated = separateByClass(dataset)
    summaries = {}
    for classValue, instances in separated.items():
        summaries[classValue] = summarize(instances)
    return summaries
 
def calculateProbability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
    return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent
 
def calculateClassProbabilities(summaries, inputVector):
    probabilities = {}
    for classValue, classSummaries in summaries.items():
        probabilities[classValue] = 1
        for i in range(len(classSummaries)):
            mean, stdev = classSummaries[i]
            x = inputVector[i]
            probabilities[classValue] *= calculateProbability(x, mean, stdev)
    return probabilities
            
def predict(summaries, inputVector):
    probabilities = calculateClassProbabilities(summaries, inputVector)
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.items():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel
 
def getPredictions(summaries, testSet):
    predictions = []
    for i in range(len(testSet)):
        result = predict(summaries, testSet[i])
        predictions.append(result)
    return predictions
 
def getAccuracy(testSet, predictions):
    correct = 0
    for i in range(len(testSet)):
        if testSet[i][-1] == predictions[i]:
            correct += 1
    return (correct/float(len(testSet))) * 100.0

def recall(testSet, predictions):
    correct = 0
    falseNegative = 0
    for i in range(len(testSet)):
        if predictions[i] == 0 and testSet[i][-1]!=predictions[i]:
            falseNegative += 1
        if testSet[i][-1] == predictions[i]:
            correct += 1
    return (correct/(correct + falseNegative))   

def precision(testSet, predictions):
    correct = 0
    falsepositive=0
    for i in range(len(testSet)):
        if testSet[i][-1] == predictions[i]:
            correct += 1
        if predictions[i] == 1 and testSet[i][-1]!=predictions[i]:
            falsepositive+=1
    return (correct/(correct + falsepositive))        

def getFMeasure(testSet, predictions):
    correct = 0
    falseNegative = 0
    falsepositive=0
    for i in range(len(testSet)):
        if predictions[i] != testSet[i][-1]:
            falseNegative += 1
        if testSet[i][-1] == predictions[i]:
            correct += 1
        if predictions[i] == 1 and testSet[i][-1]!=predictions[i]:
            falsepositive+=1    
    return (2*correct/(2*correct + falseNegative+ falsepositive))
def main():
    filename = 'creditcard2.csv'
    
  #print('Split {0} rows into train={1} and test={2} rows'.format(len(dataset),
   #                                              len(trainingSet), len(testSet)))
    #print('Split {0} rows into train={1} and test={2} rows').format(len(dataset),trainingSet,testSet)
    i=1
    j=[1,81,161,301,651,1000,2000]       
    for i in range(len(j)):
        splitRatio =random.uniform(0.5,0.8)
        dataset = loadCsv(filename)
        trainingSet, testSet = splitDataset(dataset, splitRatio)
        print('split',len(dataset))
        print('TrainingSet',len(trainingSet))
        print('TestSet',len(testSet))# prepare model
        summaries = summarizeByClass(trainingSet)
        # test model
       # print(summaries)
        predictions = getPredictions(summaries, testSet)
        accuracy = getAccuracy(testSet, predictions)
        precisionVal = precision(testSet, predictions)
        recallVal = recall(testSet, predictions)
        fVal = getFMeasure(testSet, predictions)
        print('Accuracy: {0}%'.format(accuracy))
        print('Precision: {0}%'.format(precisionVal))
        print('Recall: {0}%'.format(recallVal))
        print('FMeasure: {0}%'.format(fVal))
    # separated=separateByClass(predictions)
    i+=1
#    
#  
    
main()
