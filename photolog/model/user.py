from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from photolog.model import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=False)
    password = Column(String(55), unique=False)

    photos = relationship('Photo',
                          backref='user',
                          cascade='all, delete, delete-orphan')

    def __init__(self, name, email, password):
        self.username = name
        self.email = email
        self.password = password

    # __repr__() 함수는 객체를 호추할 때 객체가 가진 속성값을 출력하여 어떤 값이 들어있는지 확인하는 용도로 디버깅이나 로깅에 사용
    def __repr__(self):
        return '<User %r %r>' % (self.username, self.email)
