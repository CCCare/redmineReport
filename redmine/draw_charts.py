# -*- coding: UTF-8 -*-
import datetime

from pyecharts import options as opts
from pyecharts.charts import Pie, Page
from pyecharts.charts import Line

# 参考文档：https://pyecharts.org/
from redmine.common.base.config_operate import ReadConfig
from redmine.common.redmine_common import MyRedmine
from redmine.common.redmine_issues import MyIssue
from redmine.common.redmine_trackers import MyTracker


def draw_pie_bug_priority(priority_data):
    data = priority_data
    cate = data.keys()
    v = []
    final = []
    for i in cate:
        u = data.get(i)
        v.append(len(u))
    final.append(cate)
    final.append(v)

    pie = (Pie()
           .add('', [list(z) for z in zip(cate, v)],
                radius=["30%", "75%"],
                rosetype="radius")
           .set_global_opts(title_opts=opts.TitleOpts(title="BUG优先级统计图", subtitle="按优先级统计BUG"),
                            # legend_opts=opts.LegendOpts(pos_left="20%"),
                            # 工具箱配置项
                            toolbox_opts=opts.ToolboxOpts(is_show=True))
           .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}({d}%)"))

           )
    return pie

def draw_pie_bug_tracker(tracker_bug_data):
    # all_issues = redmine_common.get_issues(redmineObj, project_name, None, None);
    data = tracker_bug_data
    cate = data.keys()
    v = []
    final = []
    for i in cate:
        u = data.get(i)
        v.append(len(u))
    final.append(cate)
    final.append(v)

    pie = (Pie()
           .add('', [list(z) for z in zip(cate, v)],
                radius=["30%", "75%"],
                rosetype="radius")
           .set_global_opts(title_opts=opts.TitleOpts(title="跟踪标签统计图", subtitle="按跟踪标签统计issue"),
                            # legend_opts=opts.LegendOpts(pos_left="20%"),
                            # 工具箱配置项
                            toolbox_opts=opts.ToolboxOpts(is_show=True))
           .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}({d}%)"))

           )
    return pie


def draw_pie_bug_agent(issues):
    issuesByAssignTo = issues
    assignNames = issuesByAssignTo.keys()
    v = []
    for i in assignNames:
        u = issuesByAssignTo.get(i)
        v.append(u)

    pie = (Pie()
           .add('',
                [list(z) for z in zip(assignNames, v)],
                radius=["30%", "75%"],
                rosetype="radius")
           .set_global_opts(title_opts=opts.TitleOpts(title="指派人统计图",
                                                      subtitle="按指派人统计BUG"),
                            # 工具箱配置项
                            toolbox_opts=opts.ToolboxOpts(is_show=True))
           .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}({d}%)"))
           )
    return pie


def draw_line_bug_time(issue):
    issuesByCreateTime = issue['issuesByCreateTime']
    issuesByCloseTime = issue['issuesByCloseTime']
    tmpTime = list(issuesByCreateTime.keys())
    tmpTime.extend(list(issuesByCloseTime.keys()))
    tmpTime.sort()
    minTime = min(tmpTime)
    maxTime = max(tmpTime)
    print("最小时间：" + minTime.strftime('%Y-%m-%d'))
    print("最大时间：" + maxTime.strftime('%Y-%m-%d'))
    xTime = []
    create_kv = []
    close_kv = []
    # xTime = [
    #     str(minTime + datetime.timedelta(days=i))
    #     for i in range((maxTime - minTime).days + 1)
    # ]
    for i in range((maxTime - minTime).days + 1):
        # iTime = minTime + datetime.timedelta(days=i)
        iTime = str(minTime + datetime.timedelta(days=i))
        xTime.append(iTime)
        formate_itime = datetime.datetime.strptime(iTime, '%Y-%m-%d %H:%M:%S')
        if formate_itime not in issuesByCreateTime.keys():
            issuesByCreateTime[formate_itime] = 0
        if formate_itime not in issuesByCloseTime.keys():
            issuesByCloseTime[formate_itime] = 0

    # 根据时间排序
    sortedIssuesByCreateTime = dict(
        [(k, issuesByCreateTime[k]) for k in sorted(issuesByCreateTime.keys())]
    )
    # 根据时间排序
    sortedIssuesByCloseTime = dict(
        [(k, issuesByCloseTime[k]) for k in sorted(issuesByCloseTime.keys())]
    )
    print(xTime)
    print(sortedIssuesByCreateTime.values())
    print(sortedIssuesByCloseTime.values())
    line = (Line()
            .add_xaxis(xTime)
            .add_yaxis("创建时间", sortedIssuesByCreateTime.values(), is_smooth=True)
            .add_yaxis("关闭时间", sortedIssuesByCloseTime.values(), is_smooth=True)
            .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                             label_opts=opts.LabelOpts(is_show=False)
                             )
            .set_global_opts(title_opts=opts.TitleOpts(title="创建时间和关闭时间对比图",subtitle="按创建时间/关闭时间统计BUG响应趋势"),
                             # 工具箱配置项
                             toolbox_opts=opts.ToolboxOpts(is_show=True),
                             xaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                                                      is_scale=False,
                                                      boundary_gap=False
                                                      )
                             )
            )
    return line


def page_simple_layout(redmineObj, project_name,query_id,tracker_name):
    myIssue = MyIssue(redmine)
    myTracker = MyTracker(redmine)
    # 数据获取
    if query_id is not None:
        all_issues = myIssue.get_issues_by_query_id(redmineObj,project_name,query_id)
    else:
        all_issues = myIssue.get_issues(project_name, None,None)  # 根据项目或者根据自定义查询id获取所有issue
        tracker_id = myTracker.get_trackerId_by_name(tracker_name)  # 跟踪标签需要手动填，不同项目跟踪标签不同
        issues = myIssue.get_issues(project_name, tracker_id, None)  # 根据tacker_id获取项目内或者自定义查询内的issue
    issues_time = myIssue.stat_issue_by_createOrClose_time(issues) # 获取issues中的创建时间和关闭时间
    priority_data = myIssue.get_issues_by_priority(issues)
    assign_to_data = myIssue.stat_issue_by_assignTo(issues)
    tracker_bug_data = myIssue.get_issues_by_tracker(all_issues)

    # 制作统计图
    priority_pie = draw_pie_bug_priority(priority_data) # 按优先级统计BUG
    assign_to_pie = draw_pie_bug_agent(assign_to_data) # 按指派人统计BUG
    time_line = draw_line_bug_time(issues_time) # 按创建时间/关闭时间统计BUG
    tracker_pie = draw_pie_bug_tracker(tracker_bug_data) # 按跟踪标签统计Issue
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        tracker_pie,
        priority_pie,
        assign_to_pie,
        time_line
    )
    page.render("./reports/redmine.html")

if __name__ == '__main__':
    config = ReadConfig()
    redmine = MyRedmine(config.REDMINE_URL,config.REDMINE_KEY).redmine
    query_id = None  # 自定义查询id
    page_simple_layout(redmine,config.REPORT_PROJECT,query_id,config.REPORT_TRACKER_NAME)
