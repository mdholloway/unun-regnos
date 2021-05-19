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
    #is there an onset? 50/50 chance
    newSyllable = ""
    if random.randint(0,1):
        newSyllable = random.choice(phoneticTypeMap["STOP"]) #lets always have stops for starts?
    #now pick a vowel
    nucleusVowel = random.choice(phoneticTypeMap["WVOWEL"]+phoneticTypeMap["VOWEL"])
    newSyllable += nucleusVowel
    if nucleusVowel in ['i','a','u']:
        #small chance of dipthongs after strong vowels with a weak vowel
        if not random.randint(0,30):
            newSyllable += random.choice(phoneticTypeMap["WVOWEL"])
    else:
        #"weak" vowels get sonorants (approximates or nasals) as simple codas
        newSyllable += random.choice(phoneticTypeMap["NASAL"] + phoneticTypeMap["APPROX"])
        #and we're done with our weak vowel words
        return newSyllable
    #lets make some cluster codas
    longerChance = 1
    if len(newSyllable) == 1:
        longerChance = 0
    for phonotype in sonorityPriority:
        if not random.randint(0,longerChance):
            newSyllable += random.choice(phoneticTypeMap[phonotype])
            longerChance += random.randint(0,3) # make it potentially less likely the word will get longer
        else:
            if longerChance > 1:
                longerChance -= random.randint(0,3) # make it potentially more likely the word will get longer
            if longerChance < 0: longerChance = 0
    return newSyllable
