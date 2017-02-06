import numpy as np
from gensim.models import Word2Vec
import jieba
import os

# num of features
N = 100

def retrain_word2vec(corpus):
    lines = corpus.splitlines()

    model = Word2Vec([jieba.cut(l) for l in lines if len(l) >= 5])
    model.init_sims(replace = True)
    model.save('word2vec.model')

    delattr(word2vec_model, 'm')
    delattr(word2vec_matrix, 'm')

def word2vec_model():
    """
    :rtype: Word2Vec
    """
    if hasattr(word2vec_model, 'm'):
        return word2vec_model.m

    if os.path.isfile('word2vec.model'):
        word2vec_model.m = Word2Vec.load('word2vec.model')
        return word2vec_model()

    word2vec_model.m = Word2Vec()
    return word2vec_model()

def word2vec_matrix():
    """
    :rtype: numpy.array
    """
    if hasattr(word2vec_matrix, 'm'):
        return word2vec_matrix.m

    word2vec_model.m = normalize_matrix(word2vec_model().syn0)
    return word2vec_matrix()

def tfidf(sentence, topK = 5):
    from jieba.analyse import extract_tags
    return extract_tags(sentence, topK = topK)

# normalize
def normalize_matrix(mat):
    if len(mat.shape) != 2:
        return mat
    norm = np.linalg.norm(mat, axis=1, keepdims=True)
    zero_vec = np.all(mat == 0, axis=1, keepdims=True)
    norm[zero_vec] = 1
    return mat / norm

def normalized_bow(words):
    m = word2vec_model()

    indices = [m.vocab[word].index for word in words if word in m.vocab]
    word_count = m.syn0.shape[0]

    vec = np.zeros(word_count)
    vec[indices] = 1
    vec = normalize_matrix()
    return vec.reshape([1, -1])


def ssi_similarity(m, q, d):
    """
    n0,n1: num of docs, typically n0 = 1
    m: word2vec model (N x D)
    q: normalized b-o-w for doc q (n0 x N)
    d: normalized b-o-w for doc d (n1 x N)

    ssi is calc-ed by f(q,d) = q . (m . m' + I) . d'
                             = q . m . m' . d' + q . d'
    """

    return np.dot(q.dot(m), m.T.dot(d.T)) + q.dot(d.T)

    # orthogonal word mode
    #return q.dot(d.T)

def similar_to(q, d, d_id, count):
    m = word2vec_matrix()
    q, d, d_id = np.array(q), np.array(d), np.array(d_id)

    sim = ssi_similarity(m, q.reshape([1,-1]), d).ravel()
    order = (-sim).argsort()[:count]

    return zip(
        d_id[order],  # id
        sim[order]    # score
    )


def meta():
    trained = len(word2vec_model().vocab) > 0
    return dict(
        trained          = trained,
        vocabulary_count = len(word2vec_model().vocab),
        feature_count    = N,
    )


