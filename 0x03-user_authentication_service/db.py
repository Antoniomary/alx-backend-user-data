#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

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

    def find_user_by(self, **data: dict) -> User:
        """returns the first row found in the users table
           as filtered by the method’s input arguments
        """
        possible_field = ['id',
                          'email',
                          'hashed_password',
                          'session_id',
                          'reset_token']
        for info in data:
            if info not in possible_field:
                raise InvalidRequestError()

        users = self._session.query(User).all()
        found = False
        for user in users:
            for k, v in data.items():
                if k == 'id' and user.id == v:
                    found = True
                elif k == 'email' and user.email == v:
                    found = True
                elif k == 'hashed_password' and user.hashed_password == v:
                    found = True
                elif k == 'session_id' and user.session_id == v:
                    found = True
                elif k == 'reset_token' and user.reset_token == v:
                    found = True
                else:
                    found = False
                    break

            if found:
                return user

        if not found:
            raise NoResultFound()
