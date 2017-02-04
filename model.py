import peewee as pw
from datetime import datetime
import numpy as np
import algorithm

db = pw.SqliteExtDatabase('articles.db')

class NumpyArrayField(pw.Field):
    db_field = 'blob'
    def db_value(self, val):
        val.tobytes()
    def python_value(self, val):
        np.fromstring(val)
class TagField(pw.Field):
    db_field = 'varchar'
    def db_value(self, val):
        ','.join(val)
    def python_value(self, val):
        val.split(',')

class Article(pw.Model):
    class Meta:
        database = db

    id = pw.CharField(unique = True)
    title = pw.CharField()
    body = pw.TextField()
    tags = TagField()
    keywords = pw.TextField
    n_bow = NumpyArrayField(default = np.zeros(0))
    created_at = pw.DateTimeField(default = datetime.now)

    @classmethod
    def word2vec_corpus(cls):
        import jieba
        corpora = []

        for article in cls.select():
            corpora.append(
                "\n".join([
                    article.title,
                    article.body,
                    "\n".join(article.tags)
                ])
            )

        return "\n".join(corpora)

    def compute_bow(self):
        self.keywords = self.tags + \
                        algorithm.tfidf(self.title)
        self.n_bow = self.normalized_bow(self.keywords)


