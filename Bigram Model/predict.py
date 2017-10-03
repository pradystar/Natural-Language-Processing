'''
Uses the corpus data contained in the files mentioned below and computes
probability of the sentence

bigram_unsmoothed.txt
bigram_add1.txt
'''

import sys
import csv

def predict_gt(sentence_bigram):
    '''
    Predict sentence using Good-Turing
    '''
    prob = 1
    with open('sentence_bigrams_good_turing.txt', 'w') as file1:
        for (word1, word2) in sentence_bigram:
            with open('corpus_good_turing.txt', 'r') as bigrams:
                reader = csv.reader(bigrams, delimiter='\t')
                # this the probabilty for unseen bigrams
                temp_row = next(reader)
                temp = float(temp_row[2])
                count = float(temp_row[1])
                for row in reader:
                    if row[0] == word1 + ' ' + word2:
                        temp = float(row[2])
                        count = float(row[1])
                        break
            file1.write(('%s\t%s\t%s\n') % (word1 + ' ' + word2, count, temp))
            prob *= temp
    return prob

def predict_smooth(sentence_bigram, stats):
    '''
    Predict sentence using add1 smoothing
    '''
    prob = 1
    vocab_size = len(stats)
    with open('sentence_bigrams_add1.txt', 'w') as file:
        for (word1, word2) in sentence_bigram:
            temp = 1
            with open('corpus_bigram.txt', 'r') as bigrams:
                reader = csv.reader(bigrams, delimiter='\t')
                found = False
                for row in reader:
                    if row[0] == word1 + ' ' + word2:
                        temp += float(row[1])
                        prev_count = int(stats.get(word1, 0))
                        reconstitued_count = temp * prev_count / (prev_count + vocab_size)
                        bigram_prob = temp / (prev_count + vocab_size)
                        file.write(('%s\t%s\t%s\n') % (row[0], reconstitued_count, bigram_prob))
                        found = True
                        break
                if not found:
                    prev_count = int(stats.get(word1, 0))
                    reconstitued_count = temp * prev_count / (prev_count + vocab_size)
                    bigram_prob = temp / (prev_count + vocab_size)
                    file.write(('%s\t%s\t%s\n') % (
                        word1 + ' ' + word2, reconstitued_count, bigram_prob))
            prob *= temp / (int(stats.get(word1, 0)) + vocab_size)
    return prob

def predict(sentence_bigram):
    '''
    Predict the sentence probability using the provided file
    '''
    prob = 1
    with open('sentence_bigrams.txt', 'w') as file1:
        for (word1, word2) in sentence_bigram:
            temp = 0
            count = 0
            with open('corpus_bigram.txt', 'r') as file:
                reader = csv.reader(file, delimiter='\t')
                for row in reader:
                    if row[0] == word1 + ' ' + word2:
                        count = row[1]
                        temp = row[2]
                        break
            file1.write(('%s\t%s\t%s\n') % (word1 + ' ' + word2, count, temp))
            prob *= float(temp)
    return prob

def main():
    '''
    main functionality
    '''
    # now predict sentence probability
    # import corpus stats
    stats = {}
    with open('corpus_stats.txt', 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            stats[row[0]] = row[1]
    sentence = sys.argv[1:]
    sentence_bigram = [(word, word1) for word, word1 in zip(sentence, sentence[1:])]
    print('sentence is: %s' % (' '.join(sentence)))
    # using unsmoothed count
    prob = predict(sentence_bigram)
    print('Probability using unsmoothed count is ', prob)
    prob = predict_smooth(sentence_bigram, stats)
    print('Probability using add1 smoothing is ', prob)
    prob = predict_gt(sentence_bigram)
    print('Probability using Good-Turing smoothing is ', prob)

if __name__ == '__main__':
    main()
    