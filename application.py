import flask
from dbmodel import Item, Category
from dbhelper import DBHelper

app = flask.Flask(__name__)


@app.route('/')
@app.route('/catalog')
def default():
    helper = DBHelper()
    categories = helper.session.query(Category).all()
    items = helper.session.query(Item).order_by(Item.last_updated.desc()).all()
    return flask.render_template('index.html', categories=categories, items=items)


@app.route('/catalog/items/all')
def show_all_items():
    helper = DBHelper()
    items = helper.session.query(Item).all()
    return flask.jsonify(items=[item.serialize for item in items])


@app.route('/catalog/items/<int:itemid>')
def show_specific_item(itemid):
    helper = DBHelper()
    item = helper.session.query(Item).filter_by(id=itemid).one()
    return flask.jsonify(item=item.serialize)


@app.route('/catalog/categories/all')
def show_all_categories():
    helper = DBHelper()
    categories = helper.session.query(Category).all()
    return flask.jsonify(categories=[category.serialize for category in categories])


@app.route('/catalog/categories/<int:categoryid>')
def show_specific_category(categoryid):
    helper = DBHelper()
    category = helper.session.query(Category).filter_by(id=categoryid).one()
    return flask.jsonify(category=category.serialize)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=3000)