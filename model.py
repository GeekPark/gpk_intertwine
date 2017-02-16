from playhouse.shortcuts import model_to_dict
import peewee as pw
from datetime import datetime
import numpy as np
import algorithm
from scipy.sparse import csr_matrix
import pickle

db = pw.SqliteDatabase('data/articles.db')

class NumpySparseArrayField(pw.Field):
    db_field = 'blob'

    # input: 1xN matrix, example: [[1,2,3,4,5]]
    def db_value(self, val):
        if val is None: return None
        return pickle.dumps(val)

    def python_value(self, val):
        if val is None: return None
        return pickle.loads(val)

class TagField(pw.Field):
    db_field = 'varchar'
    def db_value(self, val):
        return ','.join(val)
    def python_value(self, val):
        return val and val.split(',')
class IdListField(pw.Field):
    db_field = 'varchar'
    def db_value(self, val):
        if val is None: return None
        return ','.join([str(x) for x in val])

    def python_value(self, val):
        if val is None or len(val) == 0: return None
        return list(map(int, val.split(',')))

class Article(pw.Model):
    class Meta:
        database = db

    _id = pw.PrimaryKeyField()
    id = pw.IntegerField(unique = True, index = True)
    title = pw.CharField(null = True)
    body = pw.TextField(null = True)
    tags = TagField(default = [], null = True)
    keywords = pw.TextField(null = True)
    related_articles = IdListField(default = [], null = True)
    n_bow = NumpySparseArrayField(default = None, null = True)
    created_at = pw.DateTimeField(default = datetime.now)

    @classmethod
    def word2vec_corpus(cls):
        import jieba
        corpora = []

        for article in cls.select():
            corpora.append(
                "\n".join([
                    article.body,
                    article.title,
                    "\n".join(article.tags)
                ])
            )

        return "\n".join(corpora)


    def compute_bow(self):
        bow = algorithm.compute_bow(
            self.title,
            self.tags
        )
        self.n_bow = csr_matrix(bow)


    def to_dict(self):
        return dict(
            _id = self._id,
            id = self.id,
            title = self.title,
            body = self.body,
            tags = self.tags,
            keywords = self.keywords,
            # n_bow = list(self.n_bow),
            related_articles = self.related_articles,
            created_at = str(self.created_at)
        )


    @classmethod
    def all_id_with_bow(cls):
        from scipy.sparse import vstack
        bytes2matrix = lambda b: NumpySparseArrayField.python_value(None, b)
        pairs = list(db.execute_sql('SELECT id, n_bow FROM article'))
        ids    = [p[0]    for p in pairs]
        n_bows = vstack([bytes2matrix(p[1]) for p in pairs])
        return ids, n_bows


def meta():
    return dict(
        article_count = Article.select().count()
    )


def enable_debug():
    import logging
    logger = logging.getLogger('peewee')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())


db.create_tables([Article], safe = True)
