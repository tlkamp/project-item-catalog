from dbmodel import User, Category, Item, Base, db_string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


class DBHelper(object):
    '''
    Helper class to abstract the database session
    away from the primary api/webapp logic.
    '''
    engine = create_engine(db_string)
    Base.metadata.bind = engine
    __DBSession = sessionmaker(bind=engine)

    def __init__(self):
        self.session = DBHelper.__DBSession()

    # Item helpers
    def create_item(self, name, description, category_name, username):
        '''
        Creates an item if it does not exist.
        Will also create the containing category if it does not exist.
        :param name: The name of the item.
        :param description: The description of the item
        :param category_name: The category name of the item.
        :param username: The currently logged in user's name.
        :return: The item that was created. None if no item created.
        '''
        current_user = self.session.query(User).filter_by(name=username).one()
        if not self.__category_exists(category_name):
            self.create_category(category_name)

        cat = self.session.query(Category).filter_by(
            name=category_name.title()).one()
        if not self.__item_exists(name, cat.id):
            new_item = Item(
                name=name,
                desc=description,
                user_id=current_user.id,
                category_id=cat.id)
            self.session.add(new_item)
            self.session.commit()
            return new_item

    def update_item(self, item_id, new_name=None,
                    new_category=None, new_desc=None):
        '''
        Updates an item if it exists in the database.
        Will create a new category if necessary.
        :param item_id: The id of the item to update.
        :param new_name: The new name of the item.
        :param new_category: The name of the category the item belongs to.
        :param new_desc: The new description of the item.
        :return: The updated item.
        '''
        item_to_update = self.session.query(Item).filter_by(id=item_id).one()
        if new_name:
            item_to_update.name = new_name
        if new_category:
            cat = self.create_category(category_name=new_category)
            if cat:
                item_to_update.category = cat
        if new_desc:
            item_to_update.desc = new_desc
        self.session.commit()
        return item_to_update

    def __item_exists(self, item_name, category_id=None, category_name=None):
        item_category = self.get_category(
            category_id=category_id,
            category_name=category_name)
        if not item_category:
            return False

        try:
            self.session.query(Item).filter_by(
                category_id=item_category.id).filter_by(
                name=item_name).one()
            return True
        except NoResultFound:
            return False

    def get_item(self, item_name, item_category_name=None,
                 item_category_id=None):
        '''
        Get a specific item from the database.
        :param item_name: The name of the desired item.
        :param item_category_name: The name of category the item is in.
        :param item_category_id: The id of the category
        :return: The item, if it exists. None if it does not exist.
        '''
        if self.__item_exists(item_name,
                              category_id=item_category_id,
                              category_name=item_category_name):
            item_category = self.get_category(
                category_name=item_category_name,
                category_id=item_category_id)
            return self.session.query(Item).filter_by(
                name=item_name, category=item_category).one()
        return None

    def delete_item(self, item_obj):
        '''
        Deletes an item from the database.
        :param item_obj: The item to delete.
        :return: None
        '''
        self.session.delete(item_obj)
        self.session.commit()

    # Category helpers
    def __category_exists(self, category_name=None, category_id=None):
        if category_name:
            try:
                self.session.query(Category).filter_by(
                    name=category_name.title()).one()
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
        '''
        Creates a category if it does not exist.
        :param category_name: The name of the category.
        :return: The newly created category,
        if one was created. None otherwise.
        '''
        if category_name and not self.__category_exists(
                category_name=category_name):
            new_category = Category(name=category_name.title())
            self.session.add(new_category)
            self.session.commit()
            return new_category

    def get_category(self, category_name=None, category_id=None):
        '''
        Get a category from the database.
        :param category_name: The name of the desired category.
        :param category_id: The id of the desired category.
        :return: The category if it exists. None otherwise.
        '''
        if self.__category_exists(
                category_name=category_name, category_id=category_id):
            if category_name:
                return self.session.query(Category).filter_by(
                    name=category_name.title()).one()
            else:
                return self.session.query(
                    Category).filter_by(id=category_id).one()

    # User helpers
    def create_user(self, username):
        '''
        Creates a user if it does not exist.
        :param username: The username for the new user.
        :return: The user that was created,
        or the existing user.
        '''
        if not self.user_exists(username):
            new_user = User(name=username)
            self.session.add(new_user)
            self.session.commit()
        return self.session.query(User).filter_by(name=username).one()

    def get_user(self, user_id=None, username=None):
        '''
        Get a particular user from the database.
        :param user_id: The id of the desired user.
        :param username: The username of the desired user.
        :return: The user, if it exists. None otherwise.
        '''
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
        '''
        Check the database for a particular user.
        :param username: The username of the user to check for.
        :return: True if the user exists, False if it does not.
        '''
        try:
            self.session.query(User).filter_by(name=username).one()
            return True
        except NoResultFound:
            return False


if __name__ == "__main__":
    # Add some default information to the database.
    # This proves that the non-default user cannot delete
    # the default user's items.
    default_user = 'default_user'
    helper = DBHelper()
    helper.create_user(default_user)

    helper.create_item(
        'default item',
        'something to test with',
        'default',
        default_user)
    helper.create_item(
        'another default',
        'something with a later modified date',
        'default',
        default_user)

    # Let the user know the database has been
    # successfully initialized.
    print('Ready to go!')
