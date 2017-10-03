'''
Demonstartion of Bigram and sentence prediction without smoothin,
with add one smoothing and good Turing smoothing
'''

import sys
from collections import Counter

def load_corpus_data(data):
    '''
    loads the data file and generates corpus statistics like
    unigrams, unigram_count, bigrams, bigram_count_unsmoothed, bigram_count_add1
    Also generates histograms for the bigram counts and stores them in a file
    '''
    unigrams, bigrams = process_file(data)
    unigram_count = Counter(unigrams)
    vocab_size = len(unigram_count)
    corpus_bigram_count = Counter(bigrams)
    # store the sorpus stats in a file
    # write_to_file(unigram_count, 'corpus_stats.txt')
    with open('corpus_stats.txt', 'w') as file:
        for k, val in unigram_count.items():
            file.write('%s\t%d\n' % (k, val))
    # stroe unsmoothed bigram count and probability stored as bigram: (count, probablity)
    # store add1 smoothed bigram count for the bigrams in the corpus
    # bigram: (count, probablity) bigram is word2|word1
    bigram_unsmoothed = {}
    bigram_add1 = {}
    bigram_histogram = {}
    bigram_good_turing = {}
    for key, value in corpus_bigram_count.items():
        prev = unigram_count.get(key[0])
        bigram_unsmoothed[key] = (value, (value / prev))
        # calculate reconstitued counts
        r_count = (value + 1) * prev / (prev + vocab_size)
        bigram_add1[key] = (r_count, (r_count / prev))
    for val in corpus_bigram_count.values():
        bigram_histogram[val] = bigram_histogram.get(val, 0) + 1
    total_bigrams = sum(corpus_bigram_count.values())
    bigram_good_turing[0] = (0, bigram_histogram[1] / total_bigrams)
    # now do good turing store c* and probablity as c: c* probablity
    for c in range(1, max(bigram_histogram) + 1):
        if c not in bigram_histogram:
            temp = 0
        else:
            temp = (c + 1) * bigram_histogram.get(c+1, 0) / bigram_histogram.get(c)
        bigram_good_turing[c] = (temp, temp / total_bigrams)
    # store smooth add1 and Good-Turing info a file
    write_to_file(bigram_unsmoothed, 'corpus_bigram.txt')
    write_to_file(bigram_add1, 'corpus_bigram_add1.txt')
    with open('corpus_good_turing.txt', 'w') as file:
        # the first line is for unseen bigrams
        _gt = bigram_good_turing[0]
        file.write('%s\t%f\t%f\n' % ('.*', _gt[0], _gt[1]))
        for k, val in corpus_bigram_count.items():
            _gt = bigram_good_turing[val]
            file.write('%s\t%f\t%f\n' % (k[0] + ' ' + k[1], _gt[0], _gt[1]))
    return

def process_file(file):
    '''
    read the file and returns the unigrams and the bigrams in the file
    '''
    with open(file, 'r') as corpus:
        tokens = corpus.read()
    tokens_list = tokens.split()
    unigrams = [word for word in tokens_list]
    bigrams = [(word, word1) for word, word1 in zip(tokens_list, tokens_list[1:])]
    return unigrams, bigrams

def write_to_file(dict_obj, file):
    '''
    write a dict to a file
    '''
    with open(file, 'w') as file:
        for k, val in dict_obj.items():
            file.write('%s\t%f\t%f\n' % (k[0] + ' ' + k[1], val[0], val[1]))

def main():
    '''
    main functionality
    '''
    # _, unigram_count, _, bigram_unsmoothed, bigram_add1 = load_corpus_data(sys.argv[1])
    load_corpus_data(sys.argv[1])

if __name__ == '__main__':
    main()
