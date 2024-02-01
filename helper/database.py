from sqlalchemy import Column, create_engine, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///ignore.db", echo=False, pool_size=10, query_cache_size=1024, max_overflow=100)
Session = sessionmaker(bind=engine)


class GroupInfo(Base):
    __tablename__ = 'ignore_ids'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, index=True)
    ignore_id = Column(Integer)
    linked_channel = Column(Integer, nullable=True)

    def __init__(self, chat_id, ignore_id, linked_channel=None):
        self.chat_id = chat_id
        self.ignore_id = ignore_id
        self.linked_channel = linked_channel


Base.metadata.create_all(engine)


def get_all_ignore_ids(chat_id: int):
    with Session() as session:
        result = session.query(GroupInfo).filter_by(chat_id=chat_id).all()
        return [c_id.ignore_id for c_id in result]


def create_new_ignore_id(chat_id: int, ignore_id: int, linked_channel: int = None):
    with Session() as session:
        if session.query(GroupInfo).filter_by(chat_id=chat_id, ignore_id=ignore_id).first():
            return False
        ignore = GroupInfo(chat_id=chat_id, ignore_id=ignore_id, linked_channel=linked_channel)
        session.add(ignore)
        session.commit()
        return True


def remove_ignore_id(chat_id: int, ignore_id: int):
    with Session() as session:
        ignore_list = session.query(GroupInfo).filter_by(chat_id=chat_id, ignore_id=ignore_id).first()
        if ignore_list:
            session.delete(ignore_list)
            session.commit()
            return True
        return False
