from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    marking_guide = Column(Text, nullable=False)

DATABASE_URL = 'sqlite:///data/database.db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Create the tables if they do not exist
    Base.metadata.create_all(bind=engine)
    
    # Add a sample question if the table is empty
    db = SessionLocal()
    if not db.query(Question).first():
        sample_question = Question(question_text="What is a computer?", marking_guide="A computer is an electronic device...")
        db.add(sample_question)
        db.commit()
    db.close()

# Call the init_db function to initialize the database
if __name__ == "__main__":
    init_db()
