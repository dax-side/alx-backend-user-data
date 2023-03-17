#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self):
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ add and return a new user object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ search for a user"""
        if kwargs is None:
            raise InvalidRequestError

        for k in kwargs.keys():
            if k not in User.__table__.columns.keys():
                raise InvalidRequestError

        user_query = self._session.query(User).filter_by(**kwargs).first()

        if user_query:
            return user_query
        else:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """ update properties of an user """
        user = self.find_user_by(id=user_id)
        for i in kwargs.keys():
            if i not in User.__table__.columns.keys():
                raise ValueError

        for k, v in kwargs.items():
            setattr(user, k, v)

        self._session.commit()
