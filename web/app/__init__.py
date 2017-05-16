#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 应用模块

Authors: Turinblueice
Date:
"""

from flask import Flask
from web import config
from web.app.extensions import db
from web.app import views


DEFAULT_APP_NAME = 'interfaceTest'


DEFAULT_MODULES = (
    (views.index, ""),
    (views.processor, "/processor"),
    (views.cases, "/cases"),
    (views.report, "/report"),
    (views.report_square, "/report-square")
)


def create_app(config_name, modules=None):
    """
        Summary:
            初始化APP,完成创建并且各全局功能模块的注册
    :param config_name: 配置名称
    :param modules: 模块远足或列表
    :return:
    """
    app = Flask(DEFAULT_APP_NAME)
    app.config.from_object(config.config[config_name])

    modules = modules or DEFAULT_MODULES
    configure_blueprint(app, modules)
    configure_extensions(app)

    return app


def configure_blueprint(app, modules):
    """
    对每个独立的module(view)设置蓝图
    :param app:
    :param modules:
    :return:
    """
    if isinstance(app, Flask):
        for module, url_prefix in modules:
            app.register_blueprint(module, url_prefix=url_prefix)


def configure_extensions(app):
    """
    初始化每个扩展插件
    :param app:
    :return:
    """
    if isinstance(app, Flask):
        db.init_app(app)

