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

    def create_item(self, name, description, category_name, user_email):
        current_user = self.session.query(User).filter_by(email=user_email).one()
        if not self.category_exists(category_name):
            self.create_category(category_name)

        cat = self.session.query(Category).filter_by(name=category_name.title()).one()
        new_item = Item(name=name, desc=description, user_id=current_user.id, category_id=cat.id)
        self.session.add(new_item)
        self.session.commit()

    def category_exists(self, category_name):
        try:
            self.session.query(Category).filter_by(name=category_name.title()).one()
            return True
        except NoResultFound:
            return False

    def create_category(self, category_name):
        new_category = Category(name=category_name.title())
        self.session.add(new_category)
        self.session.commit()

    def create_user(self, username, user_email):
        if not self.user_exists(user_email):
            new_user = User(name=username, email=user_email)
            self.session.add(new_user)
            self.session.commit()

    def user_exists(self, user_email):
        try:
            self.session.query(User).filter_by(email=user_email).one()
            return True
        except NoResultFound:
            return False

    def get_category(self, category_name):
        if self.category_exists(category_name):
            return self.session.query(Category).filter_by(name=category_name.title()).one()


if __name__ == "__main__":
    helper = DBHelper()
    helper.create_user('default_user', 'default@example.com')
    pprint([user.serialize for user in helper.session.query(User).all()])

    helper.create_item('default item', 'something to test with', 'default', 'default@example.com')
    helper.create_item('another default', 'something with a later modified date', 'default', 'default@example.com')

    pprint([category.serialize for category in helper.session.query(Category).all()])
    pprint([item.serialize for item in helper.session.query(Item).all()])

