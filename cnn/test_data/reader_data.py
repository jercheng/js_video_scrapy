from collections import namedtuple
import os
import numpy as np

raw_example = namedtuple('RawExample', 'label entity1 entity2 sentence')
position_pair = namedtuple('PosPair', 'first last')
PAD_WORD = "<pad>"


def maybe_trim_embeddings(vocab_file,
                          pretrain_embed_file,
                          pretrain_words_file,
                          trimed_embed_file):
    if not os.path.exists(trimed_embed_file):
        pretrain_embed, pretrain_words2id = _load_embedding(
            pretrain_embed_file,
            pretrain_words_file)
        word_embed = []
        vocab = _load_vocab(vocab_file)
        for w in vocab:
            if w in pretrain_words2id:
                id = pretrain_words2id[w]
                word_embed.append(pretrain_embed[id])
            else:
                vec = np.random.normal(0, 0.1, [50])
                word_embed.append(vec)
        pad_id = -1
        word_embed[pad_id] = np.zeros([50])

        word_embed = np.asarray(word_embed)
        np.save(trimed_embed_file, word_embed.astype(np.float32))

    word_embed, vocab2id = _load_embedding(trimed_embed_file, vocab_file)
    return word_embed, vocab2id


def _load_vocab(vocab_file):
    # load vocab from file
    vocab = []
    with open(vocab_file) as f:
        for line in f:
            w = line.strip()
            vocab.append(w)

    return vocab


def _load_embedding(embed_file, words_file):
    embed = np.load(embed_file)

    words2id = {}
    words = _load_vocab(words_file)
    for id, w in enumerate(words):
        words2id[w] = id

    return embed, words2id


def maybe_build_vocab(raw_train_data, raw_test_data, vocab_file):
    '''collect words in sentence'''
    if not os.path.exists(vocab_file):
        vocab = set()
        for example in raw_train_data + raw_test_data:
            for w in example.sentence:
                vocab.add(w)

        with open(vocab_file, 'w') as f:
            for w in sorted(list(vocab)):
                f.write('%s\n' % w)
            f.write('%s\n' % PAD_WORD)


def load_raw_data(file_name):
    data = []
    with open(file_name) as f:
        for line in f:
            words = line.strip().split(' ')
            sent = words[5:]
            label = int(words[0])

            entity1 = position_pair(int(words[1]), int(words[2]))
            entity2 = position_pair(int(words[3]), int(words[4]))

            example = raw_example(label, entity1, entity2, sent)
            print(example)
            data.append(example)

    return data


def main():
    train_file = load_raw_data("../data/train.cln")
    test_file = load_raw_data("../data/test.cln")
    maybe_build_vocab(train_file, test_file, "../data/vocab.txt")

    word_embed, vocab2id = maybe_trim_embeddings(
        "../data/vocab.txt",
        "../data/embed50.senna.npy",
        "../data/senna_words.lst",
        "../data/embed50.trim.npy"
    )


if __name__ == '__main__':
    main()
