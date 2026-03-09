import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


load_dotenv()


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()


#Define Models (Tables)
# Create your Python classes that inherit from the Base. These classes represent database tables.
#read up on the strucutre and what works or not .
class User(Base):
    __tablename__ = 'users' # The actual table name in the database
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)

    def __repr__(self):
        return f"<User(name='{self.name}', age='{self.age}')>" # remeber to figure out how this works 


Base.metadata.create_all(engine)        


Session = sessionmaker(bind=engine)



# with Session() as session:
#     # Create objects
#     user1 = User(name="Alice", age=30)
#     user2 = User(name="Bob", age=25)

#     # Add objects to the session
#     session.add_all([user1, user2])

#     # Commit the transaction to save changes to the database
#     session.commit()

#     # Query the database
#     # SQLAlchemy 2.0+ uses the select() construct for queries
#     from sqlalchemy import select
#     stmt = select(User).order_by(User.id)
#     results = session.execute(stmt).scalars().all()

#     print("\nUsers in the database:")
#     for user in results:
#         print(user)