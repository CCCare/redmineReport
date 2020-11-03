# -*- coding: utf-8 -*-
import datetime
import time
from redminelib import Redmine
from redmine.common.base.config_operate import ReadConfig


class MyRedmine:

    global redmine

    def __init__(self,redmine_url,redmine_key):
        self.redmine = self.set_redmine(redmine_url,redmine_key)

    def set_redmine(self,redmine_url, redmine_key):
        redmine = Redmine(redmine_url, key=redmine_key)
        return redmine

if __name__ == '__main__':
    config = ReadConfig()
    myRedmine=MyRedmine(config.REDMINE_URL,config.REDMINE_KEY)
    print(myRedmine.redmine)
