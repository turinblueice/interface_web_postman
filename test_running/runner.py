#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: case 执行模块

Authors: Turinblueice
Date: 2016/7/27
"""

import multiprocessing.dummy as multithreading
from access import interface_process
from utils import log
from report.html_report_plugin import html_plugin


class Runner(object):
    """
        Summary:
            执行模块
        Attributes:
            __cases: case列表, case为组成webApiprocessor的参数元祖
            __tasks: 任务列表, 将待执行的任务放入该列表
            __results: 结果列表, 多线程收集结果的队列

    """
    _lock = multithreading.Lock()

    RUNNING = False  # 当前任务是否正在运行的标记

    def __init__(self, cases=None):
        """

        :param cases: case 列表
        """
        super(Runner, self).__init__()
        self.__cases = cases
        self.__tasks = multithreading.JoinableQueue()
        self.__results = multithreading.Queue()

    def init_cases(self, cases):
        """
        初始化case列表
        :param cases:
        :return:
        """
        self.__cases = cases

    def producing(self):
        """
            Summary:
                任务生产者,生产任务
        :return:
        """

        if self.__cases:
            case_processors = map(interface_process.WebApiProcessor, self.__cases)
            map(self.__tasks.put, case_processors)
            return self.__tasks
        log.logger.error("任务列表为空")
        return None

    def worker(self):
        """
            Summary:
                消费
        :return:
        """

        while True:
            web_processor = self.__tasks.get()
            case_id = web_processor.get_case_id()
            case_name = web_processor.get_case_name()
            url = web_processor.get_case_url()

            log.logger.info("即将处理case:{},URL为{}".format(case_name, url))
            web_processor.make_request()
            log.logger.info("完成处理case:{},URL为{}".format(case_name, url))

            status = True
            # web_processor.assert_all_json_value()
            tests_result = web_processor.get_javascript_tests_result()

            if tests_result is None:  # test_result为空
                with self._lock:
                    html_plugin.HTML_report_manager.add_error(case_name, error=u'返回数据为非json格式')
                log.logger.info("case:{}完成报告写入".format(case_name))
                self.__results.put((case_id, case_name, "", False))

            else:
                test_count = len(tests_result)

                if test_count == 0:
                    with self._lock:
                        html_plugin.HTML_report_manager.add_error(case_name, error=u'没有指定测试字段')
                    log.logger.info("case:{}完成报告写入".format(case_name))
                    self.__results.put((case_id, case_name, "", False))

                for result_key in tests_result:

                    result_key_uni = result_key.decode('utf8')
                    try:
                        assert tests_result[result_key]
                        status = True
                        with self._lock:
                            #  写入报告时,需要同步多线程
                            html_plugin.HTML_report_manager.add_success(case_name, result_key_uni, test_count)

                    except AssertionError:  # 验证失败
                        status = False
                        with self._lock:
                            html_plugin.HTML_report_manager.add_failure(case_name, result_key_uni, test_count)
                    finally:
                        log.logger.info("case:{}完成报告写入".format(case_name))
                        self.__results.put((case_id, case_name, result_key, status))

            self.__tasks.task_done()  # 任务池每完成一个任务,标记一次
        return

    def create_consumers(self, customer_count=0):
        """
            Summary:
                创建消费者
        :return:
        """
        consumer_count = customer_count or multithreading.cpu_count()
        consumer_list = list()
        for _ in range(consumer_count):
            curr_consumer = multithreading.Process(
                target=self.worker, args=())
            curr_consumer.daemon = True  # 设置为守护进程,主进程结束则子进程结束
            consumer_list.append(curr_consumer)
            curr_consumer.start()
        return consumer_list

    def get_results(self):
        """
            Summary:

        :return:
        """
        html_plugin.HTML_report_manager.finalize()  # 报告结尾, 完成报告写入, 创建报告(包括时间戳)
        return self.__results

    def run(self, thread_num=3):
        """

        用例执行,在当前进程内同步执行

        :param thread_num: 并发的线程数
        :return: report_create_time: 测试报告创建时间
        """
        self.RUNNING = True

        self.create_consumers(thread_num)
        tasks = self.producing()

        tasks.join()
        results = self.get_results()
        report_create_time = html_plugin.HTML_report_manager.get_report_create_time()

        while not results.empty():
            result = results.get_nowait()
            case_id, case_name, case_attr, status = result
            log.logger.info("第{}个case:\"{}\"的结果属性\"{}\"验证{}".format(
                case_id, case_name, case_attr, '成功' if status else '失败'))

        self.RUNNING = False
        return report_create_time

    def run_async(self, thread_num=3):
        """
        用例执行, 开启新的线程异步执行

        """

        new_thread = multithreading.Process(target=self.run, args=(thread_num,))
        new_thread.start()


test_runner = Runner()
