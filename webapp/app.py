# -*- coding: utf-8 -*-
from __future__ import absolute_import
from flask import Flask, render_template
from flask.ext.misaka import Misaka
# from unicodedata import normalize
from slugify import slugify

from flask_flatpages import FlatPages
from flask_frozen import Freezer


# Initialize the Flask application
app = Flask(__name__)

Misaka(app)
app.config.from_pyfile('settings.py')
pages = FlatPages(app)
freezer = Freezer(app)

# quick function to sort posts.
def sort_my_posts(posts):
    """Sort pages by date"""
    return sorted(posts, reverse=True, key=lambda page: page.meta['date'])

def rm_char(txt, codif='utf-8'):
    """Replace Pt_BR character to ASCII"""
    return normalize('NFKD', txt.decode(codif)).encode('ascii', 'ignore')

@app.route('/')
def index():
    # get all files in pages/blog, including sub-directories
    posts = [page for page in pages if
             page.path.startswith('blog') if 'date' in page.meta]

    for post in posts:
        post.meta['stitle'] = slugify(post.meta['title'].replace(' ', '_'))
        post.meta['htitle'] = '#' + post.meta['stitle']
        post.meta['img_address'] = '../static/img/' + post.meta['pic']
    #  Sort pages by date
    sorted_posts = sort_my_posts(posts)
    # only post the latest 3 entries.
    home_posts = sorted_posts[:6]

    return render_template('index.html', posts=home_posts)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("8000"),
        debug=True
    )
