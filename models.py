import hashlib
import uuid
from mywebframework.db import TableManager
from settings import DB_NAME
import secrets


class User(TableManager):
    table_name = 'users'

    def __init__(self, db):
        super().__init__(
            table_name=self.table_name,
            db=db,
            username='TEXT UNIQUE',
            first_name='TEXT',
            last_name='TEXT',
            password='TEXT',
            created_at='TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        )

    def create_user(self, username, first_name, last_name, password):
        hashed_password = hashlib.sha512(
            (password).encode()).hexdigest()
        User(DB_NAME).insert(
            username=username, first_name=first_name, last_name=last_name, password=hashed_password)

    def check_password(self, username, password):
        user = User(DB_NAME).select(username=username)
        if user is None:
            return False
        hashed_password = hashlib.sha512(
            (password).encode()).hexdigest()
        return user.get('password') == hashed_password
    
    def create_token(self, username):
        user_id = User(DB_NAME).select(username=username).get('id')
        token = Token(DB_NAME).select(user=user_id)
        if not token:
            token = secrets.token_urlsafe(32)
            Token(DB_NAME).insert(user=user_id, token=token)
        else:
            token = token.get('token')
        return token


class Token(TableManager):
    table_name = 'tokens'

    def __init__(self, db):
        super().__init__(
            table_name=self.table_name,
            db=db,
            user=User,
            token='TEXT',
            created_at='TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        )


class Course(TableManager):
    table_name = 'courses'

    def __init__(self, db):
        super().__init__(
            table_name=self.table_name,
            db=db,
            title='TEXT',
            desc='TEXT',
            category=Category,
            date='TIMESTAMP',
            type=CourseType,
            created_at='TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        )

    def append(self, data):
        self.insert(**data)

    def __len__(self):
        return len(self.select_all())


class Category(TableManager):
    table_name = 'categories'

    def __init__(self, db):
        super().__init__(
            table_name=self.table_name,
            db=db,
            title='TEXT',
            desc='TEXT',
            created_at='TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        )


class CourseType(TableManager):
    table_name = 'types'

    def __init__(self, db):
        super().__init__(
            table_name=self.table_name,
            db=db,
            title='TEXT',
            desc='TEXT',
            created_at='TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        )


class Record(TableManager):
    table_name = 'records'

    def __init__(self, db):
        super().__init__(
            table_name=self.table_name,
            db=db,
            course=Course,
            student=User,
            created_at='TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        )


class Tag(TableManager):
    table_name = 'tags'

    def __init__(self, db):
        super().__init__(
            table_name=self.table_name,
            db=db,
            course=Course,
            tag='TEXT',
        )

    def select_by_course_id(self, course_id):
        course = Course(DB_NAME).select(id=course_id)
        return Tag(DB_NAME).select_many(course=course)
