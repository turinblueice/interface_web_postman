#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: URL case操作处理模块

Authors: Turinblueice
Date:
"""
from flask import Blueprint
from flask import render_template
from flask import request
from flask import Response

from case_loader import case_loader
from test_running import runner
import json
import re

from web.app.models import model_cases
from web.app.models import model_case_group
from web.app.extensions import db

cases = Blueprint('cases', __name__, template_folder='../../templates')

CASES_PER_PAGE = 4


@cases.route('/', methods=['get'])
@cases.route('/<int:group_id>/', methods=('get',))
def display(group_id=None):
    """
        Summary:
            展示case
    :return:
    """
    curr_page_num = request.args.get('page_num', '1')
    curr_page_num = int(curr_page_num) if re.match('^\d+$', curr_page_num) else 1  # 非数字则默认为1

    if group_id is None or group_id == 0:
        query_set = model_cases.Cases.query
        group_id = 0

    else:
        group = model_case_group.CaseGroups.query.filter_by(id=int(group_id)).first()
        if group is None:
            return "无该分组"

        query_set = model_cases.Cases.query.filter(model_cases.Cases.group_id == group.id)

    try:   # 如果当前页码不在分页后页码的范围内[1,Max], 则默认返回首页
        pagination = query_set.paginate(curr_page_num, CASES_PER_PAGE, True)
    except:
        pagination = query_set.paginate(1, CASES_PER_PAGE, True)

    page_number_items = _get_page_list(pagination.page, 5, pagination.pages)
    groups = model_case_group.CaseGroups.query.all()

    return render_template('case_select.html', pagination=pagination, groups=groups,
                           group_id=group_id, page_nums=page_number_items)


@cases.route('/display-json-by-group/<int:group_id>/', methods=('get',))
def display_json_by_group(group_id):
    """
    按照组别返回case列表的接口
    :param group_id:
    :return:
    """
    rsp_dic = dict(code=0)

    start = request.args.get('start', '0')
    end = request.args.get('end', '20')

    comp = re.compile(r"^\d+$")

    start = int(start) if comp.match(start) else 0
    end = int(end) if comp.match(end) else 20

    if start > end:
        start = 0

    group = model_case_group.CaseGroups.query.filter_by(id=int(group_id)).first()
    if group is None:
        rsp_dic['code'] = 2
        rsp_dic['msg'] = u"没有该分组"

    else:
        curr_group_cases = group.cases   # group通过一对多的反向代理访问cases
        curr_group_cases = curr_group_cases.slice(start, end)  # 使用slice进行分页, 自动处理start和end和总数之间的数值大小关系

        case_list = [dict(id=case.id, name=case.name) for case in curr_group_cases]
        rsp_dic['cases'] = case_list

    return Response(json.dumps(rsp_dic), content_type='application/json')


@cases.route('/display-board-by-group/<int:group_id>/', methods=('get',))
@cases.route('/display-board-by-group/<int:group_id>/<int:page_num>/', methods=('get',))
def display_by_group(group_id, page_num=None):
    """
    按照组别返回case列表展示面板
    :param group_id: 分组ID
    :param page_num: 分码序号
    :return:
    """
    curr_page_num = page_num if page_num >= 1 else 1

    group = model_case_group.CaseGroups.query.filter_by(id=int(group_id)).first()
    if group is None:
        return "无该分组"

    query_set = model_cases.Cases.query.filter(model_cases.Cases.group_id == group.id)
    pagination = query_set.paginate(curr_page_num, CASES_PER_PAGE, True)
    page_number_items = _get_page_list(pagination.page, 5, pagination.pages)

    return render_template('case_select.html', pagination=pagination, page_nums=page_number_items)


@cases.route('/cases-submit/', methods=['post'])
def cases_submit():
    """
        Summary:
            提交将要执行的case列表, 并且执行case
    :return:
    """

    test_runner = runner.test_runner  # 将单例的测试执行模块赋值到临时变量

    if not test_runner.RUNNING:

        case_str = request.form.get('cases')
        case_list = case_str.split(',')[:-1]
        origin_cases = model_cases.Cases.query.filter(model_cases.Cases.id.in_(case_list)).all()

        loader = case_loader.SQLAlchemyCaseLoader(case_list=origin_cases)
        curr_cases = loader.load()

        test_runner.init_cases(curr_cases)
        test_runner.run_async(3)
        return '测试任务已提交,请等待运行结束'

    return '请等待测试任务结束再提交新任务'


# 公共方法
def _get_page_list(curr_page, per_page_items, page_count):
    """
        获取页码列表
    :param curr_page: 当前页码
    :param per_page_items: 每页显示页码数
    :param page_count: 总页码数
    :return:
    """
    if page_count <= 0:  # 总页码数为零,则说明无任何数据展示, 展示页空白
        return [1]

    if per_page_items >= page_count:  # 避免每页显示的页数大于总页数
        per_page_items = page_count

    if per_page_items <= 0:
        per_page_items = 1

    page_num_list = list()

    start_page = curr_page - per_page_items/2
    max_page_number = curr_page + per_page_items/2
    min_page_number = curr_page - per_page_items/2
    if page_count <= max_page_number:
        start_page = page_count - per_page_items + 1
    if 0 >= min_page_number:
        start_page = 1

    for index in xrange(per_page_items):
        page_num_list.append(start_page+index)

    return page_num_list


@cases.route('/delete/', methods=('post',))
def delete():
    """
    删除case
    :return:
    """
    rsp_dic = dict(succ=False)
    case_id = request.form.get('id')

    delete_item = model_cases.Cases.query.filter_by(id=int(case_id)).first()
    if delete_item:
        delete_item.discard()
        rsp_dic['succ'] = True

    return Response(response=json.dumps(rsp_dic), content_type='application/json')


@cases.route('/update/<int:case_id>/', methods=('post', 'get'))
def update(case_id):
    """
    更改case的json接口,供ajax使用
    :param case_id: case id
    :return:
    """
    rsp_dic = dict(id=-1, info=None)
    case = model_cases.Cases.query.filter_by(id=int(case_id)).first()
    if case:
        # 有该case

        # keys = ['id', 'name', 'prior', 'description', 'url', 'method',
        #         'headers', 'params', 'data', 'cookies', 'tests', 'group_id']
        # values = map(lambda key: case.__getattribute__(key), keys)
        info_dic = case.__dict__
        del info_dic['_sa_instance_state']  # 删除case model中的非数据字段

        info_dic['cookies'] = json.loads(case.cookies) if case.cookies else dict()
        info_dic['headers'] = json.loads(case.headers) if case.headers else dict()
        info_dic['params'] = json.loads(case.params) if case.params else dict()
        info_dic['data'] = json.loads(case.data) if case.data else dict()
        rsp_dic['id'] = case.id
        rsp_dic['tests'] = ';\n'.join(case.tests.split(';')) if case.tests else ""
        rsp_dic['info'] = info_dic

    return Response(response=json.dumps(rsp_dic), content_type='application/json')


@cases.route('/update-board/<int:case_id>/', methods=('get',))
def update_on_board(case_id):
    """
    返回更新数据的模版
    :return:
    """
    case = model_cases.Cases.query.filter_by(id=int(case_id)).first()
    if case:
        groups = model_case_group.CaseGroups.query.all()

        # 将case中部分字段在数据库存储的str字符串转为相应的对象
        case.cookies = json.loads(case.cookies) if case.cookies else dict()
        case.headers = json.loads(case.headers) if case.headers else dict()
        case.params = json.loads(case.params) if case.params else dict()
        case.data = json.loads(case.data) if case.data else dict()
        case.tests = ';\n'.join(case.tests.split(';')) if case.tests else ""

        return render_template('update_processor_board.html', case=case, groups=groups)
    return '无此id为{}的case'.format(case_id)

if __name__ == "__main__":

    print _get_page_list(4, 2, 6)