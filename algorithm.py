import numpy as np
from gensim.models import Word2Vec
import jieba
import os

# num of features
N = 100


def retrain_word2vec(corpus):
    lines = corpus.splitlines()

    model = Word2Vec([jieba.lcut(l) for l in lines if len(l) >= 5])
    model.init_sims(replace = True)
    model.save('data/word2vec.model')

    hasattr(word2vec_model, 'm')  and delattr(word2vec_model, 'm')
    hasattr(word2vec_matrix, 'm') and delattr(word2vec_matrix, 'm')


def word2vec_model():
    """
    :rtype: Word2Vec
    """
    if hasattr(word2vec_model, 'm'):
        return word2vec_model.m

    if os.path.isfile('data/word2vec.model'):
        word2vec_model.m = Word2Vec.load('data/word2vec.model')
        return word2vec_model()

    word2vec_model.m = Word2Vec()
    return word2vec_model()


def word2vec_matrix():
    """
    :rtype: numpy.array
    """
    if hasattr(word2vec_matrix, 'm'):
        return word2vec_matrix.m

    def normalize_matrix(mat):
        if len(mat.shape) != 2:
            return mat
        norm = np.linalg.norm(mat, axis=1, keepdims=True)
        zero_vec = np.all(mat == 0, axis=1, keepdims=True)
        norm[zero_vec] = 1
        return mat / norm

    word2vec_matrix.m = normalize_matrix(word2vec_model().syn0)
    return word2vec_matrix()


def compute_bow(title, tags):
    m = word2vec_model()

    def tfidf(sentence, top=5):
        from jieba.analyse import extract_tags
        tags = extract_tags(sentence, topK=top, withWeight=True)
        tags = [t for t in tags if t[0] in word2vec_model().vocab]

        words = [t[0] for t in tags]
        weights = [t[1] for t in tags]

        return words, weights

    def bag_of_words(words, weights):
        indices = [m.vocab[w].index for w in words]

        vocab_count = m.syn0.shape[0]  # == len(m.vocab)
        vec = np.zeros(vocab_count)

        vec[indices] = weights
        return vec

    title_words, title_weights = tfidf(title, top=10)
    bow = bag_of_words(title_words, title_weights)
    bow = bow / (bow.max() if bow.max() != 0 else 1.0)

    tag_indices = [m.vocab[w].index for w in tags if w in m.vocab]
    bow[tag_indices] = 0.9
    bow = bow / (np.linalg.norm(bow) if np.linalg.norm(bow) != 0 else 1.0)

    return bow.reshape(1, -1)


def ssi_similarity(q, d):
    """
    n0,n1: num of docs, typically n0 = 1
    m: word2vec model (N x D)
    q: normalized b-o-w for doc q (n0 x N)
    d: normalized b-o-w for doc d (n1 x N)

    ssi is calc-ed by f(q,d) = q . (m . m' + I) . d'
                             = q . m . m' . d' + q . d'
    """

    m = word2vec_matrix()

    if id(q) == id(d):
        t = q.dot(m)
        return t.dot(t.T) + q.dot(d.T)

    return np.dot(q.dot(m), d.dot(m).T) + q.dot(d.T)

    # orthogonal word mode
    #return q.dot(d.T)

def full_relation(q, ids, count):
    ids = np.array(ids)
    sim = ssi_similarity(q, q)
    order = (-sim).argsort()[:, :count]

    return ids[order]

def related_to(q, d, d_id, count):
    d_id = np.array(d_id)

    sim = ssi_similarity(q, d).ravel()
    order = (-sim).argsort()[:, :count]

    return list(map(np.asscalar, d_id[order.A1]))


def trained():
    return len(word2vec_model().vocab) > 0


def meta():
    m = word2vec_model()
    result = dict(
        trained          = trained(),
        vocabulary_count = len(m.vocab),
        feature_count    = N
    )
    if trained():
        result.update(
            corpus_count = m.corpus_count,
            train_time   = m.total_train_time,
            train_count  = m.train_count
        )

    return result


