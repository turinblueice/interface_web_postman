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

from web.app.models import model_cases
from web.app.models import model_case_group
from web.app.extensions import db
from custom_exceptions import exceptions as EXP
from utils import log
import datetime
import json
import requests
import re


processor = Blueprint('processor', __name__, template_folder='../../templates')


@processor.route('/', methods=('get',))
def case_process():
    """
        Summary:
            case操作页访问
    :return:
    """
    groups = model_case_group.CaseGroups.query.all()
    rsp = render_template('processor.html', groups=groups)
    return rsp


@processor.route('/upload_req/', methods=('post',))
def request_handler():
    """
        Summary:
            上传请求,获取请求后的的处理方法
    :return:
    """

    form = request.form
    url = form.get('url', None)
    method = form.get('method', None)
    headers = form.get('headers', None)
    data = form.get('data', None)
    cookies = form.get('cookies', None)

    try:
        headers = json.loads(headers.encode('utf8')) if headers else '{}'
        data = json.loads(data.encode('utf8')) if headers else '{}'
        cookies = json.loads(cookies.encode('utf8')) if cookies else '{}'
    except ValueError:
        log.logger.error("传入的数据非json格式")

    # 发送请求,获取请求结果
    rsp = _make_request(method, url, data, headers, cookies)

    # 获取返回response的cookie
    cookies = dict()
    rsp_cookies = rsp.cookies
    for cookie in rsp_cookies:
        cookies[cookie.name] = {}
        cookies[cookie.name]['name'] = cookie.name
        cookies[cookie.name]['value'] = cookie.value
        cookies[cookie.name]['domain'] = cookie.domain
        cookies[cookie.name]['path'] = cookie.path
        cookies[cookie.name]['expires'] = datetime.datetime.fromtimestamp(cookie.expires).strftime("%Y-%m-%d %H:%M:%S") \
            if cookie.expires else ''
        cookies[cookie.name]['secure'] = cookie.secure
        cookies[cookie.name]['httponly'] = False if not cookie.has_nonstandard_attr('httponly') else cookie.httponly

    # 获取header信息
    headers = dict(rsp_header=rsp.headers)

    content = rsp.text  # 获取返回的文本string, 非二进制byte流
    content_type = rsp.headers['content-type']

    curr_rsp = Response(content, content_type=content_type)
    curr_rsp.headers.add('rsp-cookie', _to_string(cookies))
    curr_rsp.headers.add('rsp-header', _to_string(headers))

    return curr_rsp


@processor.route('/save_request/', methods=['post'])
def save_request():
    """
        Summary:
            将请求保存到数据库, 包含新增和修改case的保存
    :return:
    """
    forms = request.form.items()
    status_dic = dict(code=0)
    try:
        forms = map(_check_form, forms)
        forms = dict(forms)

        group = forms['group']
        if model_case_group.CaseGroups.query.filter_by(name=group).first() is None:
            #  新增分组
            new_group = model_case_group.CaseGroups(name=group)
            new_group.save()

        group_id = model_case_group.CaseGroups.query.filter_by(name=group).first().id

        if 'id' in forms:  # 更改case
            if re.match('^\d+$', forms['id']):
                case_id = int(forms['id'])
                case_item = model_cases.Cases.query.filter_by(id=case_id).first()

                case_item.id = case_id
                case_item.name = forms['name']
                case_item.group_id = group_id
                case_item.prior = forms['prior']
                case_item.params = forms['params']
                case_item.description = forms['description']
                case_item.url = forms['url']
                case_item.method = forms['method']
                case_item.headers = forms['headers']
                case_item.data = forms['data']
                case_item.cookies = forms['cookies']
                case_item.tests = forms['tests']

                case_item.commit()

        else:  # 新增case
            case_item = model_cases.Cases(name=forms['name'], group_id=group_id, description=forms['description'],
                                          prior=forms['prior'], url=forms['url'], method=forms['method'],
                                          headers=forms['headers'], data=forms['data'], cookies=forms['cookies'],
                                          tests=forms['tests'])
            case_item.save(False)

        return Response(response=json.dumps(status_dic), content_type='application/json')

    except Exception as exp:

        status_dic["code"] = 1
        status_dic["msg"] = str(exp)
        return Response(response=json.dumps(status_dic), content_type='application/json')


@processor.route("/get_groups/", methods=['get'])
def get_groups():
    """
        Summary:
            获取所有分组
    :return:
    """
    groups = model_case_group.CaseGroups.query.all()
    group_infos = map(lambda group: dict(id=group.id, name=group.name), groups)
    group_dict = dict(groups=group_infos)

    return Response(response=json.dumps(group_dict), content_type='application/json')


# 以下为公共方法
def _make_request(method, url, data, headers, cookies):
    """
        Summary:
            构建一个请求
    :param method: 请求方法get/post/put/delete
    :param url: 连接
    :param data: post方法方法体传递的数据
    :param headers: 消息头
    :param cookies: cookie
    :return: 返回response
    """
    rsp = requests.request(method, url, data=data, headers=headers, cookies=cookies)

    return rsp


def _to_string(key_dict):
    """
        Summary:
            字典转化为字符串,字典格式为{key:{}}的格式,如
            把{name1:{name:xx,value:xx,domain:dd},
            name2:{name:xx,value:xx,domain:dd}} 转化成name@xx&value@xx&domain@dd|name@xx&value@xx&domain@dd
    :param key_dict:
    :return:
    """
    dict_str = ''
    for outer_key, outer_value in key_dict.iteritems():
        for key in outer_value:
            str_slice = str(key)+'@'+str(outer_value[key])
            dict_str += str_slice
            dict_str += '&'
        dict_str = dict_str[:-1]
        dict_str += '|'
    dict_str = dict_str[:-1]
    return dict_str


def _check_form((key, value)):
    """
        Summary:
            检查表单返回数据
        Args:
            key: 表单键
            value: 表单值
        Return:
            返回字符串或者None
    """
    if isinstance(value, unicode):
        return key, value
    elif isinstance(value, str):
        return key, value.decode('utf8')  # 解析成unicode串保存
    raise EXP.FormValueError("参数"+key+"传递错误,应为unicode或者string类型")