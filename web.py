import bottle
from bottle import route, run, request
import algorithm, model
from model import Article

# request = bottle.Request()

NotFoundError = dict(ok=False, error='Record not found')
Result = lambda x=None: dict(ok=True, result=x)

@route('/train')
def retrain():
    corpus = Article.word2vec_corpus()
    algorithm.retrain_word2vec(corpus)
    # model.update_bows

@route('/index/add', method = 'POST')
def index_insert():
    print(request)
    print(request.json)

    fields = request.json['article']

    article = Article()
    article.id = fields['id']
    article.title = fields['title']
    article.body  = fields['body']
    article.tags  = fields['tags']
    if algorithm.trained():
        article.compute_bow()
    article.save()

    return Result()

@route('/index/update/<id>', method = 'POST')
def index_update(id):
    fields = request.json['article']

    try:
        article = Article.get(Article.id == id)
    except Article.DoesNotExist:
        return NotFoundError

    article.id = fields['id']
    article.title = fields['title']
    article.body  = fields['body']
    article.tags  = fields['tags']
    if algorithm.trained():
        article.compute_bow()
    article.save()

    return Result()

@route('/index/<id>', method = 'DELETE')
def index_delete(id):
    try:
        article = Article.get(Article.id == id)
    except Article.DoesNotExist:
        return NotFoundError

    article.delete_instance()

    return dict(ok=True)


@route('/similar_to/<id>')
def similar_to(id):
    count = int(request.query.count) or 10

    try:
        q_article = Article.get(Article.id == id)
        assert(isinstance(q_article, Article))
    except Article.DoesNotExist:
        return NotFoundError

    ids, bows = Article.all_id_with_bow()
    top = algorithm.similar_to(
        q_article.n_bow,
        bows,
        ids,
        count = count
    )

    return Result(top)


@route('/inspect/article/<id>')
def inspect_article(id):
    try:
        article = Article.get(Article.id == id)
    except Article.DoesNotExist:
        return NotFoundError

    return Result(article.to_dict())

@route('/inspect/meta')
def inspect_meta():
    return Result({
        **algorithm.meta(),
        **model.meta()
    })


run(host = 'localhost', port = '32298')

