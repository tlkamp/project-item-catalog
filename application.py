import flask
from dbmodel import Item, Category
from dbhelper import DBHelper
from requests_oauthlib import OAuth2Session
import json
import flask_login

app = flask.Flask(__name__)
login_manager = flask_login.LoginManager(app)
login_manager.login_view = 'catalog'

with open('client_secrets.json') as f:
    jsondata = json.load(f)
    __client_secret = jsondata['client_secret']
    __client_id = jsondata['client_id']

__authorization_uri = 'https://github.com/login/oauth/authorize'
__token_uri = 'https://github.com/login/oauth/access_token'
__gh_api_uri = 'https://api.github.com'


@login_manager.user_loader
def load_user(userid):
    helper = DBHelper()
    return helper.get_user(user_id=userid)


# login stuff
# Followed example from: https://requests-oauthlib.readthedocs.io/en/latest/examples/real_world_example.html
@app.route('/login')
def login():
    github = OAuth2Session(__client_id)
    auth_uri, state = github.authorization_url(__authorization_uri)
    flask.session['state'] = state
    return flask.redirect(auth_uri)


@app.route('/authcallback', methods=['GET'])
def auth_callback():
    helper = DBHelper()
    if not flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('catalog'))
    github = OAuth2Session(__client_id, state=flask.session['state'])
    token = github.fetch_token(__token_uri, client_secret=__client_secret, authorization_response=flask.request.url)
    gh_username = github.get(__gh_api_uri + '/user').json()['login']
    # create_user checks to see if the users exists before creating, so it's safe to always call this.
    user = helper.create_user(gh_username)
    flask_login.login_user(user, True)
    flask.session['oauth_token'] = token
    return flask.redirect(flask.url_for('.catalog'))


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('.catalog'))


# Renderable routes
@app.route('/', methods=['GET'])
@app.route('/catalog', methods=['GET'])
def catalog():
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


@app.route('/catalog/<string:categoryname>/<string:itemname>/')
def show_specific_item_page(categoryname, itemname):
    helper = DBHelper()
    item = helper.get_item(itemname, item_category_name=categoryname)
    if item:
        return flask.render_template('item.html', item=item)
    else:
        flask.abort(404)


@app.route('/catalog/<string:categoryname>/<string:itemname>/edit/')
@flask_login.login_required
def edit_item(categoryname, itemname):
    helper = DBHelper()
    item = helper.get_item(itemname, item_category_name=categoryname)
    if item:
        return flask.render_template('edit-item.html', item=item)
    else:
        flask.abort(404)


@app.route('/catalog/update_item/<int:itemid>/', methods=['PUT', 'PATCH', 'POST'])
@flask_login.login_required
def update_item(itemid):
    # Get everything out of the form
    helper = DBHelper()
    item = helper.session.query(Item).filter_by(id=itemid).one()
    new_name = flask.request.form.get('item-name', item.name)
    new_desc = flask.request.form.get('item-description', item.desc)
    new_category = flask.request.form.get('item-category', item.category.name)
    updated = helper.update_item(item.id, new_name=new_name, new_category=new_category, new_desc=new_desc)
    return flask.redirect(
        flask.url_for('show_specific_item_page', categoryname=updated.category.name, itemname=updated.name)
    )


@app.route('/catalog/add_item/', methods=['GET'])
@flask_login.login_required
def add_item():
    return flask.render_template('add-item.html')


@app.route('/catalog/create/', methods=['POST'])
@flask_login.login_required
def create():
    helper = DBHelper()
    name = flask.request.form['item-name']
    category_name = flask.request.form['item-category']
    description = flask.request.form['item-description']
    helper.create_item(name, description, category_name, flask_login.current_user.name)
    return flask.redirect(flask.url_for('show_specific_item_page', categoryname=category_name, itemname=name))


@app.route('/catalog/<string:categoryname>/<string:itemname>/delete/')
@flask_login.login_required
def delete_item(categoryname, itemname):
    helper = DBHelper()
    item = helper.get_item(itemname, item_category_name=categoryname)
    # TODO: Make sure current logged in user owns the item
    if item:
        helper.delete_item(item)
        return flask.redirect(flask.url_for('show_specific_categoryname', categoryname=categoryname))
    else:
        flask.abort(500)


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
    import os

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.secret_key = os.urandom(32)
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
