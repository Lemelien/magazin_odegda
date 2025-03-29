from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'пользователи'
    id = Column(Integer, primary_key=True)
    имя_пользователя = Column(String(50), unique=True)
    пароль = Column(String(50))
    email = Column(String(100), unique=True)
    дата_регистрации = Column(DateTime, default=datetime.datetime.utcnow)
    роль = Column(String(20), default='пользователь')

class Brand(Base):
    __tablename__ = 'бренды'
    id = Column(Integer, primary_key=True)
    название = Column(String(255))
    описание = Column(String)
    страна = Column(String(100))
    год_основания = Column(Integer)
    товары = relationship("ClothingItem", back_populates="бренд")

class Category(Base):
    __tablename__ = 'категории'
    id = Column(Integer, primary_key=True)
    название = Column(String(255))
    описание = Column(String)
    товары = relationship("ClothingItem", back_populates="категория")

class ClothingItem(Base):
    __tablename__ = 'товары'
    id = Column(Integer, primary_key=True)
    бренд_id = Column(Integer, ForeignKey('бренды.id'))
    категория_id = Column(Integer, ForeignKey('категории.id'))
    название = Column(String(255))
    описание = Column(String)
    цена = Column(Float)
    количество_на_складе = Column(Integer)
    дата_добавления = Column(DateTime, default=datetime.datetime.utcnow)
    скидка = Column(Integer, default=0)
    цвет = Column(String(50))
    размер = Column(String(20))
    изображение = Column(String(255))  # Новое поле для пути к изображению
    бренд = relationship("Brand", back_populates="товары")
    категория = relationship("Category", back_populates="товары")

class Order(Base):
    __tablename__ = 'заказы'
    id = Column(Integer, primary_key=True)
    пользователь_id = Column(Integer, ForeignKey('пользователи.id'))
    дата_заказа = Column(DateTime, default=datetime.datetime.utcnow)
    статус = Column(String(50), default='в обработке')
    общая_сумма = Column(Float)
    товары = relationship("OrderItem", back_populates="заказ")

class OrderItem(Base):
    __tablename__ = 'товары_в_заказах'
    id = Column(Integer, primary_key=True)
    заказ_id = Column(Integer, ForeignKey('заказы.id'))
    товар_id = Column(Integer, ForeignKey('товары.id'))
    количество = Column(Integer)
    цена_за_единицу = Column(Float)
    заказ = relationship("Order", back_populates="товары")

class Connect:
    @staticmethod
    def create_connection():
        engine = create_engine("postgresql://postgres:1234@localhost:5432/looksy")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        return Session()