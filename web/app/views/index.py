#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 导航页

Authors: Turinblueice
Date:
"""

from flask import Blueprint
from flask import render_template
from flask import request
from flask import Response
from utils import log
import datetime
import json
import requests
import os

index = Blueprint('index', __name__, template_folder='../../templates')


@index.route('/')
def show_index():

    # from web.app.models.model_case_group import CaseGroups
    # from web.app.models.model_cases import Cases
    #
    # groups = CaseGroups.query.all()
    # cases = groups[0].cases.all()
    #
    # case = Cases.query.filter_by(id=1).first()
    # group = case.group
    lines = [u"1. 输入网址url, 输入相应参数, 点击请求获取内容",
             u"2. 点击保存, 可以将url和相应参数保存",
             u"3. 使用JavaScript语法写自定义验证方法,如 tests[\"测试\"] = responseBody.code == 200"]

    return render_template('index.html', lines=lines)

