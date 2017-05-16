#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: case加载模块

Authors: Turinblueice
Date: 2016/7/27
"""
import xml.etree.cElementTree as ET
import os
import json
from . import xml_case_key


class CaseLoader(object):
    """
        Summary:
            加载case模块
            所有加载case模块的父类,预留公共变量和方法给子类调用+实现
    """
    def __init__(self):
        super(CaseLoader, self).__init__()
        self._case_model = dict(
            name='',
            id='',
            url='',
            method='',
            params=dict(),
            data=dict(),
            headers=dict(),
            cookies=dict(),
            tests='',
            results=dict()
        )
        self._case_list = list()

    def _update_case_model(self, **kwargs):

        case_model = dict()
        for key in kwargs:
            if key in self._case_model:
                case_model[key] = kwargs[key]
        return case_model


class XMLCaseLoader(CaseLoader):

    def __init__(self, xml_path=None):
        super(XMLCaseLoader, self).__init__()
        default_xml_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../cases/case_example.xml')
        )
        self.__xml = xml_path or default_xml_path

    def load(self, xml_path=None):
        """
            Summary:
                载入case
        :return:
        """
        xml_file = xml_path or self.__xml
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for case in root:
            headers = dict()
            params = dict()
            results = dict()
            case_id = case.get(xml_case_key.XMLKey.CASE_ATTR_ID).encode('utf8').strip()
            case_name = case.get(xml_case_key.XMLKey.CASE_ATTR_NAME).encode('utf8').strip()
            url_link = case.iter(xml_case_key.XMLKey.URL).next().text.encode('utf8').strip()
            method = case.iter(xml_case_key.XMLKey.METHOD).next().text.encode('utf8').strip()
            for param in case.iter(xml_case_key.XMLKey.PARAMS).next():
                params[param.tag] = param.text.encode('utf8').strip()
            for header in case.iter(xml_case_key.XMLKey.HEADER).next():
                headers[header.tag] = header.text.encode('utf8').strip()

            for result in case.iter(xml_case_key.XMLKey.RESULT).next():
                results[result.tag] = result.text.encode('utf8').strip() if result.text else ''

            curr_case = self._update_case_model(id=case_id, name=case_name, url=url_link, method=method,
                                                params=params, headers=headers, results=results)
            self._case_list.append(curr_case)
        return self._case_list


class SQLAlchemyCaseLoader(CaseLoader):
    """
        Summary:
            sqllite数据库case载入
    """

    def __init__(self, case_list):
        """

        :param case_list: 用例列表, 用例为sqlalchemy中的declarative类对象
        """
        super(SQLAlchemyCaseLoader, self).__init__()
        self.__case_items = case_list

    def _update_case_model(self, **kwargs):
        """
        重写父类方法
        :param kwargs:
        :return:
        """
        case_model = dict()
        for key in kwargs:
            if key in self._case_model:
                if key in ('params', 'headers', 'cookies', 'data'):
                    case_model[key] = json.loads(kwargs[key]) if kwargs[key] else {}
                else:
                    case_model[key] = kwargs[key]
        return case_model

    def load(self, case_list=None):
        """

        :param case_list: sqlalchemy数据模型对象列表
        :return:
        """

        case_list = case_list or self.__case_items
        for case in case_list:

            curr_case = self._update_case_model(id=case.id, name=case.name, url=case.url, method=case.method,
                                                params=case.params, data=case.data, headers=case.headers,
                                                cookies=case.cookies, tests=case.tests)
            self._case_list.append(curr_case)
        return self._case_list


if __name__ == '__main__':

    loader = XMLCaseLoader()
    a = loader.load()
    pass