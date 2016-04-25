import nltk,os,glob
from nltk.corpus import stopwords
englishStopwords = stopwords.words('english')
seasonsPaths = ['S01/','S02/','S03/','S04/','S05/','S06/','S07/','S08/','S09/','S10/','S11/','S12/','S13/','S14/','S15/','S16/','S17/','S18/']

def gatherInfoForEpisode(episodePath,keys):
  raw = open(episodePath,encoding = "ISO-8859-1").read()
  words = nltk.word_tokenize(raw)
  words = [w.lower() for w in words if w.lower() not in englishStopwords and w.isalpha() and len(w)>3 and w.lower() is not 'br']
  fd = nltk.FreqDist(words)
  threshold = findThreshold(words)
  keysForEpisode = [w+str(fd[w]) for w in fd if fd[w]>= threshold]
  keysForEpisode = [helper(key) for key in keysForEpisode]
  keywordPath = episodePath+'Key'
  f = open(keywordPath,'a')
  f.write(' '.join(keysForEpisode))
  f.close()
  res = [w for w in keysForEpisode if w not in keys]
  return res

def helper(key):
  if key[-2].isalpha():
      tmp = key[:-1]+'0'
      key = tmp+key[-1]
  return key

def findThreshold(words):
  lenWords = len(words)
  lenSetWords = len(set(words))
  lexicalDiv = lenWords/lenSetWords
  return round(lexicalDiv*3)

def findKeywords(folderPath) :
  keywords = []
  os.chdir(folderPath)
  for episode in glob.glob('S*E*') :
    keywords += gatherInfoForEpisode(episode,keywords)
  return keywords

def updateKeywords(keys) :
  k = ' '.join(keys)
  f = open('Keywords','a')
  f.write(k)
  f.write(' ')
  f.close()
  os.chdir('..')

def gatherDataForSeason(pathToSeason) :
  keys = findKeywords(pathToSeason)
  #print(keys)
  print('Length : ',len(set(keys)))
  updateKeywords(keys)

def gatherAllData(pathToSeasons) :
  for seasonPath in pathToSeasons:
   gatherDataForSeason(seasonPath)
   print('Season '+seasonPath[1:4]+'\n') 

gatherAllData(seasonsPaths)

