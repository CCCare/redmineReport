# -*- coding: utf-8 -*-
import datetime
import time
from redminelib import Redmine


# issues = []
# settings redmine,redmine's url :http://python-redmine.readthedocs.org/
def set_Redmine(redmine_url, redmine_key):
    redmine = Redmine(redmine_url, key=redmine_key)
    return redmine


def swich_project(redmine, project_name):
    global project
    project = redmine.project.get(project_name)


def get_all_issues(redmine, project_name):
    issues = redmine.issue.filter(project_id=project_name, status_id='*')
    # print(dir(issues))
    return issues


# remdine redmine对象
# project_name 项目标识
# query_id 查询id
# tracker_id 跟踪标签id
def get_issues(redmine, project_name, query_id, tracker_id):
    issues = redmine.issue.filter(project_id=project_name, query_id=query_id, tracker_id=tracker_id, status_id='*')
    return issues


# 获取问题优先级
def get_issue_priorites(redmine):
    issues_priorites = redmine.enumeration.filter(resource='issue_priorities')
    return issues_priorites._resources


# 获取跟踪标签
def get_trackers(redmine):
    trackers = redmine.tracker.all()
    return trackers


def get_trackerId_by_name(redmine, name):
    trackers = get_trackers(redmine)
    for tracker in trackers:
        if tracker.name == name:
            return tracker.id


def get_issue_by_tracker(issues, tracker_name):
    tracker_id = 0
    trackers = get_trackers();
    for t in trackers:
        if t.name == tracker_name:
            tracker_id = t.id
            break
    issues_t = issues.filter(tracker_id=tracker_id)
    return issues_t


# 根据优先级筛选issue
def get_issue_by_priority(issues, priority, issue_priority):
    for i in issues:
        if i.priority.id == priority.id:
            issue_priority[priority] = issues
    return issue_priority


# 根据问题优先级分类
def classify_bug_issue_priorities(issues, priorities):
    priority_class = {}
    issue_priority = {}
    for p in priorities:
        get_issue_by_priority(issues, p, issue_priority)


def stat_issue_by_assignTo(issues):
    print(dir(issues))
    issuesByAssignTo = dict()
    for x in issues:
        assign_user = x.assigned_to.name
        if assign_user not in issuesByAssignTo.keys():
            issuesByAssignTo[assign_user] = 1
        else:
            issuesByAssignTo[assign_user] = issuesByAssignTo[assign_user] + 1
        print(issuesByAssignTo)

    return issuesByAssignTo


def stat_issue_by_createOrClose_time(issues):
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
def hybrid_API_multimode(issues):
    Low = []
    Normal = []
    High = []
    Urgent = []
    Immediate = []
    openlist = []
    closelist = []
    for i in issues:
        try:
            if str(i.tracker.name) == 'Bug' and str(i.priority.name) == "Low":
                Low.append(i.id)
            elif str(i.tracker.name) == 'Bug' and str(i.priority.name) == "Normal":
                Normal.append(i.id)
            elif str(i.tracker.name) == 'Bug' and str(i.priority.name) == "High":
                High.append(i.id)
            elif str(i.tracker.name) == 'Bug' and str(i.priority.name) == "Urgent":
                Urgent.append(i.id)
            elif str(i.tracker.name) == 'Bug' and str(i.priority.name) == "Immediate":
                Immediate.append(i.id)
            if str(i.tracker.name) == 'Bug' and str(i.status.name) == "New":
                openlist.append(i.id)
            if str(i.tracker.name) == 'Bug' and str(i.status.name) != "New":
                closelist.append(i.id)
        except Exception as e:
            pass
    final = {"Low": Low, "Normal": Normal, "High": High, "Urgent": Urgent, "Immediate": Immediate}

    return final


# 获取search的数据
def hybrid_API_serach(issues):
    Low = []
    Normal = []
    High = []
    Urgent = []
    Immediate = []
    openl = []
    colsel = []
    for i in issues():
        try:
            if str(i.tracker.name) == 'Bug' and str(i.priority) == "Low":
                Low.append(i)
            elif str(i.tracker.name) == 'Bug' and str(i.priority) == "Normal":
                Normal.append(i)
            elif str(i.tracker.name) == 'Bug' and str(i.priority) == "High":
                High.append(i)
            elif str(i.tracker.name) == 'Bug' and str(i.priority) == "Urgent":
                Urgent.append(i)
            elif str(i.tracker.name) == 'Bug' and str(i.priority) == "Immediate":
                Immediate.append(i)
            if str(i.tracker.name) == 'Bug' and str(i.status) == "New":
                openl.append(i)
            if str(i.tracker.name) == 'Bug' and str(i.status) != "New":
                colsel.append(i)
        except Exception as e:
            print(e)
    return len(Low), len(Normal), len(High), len(Urgent), len(Immediate), len(openl), len(colsel)


# 获取route&traffic的数据
def hybrid_API_route_traffic(issues):
    Low = []
    Normal = []
    High = []
    Urgent = []
    Immediate = []
    openl = []
    closel = []
    for i in issues:
        print(i)
        try:
            if str(i.tracker.name) == 'Bug' and str(i.priority) == "Low":
                Low.append(i)
            elif str(i.tracker.name) == 'Bug' and str(i.priority) == "Normal":
                Normal.append(i)
            elif str(i.tracker.name) == 'Bug' and str(i.priority) == "High":
                High.append(i)
            elif str(i.tracker.name) == 'Bug' and str(i.priority) == "Urgent":
                Urgent.append(i)
            elif str(i.tracker.name) == 'Bug' and str(i.priority) == "Immediate":
                Immediate.append(i)
            if str(i.tracker.name) == 'Bug' and str(i.status) == "New":
                openl.append(i)
            if str(i.tracker.name) == 'Bug' and str(i.status) != "New":
                closel.append(i)
        except Exception as e:
            print(e)
    return len(Low), len(Normal), len(High), len(Urgent), len(Immediate), len(openl), len(closel)


if __name__ == '__main__':
    redmine_url = 'http://redmine.prod.dtstack.cn/'  # redmine 的地址
    redmine_key = 'bfa6f11a1770b3c8358ce5e625f611a66aa796ee'  # 这个是自己redmine的key
    project_name = 'online'
    # project_name = 'dataapi-v4-0-2_beta'
    redmine = set_Redmine(redmine_url, redmine_key)
    tracker_id = get_trackerId_by_name(redmine, "产品BUG")
    issues = get_issues(redmine, project_name, None, tracker_id)
    # issuesByAssignTo=stat_issue_by_assignTo(issues)
    issuesAll = stat_issue_by_createOrClose_time(issues)
    # print(hybrid_API_multimode())
    print(issuesAll)

    print(tracker_id)
