#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 配置模块

Authors: Turinblueice
Date:
"""


import os


class Config(object):
    """
        app配置类
    """
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = '/app/static'
    STATIC_URL_PATH = '/app/static'


class DevelopmentConfig(Config):
    """
        开发环境配置
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(Config.BASE_DIR, 'database/db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    """
        生产环境配置
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(Config.BASE_DIR, 'database/db.sqlite')


config = {

    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
