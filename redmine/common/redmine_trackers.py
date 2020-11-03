from redmine.common.base.config_operate import ReadConfig
from redmine.common.redmine_common import MyRedmine


class MyTracker:
    def __init__(self,redmine):
        self.config = ReadConfig()
        self.redmine = redmine

    # 获取跟踪标签
    def get_trackers(self):
        trackers = self.redmine.tracker.all()
        return trackers


    def get_trackerId_by_name(self, name):
        trackers = self.get_trackers()
        for tracker in trackers:
            if tracker.name == name:
                return tracker.id