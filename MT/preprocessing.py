import torch
import io
import re
import unicodedata
from language import Vocab
from itertools import izip


# Turn a Unicode string to plain ASCII, thanks to http://stackoverflow.com/a/518232/2809427
def unicode_to_ascii(s):
    '''
    The files are all in Unicode, to simplify we will turn
    Unicode characters to ASCII, make everything lowercase,
    and trim most punctuation.
    '''
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

# Lowercase, trim, and remove non-letter characters
def normalise(s):
    s = unicode_to_ascii(s.lower().strip())
    s = re.sub(r"([,.!?])", r" \1 ", s)
    s = re.sub(r"[^a-zA-Z,.!?]+", r" ", s)
    s = re.sub(r"\s+", r" ", s).strip()
    return s

# create dictionaries and sentence pairs
def prepare_data(prefix, lang1_name, lang2_name, min_count):
    input_lang, output_lang, pairs = read_input(prefix, lang1_name, lang2_name)
    print("Read %d sentence pairs" % len(pairs))
    
    print("Indexing words...")
    for pair in pairs:
        input_lang.index_sentence(pair[0])
        output_lang.index_sentence(pair[1])

    print('Indexed %d words in input language, %d words in output' % (input_lang.n_words, output_lang.n_words))

    input_lang.trim(min_count)
    output_lang.trim(min_count)

    # trim dataset, replace low freq words with unknown
    trimmed_pairs = []

    for pair in pairs:
	input_sentence = pair[0]
	output_sentence = pair[1]
	
	# TODO I changed this! test
	# input_sentence = [word if word in input_lang.word2index else '<unk>' for word in input_sentence.split(' ')]
	# output_sentence = [word if word in output_lang.word2index else '<unk>' for word in output_sentence.split(' ')]
	input_sentence = input_lang.indexes_from_sentence(input_sentence.split(' '))
	output_sentence = output_lang.indexes_from_sentence(output_sentence.split(' '))
	trimmed_pairs.append([input_sentence, output_sentence])

    return input_lang, output_lang, trimmed_pairs

# Read input lines and put into pairs
def read_input(prefix, lang1, lang2):
    print("Reading lines...")

    # Read the file and split into lines
    source_lines = io.open(prefix+lang1, 'r')
    target_lines = io.open(prefix+lang2, 'r')

    # create output
    pairs = []

    for source, target in izip(source_lines, target_lines):
        if source[0] == '<':
            assert target[0] == '<'
            continue

        else:
            source = normalise(source.strip())
            target = normalise(target.strip())
            pairs.append([source, target])

    input_lang = Vocab(lang1)
    output_lang = Vocab(lang2)

    return input_lang, output_lang, pairs

if __name__ == '__main__':
    vocab_source, vocab_target, data = prepare_data('data/train.tags.en-nl.', 'en', 'nl', 3)
    
    # save data
    savedata = {'vocab_source': vocab_source,
                'vocab_target': vocab_target,
                 'train_pairs': data}
    torch.save(savedata, 'models/data_en_nl.pt')


