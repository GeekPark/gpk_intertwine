from bottle import route, run
import algorithm
from model import Article

@route('/train')
def retrain():
    Article.select(Article)
    algorithm.retrain()

@route('/index/update/<id>', method = 'POST')
def index_update(id):
    fields = request.json['article']

    try:
        article = Article.get(Article.id == id)
    except Article.DoesNotExist:
        return dict(ok=False, error='Record does not exist')

    article.title = article['title']
    article.body  = article['body']
    article.tags  = article['tags']

    article.compute_bow()
    return dict(ok=True)

@route('/index/<id>', method = 'DELETE')
def index_delete(id):
    try:
        article = Article.get(Article.id == id)
    except Article.DoesNotExist:
        return dict(ok=False, error='Record does not exist')

    article.delete_instance()


@route('/similar_to/<id>')
def similar_to(id):
    count = int(request.query.count) or 10
    algorithm.similar_to(id, count = count)

@route('/inspect/article/<id>')
def inspect_article(id):
    return 0

@route('/inspect/meta')
def inspect_meta():
    return dict(
        article_count = algorithm.article_count(),
        dictionary_size = algorithm.dictionary_size()
    )


run(host = 'localhost', port = '32298')

