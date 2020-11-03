# -*- coding: utf-8 -*-
import datetime
import time

from redmine.common.base.config_operate import ReadConfig
from redmine.common.redmine_common import MyRedmine
from redmine.common.redmine_issue_status import MyIssueStatus
from redmine.common.redmine_trackers import MyTracker


class MyIssue:

    def __init__(self,redmine):
        self.myRedmine = redmine

    # remdine redmine对象
    # project_index 项目标识
    # tracker_id 跟踪标签id, None为不查询tracker_id
    def get_issues(self, project_index, tracker_id, status_name):
        if status_name is not None:
            myIssueStatus = MyIssueStatus()
            status = myIssueStatus.get_issueStatus_by_name(self.myRedmine, status_name)
            if status is not None:
                issues = self.myRedmine.issue.filter(project_id=project_index, tracker_id=tracker_id,
                                              status_id=status.id)
            else:
                print("无" + status_name + "对应的状态")
        else:
            issues = self.myRedmine.issue.filter(project_id=project_index, tracker_id=tracker_id, status_id='*')
        return issues


    def get_issues_by_query_id(self, project_index,query_id):
        issues = self.myRedmine.issue.filter(project_id=project_index, query_id=query_id,include=['children', 'journals', 'watchers'])
        return issues

    # 获取问题优先级
    def get_issue_priorites(self):
        issues_priorites = self.myRedmine.enumeration.filter(resource='issue_priorities')
        return issues_priorites

    def get_issue_by_tracker(self,issues,tracker_name):
        tracker_id = 0
        myTracker=MyTracker()
        trackers = myTracker.get_trackers();
        for t in trackers:
            if t.name == tracker_name:
                tracker_id = t.id
                break
        issues_t = issues.filter(tracker_id=tracker_id)
        return issues_t

    # 根据优先级筛选issue
    def get_issue_by_priority(self,issues, priority, issue_priority):
        for i in issues:
            if i.priority.id == priority.id:
                issue_priority[priority] = issues
        return issue_priority


    def stat_issue_by_assignTo(self,issues):
        # print(dir(issues))
        issuesByAssignTo = dict()
        for x in issues:
            assign_user = x.assigned_to.name
            if assign_user not in issuesByAssignTo.keys():
                issuesByAssignTo[assign_user] = 1
            else:
                issuesByAssignTo[assign_user] = issuesByAssignTo[assign_user] + 1
            print(issuesByAssignTo)
        return issuesByAssignTo


    def stat_issue_by_createOrClose_time(self,issues):
        issuesByCreateTime = dict()
        issuesByCloseTime = dict()
        issuesAll = dict()
        for x in issues:
            # 统计创建时间
            create_time = x.created_on.strftime('%Y-%m-%d')
            formate_create_time = datetime.datetime.strptime(create_time, '%Y-%m-%d')
            if formate_create_time not in issuesByCreateTime.keys():
                issuesByCreateTime[formate_create_time] = 1
            else:
                issuesByCreateTime[formate_create_time] = issuesByCreateTime[formate_create_time] + 1

            # 统计关闭时间
            if str(x.status.name) == 'Closed':
                close_time = x.closed_on.strftime('%Y-%m-%d')
                formate_close_time = datetime.datetime.strptime(close_time, '%Y-%m-%d')
                if formate_close_time not in issuesByCloseTime.keys():
                    issuesByCloseTime[formate_close_time] = 1
                else:
                    issuesByCloseTime[formate_close_time] = issuesByCloseTime[formate_close_time] + 1
        issuesAll['issuesByCreateTime'] = issuesByCreateTime
        issuesAll['issuesByCloseTime'] = issuesByCloseTime
        print(issuesAll)
        return issuesAll


    # 获取multimode的数据
    def get_issues_by_priority(self, issues):
        priorities = self.get_issue_priorites()
        final = {}
        for priority in priorities:
            pri_list = []
            for i in issues:
                try:
                    if str(i.priority.name) == priority.name:
                        pri_list.append(i.id)
                except Exception as e:
                    pass
            final[priority.name] = pri_list
        return final


    def get_issues_by_tracker(self,all_issues):
        final = {}
        tracker_list = []
        for x in all_issues:
            tracker_name = x.tracker.name
            # logmessage = '%s : %s' %(x.id,tracker_name)
            # print(logmessage)
            if tracker_name not in final.keys():
                tracker_list = []
            else:
                tracker_list = final[tracker_name]
            tracker_list.append(x.id)
            final[tracker_name] = tracker_list
        return final


    def get_issue_by_id(self, id):
        issue = self.myRedmine.issue.get(id)
        return issue

if __name__ == '__main__':
    # redmine_url = 'http://redmine.prod.dtstack.cn/'  # redmine 的地址
    # redmine_key = 'bfa6f11a1770b3c8358ce5e625f611a66aa796ee'  # 这个是自己redmine的key
    #     redmine_url = 'http://172.16.100.144:10083/'  # redmine 的地址
    #     redmine_key = 'bd565b470778bd172e3960727d23dbef7d204c49'  # 这个是自己redmine的key
    # project_name = 'online'
    # project_name = 'dataapi-v4-0-3_beta'
    # redmine = set_Redmine(redmine_url, redmine_key)
    # tracker_id = get_trackerId_by_name(redmine, "产品BUG")
    # all_issues = get_issues(redmine,project_name,None,None,None);
    # issues = get_issues(redmine, None, 128, tracker_id,'Resolved')
    # issues = get_issues_by_query_id(redmine, 128, tracker_id,'Resolved')
    # issues = get_issues_by_query_id(redmine, project_name,128)
    # issues = get_issues(redmine, None, 128, tracker_id,None)
    # issues = get_all_issues(redmine, project_name)
    # # issuesByAssignTo=stat_issue_by_assignTo(issues)
    # issuesAll = stat_issue_by_createOrClose_time(issues)
    # print(hybrid_API_multimode())
    # priorities = get_issue_priorites(redmine)
    # final = get_issues_by_priority(redmine,issues)
    # print(issues._total_count)
    # final = get_issues_by_tracker(all_issues)
    # print(final)
    # print(tracker_id)
    # myRedmine = MyRedmine()
    config = ReadConfig()
    myIssue = MyIssue()
    issues = myIssue.get_issues_by_query_id(config.REPORT_QUERY_ID)
    # get_recent_updated_issues(issues)
    # for i in issues:
    #     history = i.journals
    #     dir(history)
