# -*- coding: utf-8 -*-


import sqlalchemy
sqlalchemy.__version__

engine = sqlalchemy.create_engine('postgresql://postgres:tuesday789@localhost:5432/Dissertation')


from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# define tables we'll be working with, and then define classes that we will map to those tables



from sqlalchemy import Column, Integer, String

class User(Base):
     __tablename__ = 'users'

     id = Column(Integer, primary_key=True)
     name = Column(String)
     fullname = Column(String)
     nickname = Column(String)

     def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
                             self.name, self.fullname, self.nickname)



Base.metadata.create_all(engine)

ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
ed_user.name
ed_user.nickname
print(str(ed_user.id))



from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)


session = Session()


# add a row to the table
ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
session.add(ed_user)

# query the table
our_user = session.query(User).filter_by(name='ed').first() 

print(ed_user is our_user)

session.add_all([
    User(name='wendy', fullname='Wendy Williams', nickname='windy'),
    User(name='mary', fullname='Mary Contrary', nickname='mary'),
    User(name='fred', fullname='Fred Flintstone', nickname='freddy')])


