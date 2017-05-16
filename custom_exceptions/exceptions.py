#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 自定义异常类

Authors: Turinblueice
Date:
"""


class FormValueError(Exception):
    """
        Summary:
            表单数据值异常
    """
    def __init__(self, message=None):
        self.message = message

    def __str__(self):

        return self.message or "没有描述"