'''
Simple class to learn a Brill's Tagger
'''

import sys
import time

def train(corpus):
    '''
    learns rules as per Brill's tagger from the taggerd input corpora
    '''
    _, word_tag, corpus_tags, corpus_words = process_corpus(corpus)
    applicable_tags = set()
    for a_tag in word_tag.values():
        if len(a_tag) > 1:
            for k in a_tag.keys():
                applicable_tags.add(k)
    applicable_tags = filter_tags(applicable_tags)
    # get the most probable tag for a word
    word_most_probable_tag = {k : max(val, key=val.get) for k, val in word_tag.items()}
    # save unigram model of model probable tags in a file
    with open('word_best_tag.txt', 'w') as file:
        for k, val in word_most_probable_tag.items():
            file.write('%s\t%s\n' % (k, val))
    transform_queue = tbl(corpus_words, corpus_tags, word_most_probable_tag, applicable_tags)
    return transform_queue

def filter_tags(tags):
    '''
    removes those tags which are not applicable for rules
    '''
    to_remove = ('$', '#', '\'', '\'\'', '\"', '(', ')', ',', '.', ':', 'TO', 'SYM')
    return tags.difference(to_remove)

def tbl(corpus_words, corpus, word_most_probable_tag, tags):
    '''
    finds the best transformation rules for the corpus
    '''
    queue = []
    retagged_corpus = retag_best_tags(corpus_words, word_most_probable_tag)
    itr = 0
    for _ in range(20):
        itr += 1
        print('iteration', itr)
        # best_transform = get_best_transform(corpus, retagged_corpus, tags)
        best_transform = get_best_transform(corpus, retagged_corpus, tags)
        apply_transform(best_transform[1:], retagged_corpus)
        queue.append(best_transform)
    queue.sort(key=lambda x: x[0], reverse=True)
    # print(queue)
    # save the rules in a file
    with open('rules.txt', 'w') as file:
        file.write('%s\t%s\t%s\t%s\n' % ('From', 'To', 'Prev', 'Score'))
        for rule in queue:
            file.write('%s\t%s\t%s\t%d\n' % (rule[1], rule[2], rule[3], rule[0]))

    return queue

def apply_transform(transform, corpus_tags):
    '''
    retag the corpus with the best rule
    '''
    for pos in range(1, len(corpus_tags)):
        if corpus_tags[pos] == transform[0] and corpus_tags[pos-1] == transform[2]:
            corpus_tags[pos] = transform[1]

def get_best_transform(correct_tag, current_tag, tags):
    '''
    get the best rule
    '''
    score = 0
    best_rule = None
    for from_tag in tags:
        for to_tag in tags:
            transforms = {}
            if from_tag == to_tag:
                continue
            # for correct_line, current_line in zip(corpus, retagged_corpus):
            # for correct_line, current_line in correct_current:
            #     correct_words = correct_line.split()
            #     current_words = current_line.split()
            for pos in range(1, len(correct_tag)):
                # _, correct_tag = correct_words[pos].split('_')
                # _, current_tag = current_words[pos].split('_')
                # _, prev_tag = current_words[pos-1].split('_')
                if correct_tag[pos] == to_tag and current_tag[pos] == from_tag:
                    transforms[current_tag[pos-1]] = transforms.get(current_tag[pos-1], 0) + 1
                elif correct_tag[pos] == from_tag and current_tag[pos] == from_tag:
                    transforms[current_tag[pos-1]] = transforms.get(current_tag[pos-1], 0) - 1
            if transforms:
                best_z = max(transforms, key=transforms.get)
                best_instance = (transforms[best_z], from_tag, to_tag, best_z)
                if best_instance[0] > score:
                    best_rule = best_instance
                    score = best_instance[0]
    return best_rule

def retag_best_tags(corpus, word_most_probable_tag):
    '''
    retag the corpus with the most probable tags
    '''
    retagged_corpus = []
    for tagged_word in corpus:
        word, _ = tagged_word.split('_')
        retagged_corpus.append(word_most_probable_tag.get(word))
    return retagged_corpus

def process_corpus(file):
    '''
    reads the corpus file and finds the most probable tags
    '''
    tags = set()
    word_tag = {}
    corpus_tags = []
    corpus_words = []
    with open(file, 'r') as corpus:
        lines = corpus.read().splitlines()
    for line in lines:
        # corpus_sentences.append(line)
        for tagged_word in line.split():
            corpus_words.append(tagged_word)
            word, tag = tagged_word.split('_')
            corpus_tags.append(tag)
            tags.add(tag)
            if word in word_tag:
                temp = word_tag.get(word)
                if tag in temp:
                    temp[tag] = temp.get(tag) + 1
                else:
                    temp[tag] = 1
            else:
                word_tag[word] = {tag: 1}
    return tags, word_tag, corpus_tags, corpus_words

def main():
    '''
    accepts the corpus as a runtime argument
    '''
    corpus = sys.argv[1]
    start = time.time()
    train(corpus)
    print('time', time.time() - start)

if __name__ == '__main__':
    main()
