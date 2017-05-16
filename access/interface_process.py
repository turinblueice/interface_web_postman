#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 网络接口处理模块

Authors: Turinblueice
Date: 2016/7/27
"""
import requests
import PyV8
from utils import log


class WebApiProcessor(object):

    def __init__(self, case=None):
        """

        :param case:
            name=None,
            id=None,
            url=None,
            method=None,
            params=None,
            data=None,
            headers=None,
            cookies=None,
            tests=None,
            results=None
        """
        self.__case = case
        self.__rsp = None

    def get_case_name(self):

        if isinstance(self.__case['name'], unicode):
            return self.__case['name'].encode('utf8')

        return self.__case['name']

    def get_case_id(self):

        if isinstance(self.__case['id'], unicode):
            return self.__case['id'].encode('utf8')

        return self.__case['id']

    def get_case_url(self):

        if isinstance(self.__case['url'], unicode):
            return self.__case['url'].encode('utf8')

        return self.__case['url']

    def get_case_tests(self):

        if isinstance(self.__case['tests'], unicode):
            return self.__case['tests'].encode('utf8')

        return self.__case['tests']

    def make_request(self):

        url, method, params, data, headers, cookies = self.__case['url'], self.__case['method'], \
                                                      self.__case['params'], self.__case['data'], \
                                                      self.__case['headers'], self.__case['cookies']
        rsp = requests.request(method, url, params=params, data=data, cookies=cookies, headers=headers)
        self.__rsp = rsp
        return rsp

    def save_response(self, rsp=None):

        rsp = rsp or self.__rsp

    def get_header(self):

        return self.__rsp.headers

    def get_json_response_obj(self, rsp=None):

        rsp = rsp or self.__rsp
        if rsp:
            if 'application/json' in self.__rsp.headers['content-type']:
                return rsp.json()
        return None

    def assert_http_status_code(self, code=200):
        """
            Summary:
                断言,判断http状态码
            Args:
                code: 状态码,比如200
        :return:
        """

        ret_code = self.__rsp.status_code
        assert ret_code == code

    def _get_json_value(self, json_obj=None, key=None):
        """
            Summary:
                获取json对象中给定key的值
            Args:
                json_obj: json对象
                key: json对象的key,若为多层对象结构,则形式为 key1-key2-key3,对应于{key1:{key2:{key3:value}}}
        :return:
        """
        json_obj = json_obj or self.get_json_response_obj()
        value = None
        case_id = self.get_case_id()

        if key:
            key_items = key.split('-')

            for key_item in key_items:
                log.logger.info("第{}个case,当前字段{}".format(case_id, key_item))
                try:
                    value = json_obj[key_item]
                    json_obj = value
                except KeyError:
                    value = None
                    break

        return value

    def assert_all_json_value(self):
        """
            Summary:
                验证所有给定的result验证
        :return:
        """
        case_id = self.get_case_id()
        str_to_bool = {'true': True, 'false': False}
        json_obj = self.get_json_response_obj()
        results = self.__case['results']
        for result_key in results:
            value = self._get_json_value(json_obj, result_key)
            # bool值转换

            if results[result_key].lower() in ('true', 'false'):
                results[result_key] = str_to_bool[results[result_key].lower()]

            log.logger.info("开始验证第{}个case的字段{}".format(case_id, result_key))
            try:
                assert value == results[result_key], "返回结果不正确,期待结果{},实际结果{}".format(value, results[result_key])
                log.logger.info("第{}个case的字段{}验证完毕,返回正确".format(case_id, result_key))
            except AssertionError as exp:
                log.logger.error("第{}个case的字段{}验证完毕,返回正确".format(case_id, result_key))
                raise exp

    def get_javascript_tests_result(self, tests_lines=None, json_obj=None):
        """
            Summary:
                对js编写的用例进行断言
            Args:
                tests_lines: 测试语句,用分号分隔
        :return:
        """

        json_obj = json_obj or self.get_json_response_obj()

        if json_obj is None:
            return None

        tests_lines = tests_lines or self.get_case_tests()
        tests_lines = tests_lines.encode('utf8') if isinstance(tests_lines, unicode) else tests_lines
        js_str = """
                    (function(jsbody){
                        var responseBody = jsbody;
                        var tests = new Object();""" + tests_lines + """
                        return tests
                    })
                """
        test_dic = dict()
        with PyV8.JSLocker():
            js_context = PyV8.JSContext()
            js_context.enter()
            test_func = js_context.eval(js_str.decode('utf8'))
            test_jsobj = test_func(json_obj)
            for key in test_jsobj.keys():
                test_dic[key] = test_jsobj[key]
            js_context.leave()

        return test_dic


if __name__ == "__main__":

    web = WebApiProcessor()
    tests_line = "tests['xx'] = responseBody.a == 1;tests['yy'] = responseBody.a==2"
    json_string = {'a': 1, 'b': 2}

    tests = web.get_javascript_tests_result(tests_line, json_string)
    print tests['xx']

