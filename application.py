import flask
from dbmodel import Item, Category
from dbhelper import DBHelper

app = flask.Flask(__name__)


# Renderable routes
@app.route('/')
@app.route('/catalog')
def default():
    helper = DBHelper()
    categories = helper.session.query(Category).all()
    items = helper.session.query(Item).order_by(Item.last_updated.desc()).all()
    return flask.render_template('index.html', categories=categories, items=items)


@app.route('/catalog/<string:categoryname>/')
def show_specific_categoryname(categoryname):
    helper = DBHelper()
    categories = helper.session.query(Category).all()
    category = helper.get_category(categoryname)
    if category:
        cat_items = helper.session.query(Item).filter_by(category_id=category.id).all()
        return flask.render_template('category.html', categories=categories, category=category, items=cat_items)
    else:
        # If the category doesn't exist, return a 404.
        flask.abort(404)


# Api routes
@app.route('/api/items/all')
def show_all_items():
    helper = DBHelper()
    items = helper.session.query(Item).all()
    return flask.jsonify(items=[item.serialize for item in items])


@app.route('/api/items/<int:itemid>')
def show_specific_item(itemid):
    helper = DBHelper()
    item = helper.session.query(Item).filter_by(id=itemid).one()
    return flask.jsonify(item=item.serialize)


@app.route('/api/categories/all')
def show_all_categories():
    helper = DBHelper()
    categories = helper.session.query(Category).all()
    return flask.jsonify(categories=[category.serialize for category in categories])


@app.route('/api/categories/<int:categoryid>')
def show_specific_category(categoryid):
    helper = DBHelper()
    category = helper.session.query(Category).filter_by(id=categoryid).one()
    return flask.jsonify(category=category.serialize)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
