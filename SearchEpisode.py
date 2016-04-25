import nltk,os,glob
from nltk.corpus import stopwords
englishStopwords = stopwords.words('english')
seasonPaths = ['S01/','S02/','S03/','S04/','S05/','S06/','S07/','S08/','S09/','S10/','S11/','S12/','S13/','S14/','S15/','S16/','S17/','S18/']

def search():
  occurances = {}
  userInput = input('Search for ?\t')
  for seasonPath in seasonPaths:
    occurances = searchSeason(seasonPath,userInput,occurances)
  return sorted(occurances, key=occurances.get, reverse=True)

def searchSeason(seasonPath,userInput,occurances):
  os.chdir(seasonPath)
  keywords = open("Keywords",encoding = "ISO-8859-1").read()
  userWords = nltk.word_tokenize(userInput)
  for w in userWords:
    w = w.lower()
    if w in keywords:
      for episodeKey in glob.glob('S*E*Key') :
        occurances = searchEpisode(seasonPath,episodeKey,w,occurances)
  os.chdir('..')
  return occurances

def searchEpisode(seasonPath,episodeKeyPath,word,occurances):
  f = open(episodeKeyPath).read()
  f = nltk.word_tokenize(f)
  for w in f:
    if w[:-2] == word:
      if episodeKeyPath[:-3] not in occurances:
        occurances[episodeKeyPath[:-3]] = int(w[-2:])
      else:
        occurances[episodeKeyPath[:-3]] += int(w[-2:])
  return occurances

def printMostFrequent(occurances,times):
  print(occurances[:times])

printMostFrequent(search(),5)
