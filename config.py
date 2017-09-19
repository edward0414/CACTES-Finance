# default config

class BaseConfig(object):
	DEBUG = False
	SECRET_KEY = 'CACTES'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///test2.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	

class DevelopmentConfig(BaseConfig):
	DEBUG = True


class ProductionCongfig(BaseConfig):
	DEBUG = False