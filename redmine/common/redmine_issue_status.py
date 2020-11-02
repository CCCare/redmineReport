
from redmine.common.redmine_common import set_Redmine

def get_all_issueStatuses(redmine):
    statuses = redmine.issue_status.all()
    print(statuses)
    return statuses

def get_issueStatus_by_name(redmine,name):
    statuses = redmine.issue_status.all()
    for status in statuses:
        if(status.name == name):
            return status

if __name__ == '__main__':
    redmine_url = 'http://redmine.prod.dtstack.cn/'  # redmine 的地址
    redmine_key = 'bfa6f11a1770b3c8358ce5e625f611a66aa796ee'  # 这个是自己redmine的key
    redmine = set_Redmine(redmine_url, redmine_key)
    get_all_issueStatuses(redmine)
    status_name = "Resolved"
    status = get_issueStatus_by_name(redmine,status_name)
    print(status)