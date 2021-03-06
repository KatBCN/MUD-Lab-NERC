#! /usr/bin/python3

import sys
import re
from os import listdir

from xml.dom.minidom import parse
from nltk.tokenize import word_tokenize


   
## --------- tokenize sentence ----------- 
## -- Tokenize sentence, returning tokens and span offsets

def tokenize(txt):
    offset = 0
    tks = []
    ## word_tokenize splits words, taking into account punctuations, numbers, etc.
    for t in word_tokenize(txt):
        ## keep track of the position where each token should appear, and
        ## store that information with the token
        offset = txt.find(t, offset)
        tks.append((t, offset, offset+len(t)-1))
        offset += len(t)

    ## tks is a list of triples (word,start,end)
    return tks


## --------- get tag ----------- 
##  Find out whether given token is marked as part of an entity in the XML

def get_tag(token, spans) :
   (form,start,end) = token
   for (spanS,spanE,spanT) in spans :
      if start==spanS and end<=spanE : return "B-"+spanT
      elif start>=spanS and end<=spanE : return "I-"+spanT

   return "O"
 
## --------- Feature extractor ----------- 
## -- Extract features for each token in given sentence

def extract_features(tokens) :

   # for each token, generate list of features and add it to the result
   result = []
   for k in range(0,len(tokens)):
      tokenFeatures = [];
      t = tokens[k][0]

      tokenFeatures.append("form="+t)
      tokenFeatures.append("suf3="+t[-3:])
      # add feature for suffix of length 4
      tokenFeatures.append("suf4=" + t[-4:])
      # add feature for suffix of length 5
      tokenFeatures.append("suf5=" + t[-5:])
      # add feature for prefix of length 3
      tokenFeatures.append("pre3=" + t[:3])
      # add feature for length of token
      tokenFeatures.append("len=" + str(len(t)))

      # add features for lowercase, uppercase, titlecase
      if t.islower():
         tokenFeatures.append("case=lower")
      if t.isupper():
         tokenFeatures.append("case=upper")
      if t.istitle():
         tokenFeatures.append("case=title")

      # add feature to indicate if not all the characters in the token are letters
      if not t.isalpha():
         tokenFeatures.append("isNotAlpha")

      # add feature to indicate DrugBank dictionary value in lowercase
      if t.lower() in dict_DrugBank:
         tokenFeatures.append("dictDB="+dict_DrugBank[t.lower()])

      # add feature to indicate if token in HSDB list in lowercase
      if t.lower() in hsdbList:
         tokenFeatures.append("hsdbList")

      if k>0 :
         tPrev = tokens[k-1][0]
         tokenFeatures.append("formPrev="+tPrev)
         tokenFeatures.append("suf3Prev="+tPrev[-3:])
         
         # add features for previous token lowercase or uppercase
         if tPrev.islower():
            tokenFeatures.append("casePrev=lower")
         if tPrev.isupper():
            tokenFeatures.append("casePrev=upper")
         # add feature to indicate if not all the characters in the previous token are letters
         if not tPrev.isalpha():
            tokenFeatures.append("Prev=isNotAlpha")
         # add feature to indicate previous token's DrugBank dictionary value in lowercase
         if tPrev.lower() in dict_DrugBank:
            tokenFeatures.append("dictDBPrev="+dict_DrugBank[tPrev.lower()])
      else :
         tokenFeatures.append("BoS")

      # Adding features related to the token two places before the current token
      if k>1 :
         tPrev2 = tokens[k-2][0]
         tokenFeatures.append("formPrev2="+tPrev2)
         tokenFeatures.append("suf3Prev2="+tPrev2[-3:])

         # add features for second previous token lowercase or uppercase
         if tPrev2.islower():
            tokenFeatures.append("casePrev2=lower")
         if tPrev2.isupper():
            tokenFeatures.append("casePrev2=upper")
         # add feature to indicate if not all the characters in the second previous token are letters
         if not tPrev2.isalpha():
            tokenFeatures.append("Prev2=isNotAlpha")
      else :
         pass # do not add feature to indicate token is in second place of sentence

      if k<len(tokens)-1 :
         tNext = tokens[k+1][0]
         tokenFeatures.append("formNext="+tNext)
         tokenFeatures.append("suf3Next="+tNext[-3:])
         # add feature to indicate if not all the characters in the next token are letters
         if not tNext.isalpha():
            tokenFeatures.append("Next=isNotAlpha")
      else:
         tokenFeatures.append("EoS")

      # # Adding features related to the token two places after the current token
      # if k<len(tokens)-2 :
      #    tNext2 = tokens[k + 2][0]
      #    tokenFeatures.append("formNext2=" + tNext2)
      #    tokenFeatures.append("suf3Next2=" + tNext2[-3:])
      #    # add feature to indicate if not all the characters in the second next token are letters
      #    if not tNext2.isalpha():
      #       tokenFeatures.append("Next2=isNotAlpha")
      # else :
      #    pass # do not add feature to indicate token is in second to last place of sentence


    
      result.append(tokenFeatures)
    
   return result


## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  baseline-NER.py target-dir
## --
## -- Extracts Drug NE from all XML files in target-dir, and writes
## -- them in the output format requested by the evalution programs.
## --

# adding drug bank dictionary to program in lowercase
dict_DrugBank = {}
file_DrugBank = open("DrugBank.txt")
for line in file_DrugBank:
    key, value = line.rstrip().lower().split("|",1)
    dict_DrugBank[key] = value

# add HSDB list to program in a set of tokenized lowercase words
file_HSDB = open('HSDB.txt')
hsdbList = set(word_tokenize(file_HSDB.read().lower()))

# directory with files to process
datadir = sys.argv[1]

# process each file in directory
for f in listdir(datadir) :
   
   # parse XML file, obtaining a DOM tree
   tree = parse(datadir+"/"+f)
   
   # process each sentence in the file
   sentences = tree.getElementsByTagName("sentence")
   for s in sentences :
      sid = s.attributes["id"].value   # get sentence id
      spans = []
      stext = s.attributes["text"].value   # get sentence text
      entities = s.getElementsByTagName("entity")
      for e in entities :
         # for discontinuous entities, we only get the first span
         # (will not work, but there are few of them)
         (start,end) = e.attributes["charOffset"].value.split(";")[0].split("-")
         typ =  e.attributes["type"].value
         spans.append((int(start),int(end),typ))
         

      # convert the sentence to a list of tokens
      tokens = tokenize(stext)
      # extract sentence features
      features = extract_features(tokens)

      # print features in format expected by crfsuite trainer
      for i in range (0,len(tokens)) :
         # see if the token is part of an entity
         tag = get_tag(tokens[i], spans) 
         print (sid, tokens[i][0], tokens[i][1], tokens[i][2], tag, "\t".join(features[i]), sep='\t')

      # blank line to separate sentences
      print()
