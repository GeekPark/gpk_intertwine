import numpy as np
from gensim.models import Word2Vec
import jieba
from model import Article
import os

# num of features
N = 100

def retrain_word2vec():
    corpus = Article.word2vec_corpus()
    lines = corpus.splitlines()

    model = Word2Vec([jieba.cut(l) for l in lines if len(l) >= 5])
    model.init_sims(replace = True)
    model.save('word2vec.model')

def word2vec_model():
    if hasattr(word2vec_model, 'm'):
        return word2vec_model.m
    if os.path.isfile('word2vec.model'):
        word2vec_model.m = Word2Vec.load('word2vec.model')
        return word2vec_model()
    retrain_word2vec()

def retrain():
    retrain_word2vec()
    Article.update()

def upsert(id, title, body, tags):
    article = Article(id = id, title = title, body = body, tags = tags)
    article.keywords = tags + tfidf(title)
    article.n_bow = normalized_bow(article.keywords)
    article.save()


def tfidf(sentence, topK = 5):
    from jieba.analyse import extract_tags
    return extract_tags(sentence, topK = topK)

# normalize
def normalize_matrix(mat):
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


def delete_article(id):
    return 0


def similar_to(id, count):
    return []

def article_count():
    return 0

def dictionary_size():
    return 0

