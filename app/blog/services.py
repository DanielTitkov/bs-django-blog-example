from typing import Optional

import re
from unidecode import unidecode
from sklearn.feature_extraction.text import CountVectorizer

from .models import Post, Comment


def update_post_trigrams(post_id: int) -> Optional[Post]:
    post = Post.objects.filter(pk=post_id).first()
    if not post:
        return None

    post.trigrams = " ".join(_get_trigrams(post.body))
    post.save()
    return post


def update_comment_trigrams(comment_id: int) -> Optional[Comment]:
    comment = Post.objects.filter(pk=comment_id).first()
    if not comment:
        return None

    comment.trigrams = " ".join(_get_trigrams(comment.body))
    comment.save()
    return comment


def _cleanse_text(text):
    return unidecode(re.sub('[\W\d\s]', '', text.lower()))
    

def _get_trigrams(text):
    cleaned_text = _cleanse_text(text)

    vectorizer = CountVectorizer(
        ngram_range=(3,3),
        lowercase=True,
        analyzer = 'char',
    )

    vectorizer.fit_transform([cleaned_text])
    return vectorizer.get_feature_names()[0:6]