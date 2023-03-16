import hashlib
import uuid
from mywebframework.db import TableManager
from settings import DB_NAME

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
        _salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(
            (password + _salt).encode()).hexdigest()
        User(DB_NAME).insert(
            username=username, first_name=first_name, last_name=last_name, password=hashed_password)

    def check_password(self, user_id, password):
        user = User.filter(id=user_id).first()
        _salt = user.salt
        hashed_password = hashlib.sha512(
            (password + _salt).encode()).hexdigest()
        return user.password == hashed_password


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
