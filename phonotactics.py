#!/usr/bin/env python3

import csv
import random

phoneticTypeMap = {}
#maps consonant type to a list of the constants with their number of entries based their weight in the phonetic table; these lists can then be selected from randomly to acheived the desired bias in their usage frequency

sonorityPriority = ['APPROX','NASAL','FRIC','STOP']

def loadPhoneticTable():
    with open('phonetic_table.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for phono_row in csv_reader:

            phoneme = phono_row['ipa']
            phonotype = phono_row['type']
            phonofield = [phoneme] * int(phono_row['weight'])
            if phonotype in phoneticTypeMap:
                phoneticTypeMap[phonotype].extend(phonofield)
            else:
                phoneticTypeMap[phonotype] = phonofield

def generateRoot():
    newSyllable = ""
    #is there an onset? 50/50 chance
    if random.randint(0,1):
        newSyllable = random.choice(phoneticTypeMap["STOP"]) #lets always have stops for starts?
    #now pick a vowel
    nucleusVowel = random.choice(phoneticTypeMap["WVOWEL"]+phoneticTypeMap["VOWEL"])
    newSyllable += nucleusVowel
    if nucleusVowel in phoneticTypeMap["VOWEL"]:
        #small chance of dipthongs after strong vowels with a weak vowel
        if not random.randint(0,30):
            newSyllable += random.choice(phoneticTypeMap["WVOWEL"])
    else:
        #weak vowels get sonorants (approximates or nasals) as simple codas
        newSyllable += random.choice(phoneticTypeMap["NASAL"] + phoneticTypeMap["APPROX"])
        #and we're done with our weak vowel words
        return newSyllable
    #lets make some cluster codas
    longerChance = 1
    for phonotype in sonorityPriority:
        if not random.randint(0,longerChance):
            newSyllable += random.choice(phoneticTypeMap[phonotype])
            longerChance += random.randint(0,3) # make it potentially less likely the word will get longer
        else:
            if longerChance > 1:
                longerChance -= random.randint(0,3) # make it potentially more likely the word will get longer
            if longerChance < 0: longerChance = 0
    return newSyllable

def generateFunctionWord():
    newWord = ""
    #function words mostly start with obstruents
    if random.randint(0,4):
        newWord += random.choice(phoneticTypeMap["FRIC"]+phoneticTypeMap["STOP"])
    #vowel can be anything, incl dipthong
    nucleusVowel = random.choice(phoneticTypeMap["WVOWEL"]+phoneticTypeMap["VOWEL"])
    newSyllable += nucleusVowel
    if nucleusVowel in phoneticTypeMap["VOWEL"]:
        #small chance of dipthongs after strong vowels with a weak vowel
        if not random.randint(0,30):
            newSyllable += random.choice(phoneticTypeMap["WVOWEL"])
    #codas with optional sonorant and required stop
    if random.randint(0,2):
        newWord += random.choice(phoneticTypeMap["APPROX"]+phoneticTypeMap["NASAL"])
    newWord += random.choice(phoneticTypeMap["STOP"]+phoneticTypeMap["FRIC"])
    return newSyllable

def expandRoot(root):
    lexeme = ""
    #if the word starts with a weak vowel it can get a obstruent
    if (root[0] in phoneticTypeMap["WVOWEL"]) and random.randint(0,2):
        lexeme = random.choice(phoneticTypeMap["STOP"]+phoneticTypeMap["FRIC"])
    #if the word starts with a vowel it can can get a softer sound
    if (root[0] in phoneticTypeMap["VOWEL"]) and random.randint(0,3):
        lexeme = random.choice(phoneticTypeMap["NASAL"])
    lexeme += root
    #there are some two syllable roots, but second syllable starts with vowel and is short
    if random.randint(0,2):
        second_root = "XXXXXXX"
        while (len(second_root) > 4) and (second_root[0] not in phoneticTypeMap["VOWEL"]):
            second_root = generateRoot()
        lexeme += second_root
    elif (len(lexeme) < 4) and random.randint(0,1):
    #maybe add another consant to short roots
        if lexeme[-1] in phoneticTypeMap["NASAL"]: lexeme += random.choice(phoneticTypeMap["STOP"])
        if lexeme[-1] in phoneticTypeMap["FRIC"]: lexeme += random.choice(phoneticTypeMap["STOP"])
        if lexeme[-1] in phoneticTypeMap["STOP"]: lexeme += random.choice(phoneticTypeMap["FRIC"])
        if lexeme[-1] in phoneticTypeMap["APPROX"]: lexeme += random.choice(phoneticTypeMap["FRIC"])
    elif (len(lexeme) < 5) and not random.randint(0,4):
    #slightly less chance to make roots slightly longer again
        if lexeme[-1] in phoneticTypeMap["NASAL"]: lexeme += random.choice(phoneticTypeMap["STOP"])
        if lexeme[-1] in phoneticTypeMap["FRIC"]: lexeme += random.choice(phoneticTypeMap["STOP"])
        if lexeme[-1] in phoneticTypeMap["STOP"]: lexeme += random.choice(phoneticTypeMap["FRIC"])
        if lexeme[-1] in phoneticTypeMap["APPROX"]: lexeme += random.choice(phoneticTypeMap["FRIC"])
    #finally we perform some collapsing and transposing to give some humanization
    #sometimes make things plosive at the start
    if not random.randint(0,2):
        if lexeme[0] == "k": lexeme[0] = "K"
        if lexeme[0] == "p": lexeme[0] = "P"
    #often collapse some combos
    if random.randint(0,2):
        if "jŋ" in lexeme: lexeme.replace("jŋ","n")
        if "hb" in lexeme: lexeme.replace("hb","b")
        if "nb" in lexeme: lexeme.replace("nb","m")
        if "ɕg" in lexeme: lexeme.replace("ɕg","g")
        if "ŋʃ" in lexeme: lexeme.replace("ŋʃ","ns")
    #__FUTURE__add some more of the collapses for longer combos, some ellision and alignment (voiced with voiced)

    #very occasionally add an s to the begging of words
    if (not random.randint(0,50)) and (lexeme[0] in phoneticTypeMap["STOP"]): lexeme = 's' + lexeme

    return lexeme
