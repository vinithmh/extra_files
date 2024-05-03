import sqlalchemy as db
from dotenv import load_dotenv
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from redis import Redis

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(121), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    role = db.Column(db.String(80), unique=False, nullable=False)

load_dotenv()

engine = db.create_engine(f"mysql+pymysql://{os.getenv('USER_NAME')}:{os.getenv('PASSWORD')}@{os.getenv('DB_URL')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")

cache = Redis(host=os.getenv('REDIS_DB_URL'), port=6379, db=0)

Session = sessionmaker(bind=engine)

session = Session()

def lazy_loading():
    try:
        # Retrieve user ID from cache
        user_id = cache.get("user_id")
        if user_id:
            # User ID found in cache, print it
            print("User ID retrieved from cache:", user_id.decode())
        else:
            # User ID not found in cache, fetch from database
            user = session.query(User).filter_by(email='sample@email.com').first()
            if user:
                # User found in database, store user ID in cache
                cache.set("user_id", user.id)
                print("User ID stored in cache:", user.id)
            else:
                # User not found in database
                print("User not found in database")
    except Exception as e:
        # Print any exceptions raised
        print("Exception occurred:", e)

# Call the lazy_loading function
lazy_loading()
