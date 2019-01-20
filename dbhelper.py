from dbmodel import User, Category, Item, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from pprint import pprint


class DBHelper(object):
    engine = create_engine('sqlite:///catalog.db')
    Base.metadata.bind = engine
    __DBSession = sessionmaker(bind=engine)

    def __init__(self):
        self.session = DBHelper.__DBSession()

    def create_item(self, name, description, category_name, username):
        current_user = self.session.query(User).filter_by(name=username).one()
        if not self.category_exists(category_name):
            self.create_category(category_name)

        cat = self.session.query(Category).filter_by(name=category_name.title()).one()
        if not self.item_exists(name, cat.id):
            new_item = Item(name=name, desc=description, user_id=current_user.id, category_id=cat.id)
            self.session.add(new_item)
            self.session.commit()
            return new_item

    def update_item(self, item_to_update, new_name=None, new_category=None, new_desc=None):
        if new_name:
            item_to_update.name = new_name
        if new_category:
            item_to_update.category = new_category
        if new_desc:
            item_to_update.desc = new_desc
        self.session.commit()

    def item_exists(self, item_name, category_id=None, category_name=None):
        item_category = self.get_category(category_id=category_id, category_name=category_name)
        if not item_category:
            return False

        try:
            self.session.query(Item).filter_by(category_id=item_category.id).filter_by(name=item_name).one()
            return True
        except NoResultFound:
            return False

    def get_item(self, item_name, item_category_name=None, item_category_id=None):
        if self.item_exists(item_name, category_id=item_category_id, category_name=item_category_name):
            item_category = self.get_category(category_name=item_category_name, category_id=item_category_id)
            return self.session.query(Item).filter_by(name=item_name, category=item_category).one()
        return None

    def category_exists(self, category_name=None, category_id=None):
        if category_name:
            try:
                self.session.query(Category).filter_by(name=category_name.title()).one()
                return True
            except NoResultFound:
                return False
        elif category_id:
            try:
                self.session.query(Category).filter_by(id=category_id).one()
                return True
            except NoResultFound:
                return False
        else:
            return False

    def create_category(self, category_name):
        new_category = Category(name=category_name.title())
        self.session.add(new_category)
        self.session.commit()
        return new_category

    def create_user(self, username):
        if not self.user_exists(username):
            new_user = User(name=username)
            self.session.add(new_user)
            self.session.commit()
        return self.session.query(User).filter_by(name=username).one()

    def get_user(self, user_id=None, username=None):
        if user_id:
            try:
                return self.session.query(User).filter_by(id=user_id).one()
            except NoResultFound:
                return None
        elif username:
            try:
                return self.session.query(User).filter_by(name=username).one()
            except NoResultFound:
                return None
        else:
            return None

    def user_exists(self, username):
        try:
            self.session.query(User).filter_by(name=username).one()
            return True
        except NoResultFound:
            return False

    def get_category(self, category_name=None, category_id=None):
        if self.category_exists(category_name=category_name, category_id=category_id):
            if category_name:
                return self.session.query(Category).filter_by(name=category_name.title()).one()
            else:
                return self.session.query(Category).filter_by(id=category_id).one()

    def delete_item(self, item_obj):
        self.session.delete(item_obj)
        self.session.commit()


if __name__ == "__main__":
    default_user = 'default_user'
    helper = DBHelper()
    helper.create_user(default_user)
    pprint([user.serialize for user in helper.session.query(User).all()])

    helper.create_item('default item', 'something to test with', 'default', default_user)
    helper.create_item('another default', 'something with a later modified date', 'default', default_user)

    pprint([category.serialize for category in helper.session.query(Category).all()])
    pprint([item.serialize for item in helper.session.query(Item).all()])

    helper.update_item(helper.get_item(item_name='default item', item_category_name='default'), new_desc='this got updated!!!')

