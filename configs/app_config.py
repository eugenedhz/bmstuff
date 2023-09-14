from datetime import timedelta


class Default(object):
	TESTING = False

	JWT_TOKEN_LOCATION = ['cookies']
	JWT_COOKIE_SAMESITE = 'None'
	JWT_COOKIE_CSRF_PROTECT = False
	JWT_COOKIE_SECURE = True
	JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
	JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
	JWT_SECRET_KEY = "jbOIASHODIHF*EHE#&*T738"

	DB_NAME = 'bmstu'
	DB_PASSWORD = 'test3915'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	@property
	def SQLALCHEMY_DATABASE_URI(self):
		return f'postgresql+psycopg2://postgres:{self.DB_PASSWORD}@localhost/{self.DB_NAME}'


class Development(Default):
	DB_NAME = 'bmstu'
	DB_PASSWORD = 'test3915'

	JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
	JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=2)


class Staging(Default):
	DB_NAME = 'bmstu'
	DB_PASSWORD = 'test3915'