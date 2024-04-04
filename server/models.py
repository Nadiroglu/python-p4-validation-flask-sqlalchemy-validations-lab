from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, ValidationError as WTFormsValidationError
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('All Authors must have a name')
        elif Author.query.filter_by(name = name).first():
            raise WTFormsValidationError('Username already exists')
        return name

    



    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number or not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError('Phone number must be exactly ten digits')
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if not content or len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if not summary or len(summary) > 250:
            raise ValueError("Post summary is a maximum of 250 characters")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category != "Fiction" and category != "Non-Fiction":
            raise ValueError("Post category must be either Fiction or Non-Fiction")
        return category

    @validates('title')
    def validate_title(self, key, title):
        list = ["Won't Believe", "Secret", "Top","Guess"]
        # for keyword in list:
        #     if keyword in title:
        #         return title
        # raise ValueError("Title must contain one of the followin keywords:")

        if not any(keyword in title for keyword in list):
            raise ValueError("Title must contain one of the followin keywords:")
        return title


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
