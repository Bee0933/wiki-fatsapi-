from sqlalchemy import Column, Integer, String
from .database import Base


# user table 
class User(Base):
      __tablename__ = 'user'
      id=Column(Integer, primary_key=True)
      username=Column(String(50), unique=True, nullable=False)
      email=Column(String(50), nullable=False)
      password=Column(String(200), nullable=False)

      def __repr__(self) -> str:
            return f'user: {self.username}, email : {self.email}'