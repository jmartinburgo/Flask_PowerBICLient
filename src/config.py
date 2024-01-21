class Config:
    SECRET_KEY= "asdlkjlkasdjlakssdlkjl"

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST= 'localhost'
    MYSQL_USER= 'root'
    MYSQL_DB= 'flask_login'


config = {
    'development': DevelopmentConfig
}