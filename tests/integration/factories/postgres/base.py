from factory.alchemy import SQLAlchemyModelFactory  # type: ignore
from sqlalchemy.orm import Session


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    @classmethod
    def set_session(cls, session: Session) -> None:
        if cls is BaseFactory:
            for sub_factory in cls.__subclasses__():
                sub_factory.set_session(session)
        else:
            cls._meta.sqlalchemy_session = session
