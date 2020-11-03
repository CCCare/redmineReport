# -*- coding: utf-8 -*-

import configparser
import os


class ReadConfig:
    """定义一个读取配置文件的类"""

    REDMINE_URL=""
    REDMINE_KEY=""
    REDMINE_PROJECT=""

    REPORT_PROJECT=""
    REPORT_QUERY_ID=0
    REPORT_TRACKER_NAME=""

    ALARM_PROJECT=""
    ALARM_PRIORITIES=[]
    ALARM_QUERY={}
    HOUR_DIFF=0
    DAY_DIFF=0

    WEBHOOK=""
    IS_SEND_TO_DINGTALK=False
    MESSAGE_TITLE = ""

    def __init__(self,isTest=False):
        cf = self.read_configFile()

        # 读取redmine配置
        self.REDMINE_URL = cf.get('redmine_dtstack','redmine_url')
        self.REDMINE_KEY = cf.get('redmine_dtstack','redmine_key')
        self.REDMINE_PROJECT = cf.get('redmine_dtstack','redmine_project')

        self.REPORT_PROJECT = cf.get('qa_report','report_project_index')
        self.REPORT_QUERY_ID = int(cf.get('qa_report','report_query_id'))
        self.REPORT_TRACKER_NAME = cf.get('qa_report','report_tracker_name')

        # 读取线上问题提醒配置
        self.ALARM_PROJECT = cf.get('online_alarm','alarm_project')
        self.ALARM_PRIORITIES = cf.get('online_alarm','alarm_priorities').split(",")
        alarm_query_groups = cf.get('online_alarm','alarm_query_group').split(",")
        alarm_query_ids = cf.get('online_alarm', 'alarm_query_id').split(",")
        for i in range (len(alarm_query_groups)):
            self.ALARM_QUERY[alarm_query_groups[i]] = int(alarm_query_ids[i])

        # self.ALARM_QUERY_GROUP = cf.get('online_alarm','alarm_query_group')
        # self.ALARM_QUERY_ID = cf.get('online_alarm','alarm_query_id')
        self.HOUR_DIFF = int(cf.get('online_alarm','hour_diff'))
        self.DAY_DIFF = int(cf.get('online_alarm','day_diff'))

        # 读取钉钉机器人配置
        if isTest:
            self.WEBHOOK = cf.get('test_dingTalk','webhook')
            self.IS_SEND_TO_DINGTALK = cf.get('test_dingTalk','is_send_to_dingTalk')
            self.MESSAGE_TITLE = cf.get('test_dingTalk', 'title')
        else:
            self.WEBHOOK = cf.get('formal_dingTalk', 'webhook')
            self.IS_SEND_TO_DINGTALK = cf.get('formal_dingTalk', 'is_send_to_dingTalk')
            self.MESSAGE_TITLE = cf.get('formal_dingTalk', 'title')


    def read_configFile(self):
        cf = configparser.ConfigParser()
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # print("path:"+path)
        # redmineConfFile = os.path.abspath(os.path.join(os.getcwd(), '../../../', 'conf', 'redmine.cfg'))
        # dingTalkConfFile = os.path.abspath(os.path.join(os.getcwd(), '../../../', 'conf', 'dingTalk.cfg'))
        redmineConfFile = os.path.join(path, '../../conf/redmine.cfg')
        dingTalkConfFile = os.path.join(path, '../../conf/dingTalk.cfg')
        cf.read(redmineConfFile, encoding="utf-8")
        cf.read(dingTalkConfFile, encoding="utf-8")
        return cf

if __name__ == '__main__':
    config=ReadConfig()

    print("读取配置文件完成>>>")
    print(config.REDMINE_URL)