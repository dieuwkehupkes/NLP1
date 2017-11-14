class Vocab:
    def __init__(self, name, pad=0, sos=1, eos=2, unk=3):
        self.name = name
        self.trimmed = False
        self.word2index = {}
        self.word2count = {}
        self.index2word = {pad:"PAD", sos:"SOS", eos:"EOS", unk:"<unk>"}
        self.pad = pad
        self.sos = sos
        self.eos = eos
        self.unk = unk
        self.n_words = 4 # Count default tokens

    def index_sentence(self, sentence):
        for word in sentence.split(' '):
            self.index_word(word)

    def index_word(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

    def indexes_from_sentence(self, sentence):
        indices = [self.word2index[word] if word in self.word2index else 3 for word in sentence] + [self.eos]
        return indices

    def pad_seq(self, seq, length):
        seq += [self.pad for i in xrange(length - len(seq))]

        return seq

    # Remove words below a certain count threshold
    def trim(self, min_count):
        if self.trimmed: return
        self.trimmed = True
        
        keep_words = []
        
        for k, v in self.word2count.items():
            if v >= min_count:
                keep_words.append(k)

        print('keep_words %s / %s = %.4f' % (
            len(keep_words), len(self.word2index), float(len(keep_words)) / len(self.word2index)
        ))

        # Reinitialize dictionaries
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "PAD", 1: "SOS", 2: "EOS"}
        self.n_words = 3 # Count default tokens

        for word in keep_words:
            self.index_word(word)
