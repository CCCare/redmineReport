from redmine.common.base.config_operate import ReadConfig
from redmine.common.redmine_common import MyRedmine


class MyIssueStatus:
    def __init__(self,redmine):
        self.redmine = redmine

    def get_all_issueStatuses(self):
        statuses = self.redmine.issue_status.all()
        print(statuses)
        return statuses

    def get_issueStatus_by_name(self,name):
        statuses = self.redmine.issue_status.all()
        for status in statuses:
            if(status.name == name):
                return status

if __name__ == '__main__':
    myIssueStatus = MyIssueStatus()
    myIssueStatus.get_all_issueStatuses()
    status_name = "Resolved"
    status = myIssueStatus.get_issueStatus_by_name(status_name)
    print(status)