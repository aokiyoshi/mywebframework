from models import User, Course, Category, CourseType, Record, Token, Tag
from settings import DB_NAME

for model in (User, Course, Category, CourseType, Record, Token, Tag):
    model(DB_NAME).create_table()
