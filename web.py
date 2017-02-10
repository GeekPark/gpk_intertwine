import bottle
from bottle import route, run, request
import algorithm, model
from model import Article

# request = bottle.Request()

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

@route('/train')
@error_handled
def retrain():
    corpus = Article.word2vec_corpus()
    algorithm.retrain_word2vec(corpus)

    for article in Article.select():
        article.compute_bow()
        article.save()
    # model.update_bows

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


@route('/similar_to/<id>')
@error_handled
def similar_to(id):
    count = request.query.count and int(request.query.count) or 10

    q_article = Article.get(Article.id == id)
    assert(isinstance(q_article, Article))

    ids, bows = Article.all_id_with_bow()
    top = algorithm.similar_to(
        q_article.n_bow,
        bows,
        ids,
        count = count
    )
    l = list(top)
    return l


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


run(host = 'localhost', port = '32298', reloader=True)

