#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from user import (
    Base,
    User
)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """saves the user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """returns the first row found in the users table
           as filtered by the method’s input arguments
        """
        if not kwargs:
            raise InvalidRequestError

        user = None

        valid_attributes = ['id', 'email', 'hashed_password',
                            'session_id', 'reset_token']
        for attr in kwargs.keys():
            if attr not in valid_attributes:
                raise InvalidRequestError

        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user:
                return user
        except InvalidRequestError:
            raise InvalidRequestError

        if not user:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates a user’s attributes with kwargs passed
        """
        user = self.find_user_by(id=user_id)

        valid_attributes = ['id', 'email', 'hashed_password',
                            'session_id', 'reset_token']

        for k, v in kwargs.items():
            if k not in valid_attributes:
                raise ValueError
            setattr(user, k, v)

        self._session.commit()
