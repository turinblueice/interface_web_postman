#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 测试入口

Authors: Turinblueice
Date: 2016/7/27
"""
from case_loader import case_loader
from test_running import runner
from utils import log


if __name__ == '__main__':

    # url_list = case_loader.XMLCaseLoader().load()
    url_list = case_loader.SQLAlchemyCaseLoader().load()
    test_runner = runner.Runner(url_list)

    consumers = test_runner.create_consumers(3)
    tasks = test_runner.producing()
    tasks.join()

    log.logger.info("执行结束")
    results = test_runner.get_results()

    while not results.empty():
        result = results.get_nowait()
        case_num, status = result
        log.logger.info("第{}个case执行{}".format(case_num, '成功' if status else '失败'))