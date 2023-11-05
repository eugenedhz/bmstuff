from api.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


Column = db.Column
Model = db.Model


tagged_todos = db.Table('tagged_todos',
	Column('todo_id', db.Integer, db.ForeignKey('todo.id')),
	Column('todo_tag_id', db.Integer, db.ForeignKey('todo_tag.id'))
)


tagged_files = db.Table('tagged_files',
	Column('file_id', db.Integer, db.ForeignKey('file.id')),
	Column('file_tag_id', db.Integer, db.ForeignKey('file_tag.id'))
)


class User(Model): 
	id = Column(db.Integer, primary_key = True)

	todos = db.relationship('Todo', backref='user', lazy='dynamic')
	files = db.relationship('File', backref='user', lazy='dynamic')

	username = Column(db.String(64), unique=True)
	email = Column(db.String(120), unique=True)
	password_hash = Column(db.String(128))
	
	def hash_password(self, password):
		self.password_hash = generate_password_hash(password=password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)


class Admin(Model):
	id = Column(db.Integer, primary_key = True)

	username = Column(db.String(64), unique=True)
	password_hash = Column(db.String(128))
	
	def hash_password(self, password):
		self.password_hash = generate_password_hash(password=password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)


class Todo(Model):
	id = Column(db.Integer, primary_key = True)

	taggedTodos = db.relationship('TodoTag', secondary=tagged_todos, lazy='joined')
	files = db.relationship('File', backref='files', lazy='dynamic')
	user_id = Column(db.Integer, db.ForeignKey('user.id'))

	title = Column(db.String(150))
	text = Column(db.String(2000))
	done = Column(db.Boolean, default=False)
	date_to = Column(db.Date)
	date = Column(db.Date)


class File(Model):
	id = Column(db.Integer, primary_key = True)

	taggedFiles = db.relationship('FileTag', secondary=tagged_files, lazy='joined')
	user_id = Column(db.Integer, db.ForeignKey('user.id'))
	todo_id = Column(db.Integer, db.ForeignKey('todo.id'))

	title = Column(db.String(100))
	path = Column(db.String(50))


class TodoTag(Model):
	id = Column(db.Integer, primary_key = True)

	title = Column(db.String(50))


class FileTag(Model):
	id = Column(db.Integer, primary_key = True)

	title = Column(db.String(50))
