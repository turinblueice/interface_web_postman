#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: case group数据库model

Authors: Turinblueice
Date:
"""
from web.app.extensions import db


class CaseGroups(db.Model):

    __tablename__ = 'group'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement='auto')
    name = db.Column('name', db.Text, nullable=False)
    description = db.Column('description', db.String, nullable=False)

    def __init__(self, name, description=""):

        self.name = name
        self.description = description  # 预留字段, 组别的描述信息

    def save(self, lazy=False):
        """
            Summary:
                将该条目保存到数据库
        :param lazy: True: 立即提交事务至数据库;False: 延迟提交事务至数据库
        :return:
        """
        db.session.add(self)
        if not lazy:
            db.session.commit()

    def discard(self, lazy=False):
        """
            Summary:
                数据库中废弃该条目
        :param lazy:
        :return:
        """
        db.session.delete(self)
        if not lazy:
            db.session.commit()

    def __str__(self):

        return self.name + ": " + self.description

    def __repr__(self):

        return self.id, self.name, self.description


