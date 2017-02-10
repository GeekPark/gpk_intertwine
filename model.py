from playhouse.shortcuts import model_to_dict
import peewee as pw
from datetime import datetime
import numpy as np
import algorithm

db = pw.SqliteDatabase('data/articles.db')

class NumpyArrayField(pw.Field):
    db_field = 'blob'
    def db_value(self, val):
        return val is not None and val.tobytes()
    def python_value(self, val):
        return val and np.fromstring(val)
class TagField(pw.Field):
    db_field = 'varchar'
    def db_value(self, val):
        return val and ','.join(val)
    def python_value(self, val):
        return val and val.split(',')

class Article(pw.Model):
    class Meta:
        database = db

    _id = pw.PrimaryKeyField()
    id = pw.IntegerField(unique = True)
    title = pw.CharField(null = True)
    body = pw.TextField(null = True)
    tags = TagField(null = True)
    keywords = pw.TextField(null = True)
    n_bow = NumpyArrayField(default = np.zeros(algorithm.N), null = True)
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
        self.n_bow = bow


    def to_dict(self):
        return dict(
            _id = self._id,
            id = self.id,
            title = self.title,
            body = self.body,
            tags = self.tags,
            keywords = self.keywords,
            n_bow = list(self.n_bow),
            created_at = str(self.created_at)
        )


    @classmethod
    def all_id_with_bow(cls):
        pairs = list(cls.select(Article.id, Article.n_bow))
        ids    = [p.id    for p in pairs]
        n_bows = [p.n_bow for p in pairs]
        return ids, n_bows


def meta():
    return dict(
        article_count = Article.select().count()
    )



db.create_tables([Article], safe = True)
