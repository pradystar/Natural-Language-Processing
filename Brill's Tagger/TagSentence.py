'''
Tags a sentence based on the rules learnt by Brills Tagger
'''

import sys
import csv

def load_rules():
    '''
    loads the rules in a list arranged by
    the descending priority
    '''
    rules = []
    with open('rules.txt', 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)
        for row in reader:
            rules.append((row[0], row[1], row[2]))
    return rules

def load_best_tags():
    '''
    loads the best tag for the words
    '''
    word_tag = {}
    with open('word_best_tag.txt', 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            word_tag[row[0]] = row[1]
    return word_tag

def tag_with_most_probable(sentence, word_best_tag):
    '''
    tags the sentence with the most probable tag
    '''
    tagged_sentence = []
    for word in sentence.split():
        tagged_sentence.append(word + '_' + word_best_tag.get(word))
    return ' '.join(tagged_sentence)

def tag_with_rules(sentence, rules):
    '''
    tags the sentence tagged with most probable tags based on rules
    '''
    words = sentence.split()
    for pos in range(1, len(words)):
        word, tag = words[pos].split('_')
        _, prev = words[pos-1].split('_')
        for rule in rules:
            if tag == rule[0] and prev == rule[2]:
                words[pos] = word + '_' + rule[1]
                break
    return ' '.join(words)

def error(sentence, gold):
    '''
    find the error compring the tagged sentence with the gold
    '''
    error_rate = 0
    for word_tag, correct_word_tag in zip(sentence.split(), gold.split()):
        _, current_tag = word_tag.split('_')
        _, correct_tag = correct_word_tag.split('_')
        if current_tag != correct_tag:
            error_rate += 1
    return error_rate / len(sentence.split())

def main():
    '''
    main functionality
    '''
    sentence = sys.argv[1]
    gold = ''
    if len(sys.argv) > 2:
        gold = sys.argv[2]
    print('sentence is:', sentence)
    if gold:
        print('gold is:', gold)
    rules = load_rules()
    word_tag = load_best_tags()
    unigram_tag_sentence = tag_with_most_probable(sentence, word_tag)
    print('sentence tagged with unigram model using most probable tag')
    print(unigram_tag_sentence)
    if gold:
        print('error in sentence tagged with unigram model using most probable tag')
        print(error(unigram_tag_sentence, gold))
    brills_tagged = tag_with_rules(unigram_tag_sentence, rules)
    print('sentence tagged with brills rule')
    print(brills_tagged)
    if gold:
        print('error in sentence tagged using Brill\'s tagger')
        print(error(brills_tagged, gold))

if __name__ == '__main__':
    main()
