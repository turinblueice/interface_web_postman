#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 报告列表广场

Authors: Turinblueice
Date:
"""

from flask import Blueprint
from flask import render_template
from flask import request
from flask import Response
import os
import re
import datetime


report_square = Blueprint('report_square', __name__, template_folder='../../templates')


@report_square.route('/', methods=('get',))
def show_report_square():
    """
    展示测试报告广场面板, 访问各个列表
    :return:
    """
    start_time = request.args.get('start', None)
    end_time = request.args.get('end', None)

    if start_time is None or end_time is None:
        today = datetime.datetime.today()
        week_ago = today - datetime.timedelta(days=6)
        end_time = today.strftime('%Y%m%d')
        start_time = week_ago.strftime('%Y%m%d')

    regex_comp = re.compile(r'\d{8}')
    if regex_comp.match(start_time) is None:
        return "开始时间格式错误,应该为8位数字"
    if regex_comp.match(end_time) is None:
        return "结束时间格式错误,应该为8位数字"

    report_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../../outputs/report')
    )

    report_dirs = filter(lambda report_dir: report_dir not in ['index', 'static'] and report_dir >= start_time and report_dir <= end_time,
                         os.listdir(report_path))

    report_urls_dic = dict()

    for report_dir in report_dirs:
        report_urls_dic[report_dir] = list()
        for url in os.listdir(os.path.join(report_path, report_dir)):
            timestamp = url[7:-5]
            report_urls_dic[report_dir].append(timestamp)

    return render_template('report_square.html', report_urls_dic=report_urls_dic)


