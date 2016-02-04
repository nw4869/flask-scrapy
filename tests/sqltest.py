from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.models import *

# engine = create_engine('sqlite:///:memory:', echo=True)
# Base = declarative_base()
#
#
# class User(Base):
#      __tablename__ = 'users'
#
#      id = Column(Integer, primary_key=True)
#      name = Column(String)
#      fullname = Column(String)
#      password = Column(String)
#
#      def __repr__(self):
#         return "<User(name='%s', fullname='%s', password='%s')>" % (
#                              self.name, self.fullname, self.password)

# Base.metadata.create_all(engine)

# Session = sessionmaker(bind=engine)
# session = Session()

# ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
# session.add(ed_user)
# session.commit()
#
# user = session.query(User).filter_by(name='ed').first()
# print(user)

from config import DevelopmentConfig
from manage import app


# engine = create_engine('sqlite:///../data-dev.sqlite', echo=True)
# engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI, echo=True)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
Session = sessionmaker(bind=engine)
session = Session()
new_task = Task(name='new_task')
session.add(new_task)
session.commit()
task = session.query(Task).filter_by(name='new_task').first()
print(task.name)
