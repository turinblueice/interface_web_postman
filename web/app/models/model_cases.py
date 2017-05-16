#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: cases数据库model

Authors: Turinblueice
Date:
"""
from web.app.extensions import db


class Cases(db.Model):

    __tablename__ = 'cases'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement='auto')
    name = db.Column('name', db.Text, nullable=False)
    prior = db.Column('prior', db.String(2), nullable=False)
    description = db.Column('description', db.String)
    url = db.Column('url', db.Text, nullable=False)
    method = db.Column('method', db.String, nullable=False)
    headers = db.Column('headers', db.Text, nullable=False)
    params = db.Column('params', db.Text)
    data = db.Column('data', db.Text)
    cookies = db.Column('cookie', db.Text, nullable=False)
    tests = db.Column('tests', db.Text, nullable=False)

    group_id = db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('CaseGroups', backref=db.backref('cases', lazy='dynamic'))

    def __init__(self, name, group_id, prior="1", description="", url="", method="get",
                 headers="", params="", data="", cookies="", tests=""):

        self.name = name
        self.group_id = group_id
        self.prior = prior
        self.description = description
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.cookies = cookies
        self.tests = tests

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

    def commit(self):
        """
            Summary:
                提交更改
        :return:
        """
        db.session.commit()

    def __str__(self):

        return self.name + ": " + self.url

    def __repr__(self):

        return self.id, self.name, self.prior

