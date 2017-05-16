#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 程序运行控制模块

Authors: Turinblueice
Date:
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # 增加默认搜索路径

from flask_script import Manager
from flask_script import Server
from flask_script import Shell
from flask_script import prompt_bool
from web.app.extensions import db
from web import app


manager = Manager(app.create_app('development'))
manager.add_command("runserver", Server('0.0.0.0', port=5050))


def _mk_context():
    return dict(db=db)

manager.add_command("shell", Shell(make_context=_mk_context))  # 为app增加一个内部shell


@manager.command
def createall():
    """
        创建数据库表
    :return:
    """
    from web.app.models.model_case_group import CaseGroups
    from web.app.models.model_cases import Cases  # 导入模型表, 以便后续能创建表

    db.create_all()


@manager.command
def dropall():
    """
        删除所有表
    :return:
    """
    if prompt_bool("Are you sure?"):
        db.drop_all()


if __name__ == '__main__':

    manager.run()



