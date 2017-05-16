#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: html模式输出测试报告的插件

Authors: Turinblueice
Date:    16/3/23 16:18
"""


import traceback
import hashlib
import os
import datetime
import shutil
import xml.etree.ElementTree as ET


def get_md5_code(ori_str):

    m = hashlib.md5()
    m.update(ori_str)
    return m.hexdigest()


class HtmlOutput(object):
    """
        Summary:
            没有样式装饰的html代码
    """

    def __init__(self):
        """
        """
        super(HtmlOutput, self).__init__()

        #  默认报告所在目录
        default_report_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../../outputs/report/index'))

        if not os.path.isdir(default_report_dir):
            os.makedirs(default_report_dir)

        src_static_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'static')
        )
        dest_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../../outputs/report/static')
        )

        if not os.path.isdir(dest_dir):
            shutil.copytree(src_static_dir, dest_dir)
        # 默认报告路径
        self.__default_report_path = default_report_dir+'/report_index.html'

        # 报告一式两份, 用户给定一份,路径report_file, 可选; 本地保存一份, 默认路径为 default_report_path
        self.__report_path = self.__report_create_time = None
        self._init_report_path()

        self.__case_count = 0

        self.__error_count = 0
        self.__failure_count = 0

        self.__html = ['<html><head>',
                       '<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />',
                       '<link rel="stylesheet" type="text/css" href="../static/style/report.css" />',
                       '<title>测试报告</title>',
                       '</head>',
                       '<body></body>',
                       '</html>']


        # 报告文件生成完毕后,开始加载报告文件的dom tree
        # self.__tree = ET.parse(self.__report_file)
        # self.__root = self.__tree.getroot()

        #  直接将html string装在入dom内存, 不用先生成文件再从文件中载入
        self.__root = ET.fromstring(''.join(self.__html))
        self.__tree = ET.ElementTree(self.__root)
        self.__body = self.__root.find('body')

    def _add_table(self, test_name="", test_attr="", attr_count=0):
        """
        增加行

        :param: test_name: case或者测试集名称
        :param: test_attr: case验证步骤,测试集属性
        :param: attr_count: 验证步骤数
        :return: row_elem 返回行
        """
        self.__case_count += 1

        test_name = test_name.decode('utf8') if not isinstance(test_name, unicode) else test_name
        test_attr = test_attr.decode('utf8') if not isinstance(test_attr, unicode) else test_attr

        table_elem = self.__body.find('.//table[@id="{}"]'.format(get_md5_code(test_name.encode('utf8'))))

        if table_elem is None:
            table_elem = ET.SubElement(self.__body, 'table', attrib={'id': get_md5_code(test_name.encode('utf8'))})
            row_elem = ET.SubElement(table_elem, 'tr')
            cell_elem_1 = ET.SubElement(row_elem, 'td', attrib={'rowspan': str(attr_count),
                                                                'class': 'table-cell-group'})
            cell_elem_1.text = test_name
        else:
            row_elem = ET.SubElement(table_elem, 'tr')

        cell_elem_2 = ET.SubElement(row_elem, 'td', attrib={'class': 'table-cell'})
        cell_elem_2.text = test_attr

        return row_elem

    def add_success(self, test_name, test_attr="", attr_count=0):

        row_elem = self._add_table(test_name, test_attr, attr_count)

        cell_elem_3 = ET.SubElement(row_elem, 'td', attrib={'class': 'table-cell pass'})
        cell_elem_3.text = 'Pass'

    def add_failure(self, test_name, test_attr="", attr_count=0):

        self.__failure_count += 1

        row_elem = self._add_table(test_name, test_attr, attr_count)

        cell_elem_3 = ET.SubElement(row_elem, 'td', attrib={'class': 'table-cell failure'})
        cell_elem_3.text = 'fail'

    def add_error(self, test_name, test_attr="", attr_count=0, error=""):

        self.__error_count += 1

        row_elem = self._add_table(test_name, test_attr, attr_count)

        error = error.decode('utf8') if not isinstance(error, unicode) else error
        cell_elem_3 = ET.SubElement(row_elem, 'td', attrib={'class': 'table-cell error'})
        cell_elem_3.text = error

    def finalize(self):

        elem = self.__root.find('.//*[@id="bottom"]')
        fail_elem = self.__root.find('.//*[@id="bottom-fail"]')
        if elem is None:

            row_elem = ET.SubElement(self.__body, 'div', attrib={'class': 'table-bottom', 'id': 'bottom'})
            row_elem.text = "Ran {} test{}".format(self.__case_count, self.__case_count != 1 and "s" or "")

            row_elem = ET.SubElement(self.__body, 'div', attrib={'class': 'table-bottom', 'id': 'bottom-fail'})
            row_elem.text = 'FAILED ( failures={} errors={} )'.format(self.__failure_count, self.__error_count)

        else:
            elem.text = "Ran {} test{}".format(self.__case_count, self.__case_count != 1 and "s" or "")
            fail_elem.text = 'FAILED ( failures={} errors={} )'.format(self.__failure_count, self.__error_count)

        if self.__report_path is None:
            self._init_report_path()

        self.__tree.write(self.__report_path, encoding='utf8')
        self.__tree.write(self.__default_report_path, encoding='utf8')

        self.__body.clear()  # 为下一次装载报告节点清除body
        self.__report_path = None  # 报告已完成,报告路径回到初始状态
        self.__report_create_time = None

        self.__case_count = self.__failure_count = self.__error_count = 0

    def dump_html(self):

        ET.dump(self.__tree)

    def _init_report_path(self):
        """
        初始化报告路径
        :return:
        """
        now = datetime.datetime.now()
        now_str = now.strftime("%Y%m%d%H%M%S")
        today_str = now.strftime("%Y%m%d")
        dir_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../../outputs/report/' + today_str)
        )

        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        html_report_path = os.path.join(dir_path, 'report_' + now_str + '.html')

        self.__report_path = html_report_path
        self.__report_create_time = now

    def get_report_create_time(self):

        return self.__report_create_time


# def _get_html_report():
#     """
#         Summary:
#             获取html报告路径
#     Returns:
#         (报告路径, 报告创建意见)
#
#     """
#     now = datetime.datetime.now()
#     now_str = now.strftime("%Y%m%d%H%M%S")
#     today_str = now.strftime("%Y%m%d")
#     dir_path = os.path.abspath(
#         os.path.join(os.path.dirname(__file__), '../../outputs/report/'+today_str)
#     )
#
#     if not os.path.isdir(dir_path):
#         os.makedirs(dir_path)
#
#     html_report_path = os.path.join(dir_path, 'report_'+now_str+'.html')
#     return html_report_path, now

HTML_report_manager = HtmlOutput()

if __name__ == '__main__':

    #path = '../../outputs/report/20161013/report_20161013154417'

    htmlrunner = HtmlOutput()
    htmlrunner.add_success('www', '他人IN记点击头像', 3)
    htmlrunner.add_success('www', '加载', 3)
    htmlrunner.add_success('www', '加载xx', 3)
    htmlrunner.add_failure('zzz', 'QQ登录失败', 2)
    htmlrunner.add_error('zzz', '他人IN记多页加载', '没有执行', 2)
    htmlrunner.finalize()
    htmlrunner.dump_html()
