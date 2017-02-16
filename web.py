import bottle
from bottle import route, run, request
import algorithm, model
from model import Article
import numpy as np
from scipy.sparse import vstack

# request = bottle.Request()

TOP_COUNT = 10

def Error(reason, **others):
    return dict(ok=False, error=reason, **others)
def Result(object=None):
    if object is None:
        return dict(ok=True)
    else:
        return dict(ok=True, result=object)

def error_handled(foo):
    def wrapper(*args, **kwargs):
        try:
            return Result(foo(*args, **kwargs))
        except Article.DoesNotExist as e:
            import traceback
            traceback.print_exc()
            return Error('Record not found')
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Error(
                str(e),
                cls=str(type(e)),
            )
    return wrapper

@route('/train/word2vec')
@error_handled
def train_word2vec():
    corpus = Article.word2vec_corpus()
    algorithm.retrain_word2vec(corpus)

@route('/train/bow')
@error_handled
def train_bow():
    for article in Article.select():
        article.compute_bow()
        article.save()

@route('/train/full_relation')
@error_handled
def train_full_relation():
    ids = [a.id for a in Article.select()]
    bows = vstack([a.n_bow for a in Article.select()])

    rel = algorithm.full_relation(bows, ids, TOP_COUNT)
    for (_id, vec) in zip(ids, rel):
        Article\
            .update(related_articles = map(np.asscalar, vec))\
            .where(Article.id == _id)\
            .execute()


@route('/index/add', method = 'POST')
@error_handled
def index_insert():
    fields = request.json['article']

    article = Article()
    article.id = fields['id']
    article.title = fields['title']
    article.body  = fields['body']
    article.tags  = fields['tags']
    if algorithm.trained():
        article.compute_bow()
    article.save()

@route('/index/update/<id>', method = 'POST')
@error_handled
def index_update(id):
    fields = request.json['article']

    article = Article.get(Article.id == id)

    article.id = fields['id']
    article.title = fields['title']
    article.body  = fields['body']
    article.tags  = fields['tags']
    if algorithm.trained():
        article.compute_bow()
    article.save()

@route('/index/<id>', method = 'DELETE')
@error_handled
def index_delete(id):
    article = Article.get(Article.id == id)
    article.delete_instance()

@route('/index', method = 'DELETE')
@error_handled
def index_purge():
    Article.drop_table()
    Article.create_table()

@route('/related_to/<id>')
@error_handled
def related_to(id):
    q_article = Article.get(Article.id == id)
    assert(isinstance(q_article, Article))

    rel = q_article.related_articles
    if rel and len(rel) >= 0:
        return list(rel)

    ids, bows = Article.all_id_with_bow()
    top = algorithm.related_to(
        q_article.n_bow,
        bows,
        ids,
        count = TOP_COUNT
    )
    q_article.related_articles = [t for t in top]
    q_article.save()

    return related_to(id)



@route('/inspect/article/<id>')
@error_handled
def inspect_article(id):
    article = Article.get(Article.id == id)
    return article.to_dict()

@route('/inspect/meta')
@error_handled
def inspect_meta():
    return {
        **algorithm.meta(),
        **model.meta()
    }


run(host = 'localhost', port = '32298')

