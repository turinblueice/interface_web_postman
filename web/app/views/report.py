#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 测试报告查看处理模块

Authors: Turinblueice
Date:
"""

from flask import Blueprint
from flask import render_template
from flask import request
import re
import os


report = Blueprint('report', __name__, template_folder='../../../outputs/report/',
                   static_folder='../../../outputs/report/static')


@report.route('/index/', methods=('get',))
def show_report():
    """
    展示执行报告
    :return:
    """

    return render_template('index/report_index.html')


@report.route('/<date>/', methods=('get',))
def show_date_report(date):
    """
    展示按日期划分的报告
    :return:
    """

    date_str = date.encode('utf8')
    if re.match(r"\d{8}", date_str) is None:
        return '报告时间目录访问错误'

    timestamp = request.args.get('time', None)
    if timestamp is None:
        return '未设置报告的时间戳'

    if re.match(r"\d{14}", timestamp) is None:
        return '报告时间戳设置错误,格式为14位数字'

    template_name = 'report_'+timestamp.encode('utf8')+'.html'

    template_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../../outputs/report/{}/{}'.format(date_str, template_name)))

    if os.path.isfile(template_path):
        return render_template(date_str+'/'+template_name)

    return '无此报告'


