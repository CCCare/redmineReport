# -*- coding: UTF-8 -*-
import datetime

from pyecharts import options as opts
from pyecharts.charts import Pie, Page
from pyecharts.charts import Line
import redmine_common


# 参考文档：https://pyecharts.org/
def draw_pie_bug_priority(redmineObj,issues):
    data = redmine_common.get_issues_by_priority(redmineObj,issues)
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
           .set_global_opts(title_opts=opts.TitleOpts(title="BUG优先级数据统计", subtitle="按Bug优先级分类"),
                            # legend_opts=opts.LegendOpts(pos_left="20%"),
                            # 工具箱配置项
                            toolbox_opts=opts.ToolboxOpts(is_show=True))
           .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))

           )
    return pie


def draw_pie_bug_agent(issues):
    issuesByAssignTo = redmine_common.stat_issue_by_assignTo(issues)
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
           .set_global_opts(title_opts=opts.TitleOpts(title="BUG经办人数据统计",
                                                      subtitle="按Bug经办人分类"),
                            # 工具箱配置项
                            toolbox_opts=opts.ToolboxOpts(is_show=True))
           .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
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
            .set_global_opts(title_opts=opts.TitleOpts(title="BUG创建时间和关闭时间对比图"),
                             # 工具箱配置项
                             toolbox_opts=opts.ToolboxOpts(is_show=True),
                             xaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                                                      is_scale=False,
                                                      boundary_gap=False
                                                      )
                             )
            )
    return line


def page_simple_layout(issues, issues_time):
    priority_bar = draw_pie_bug_priority(redmineObj,issues)
    assign_to_bar = draw_pie_bug_agent(issues)
    time_line = draw_line_bug_time(issues_time)
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        priority_bar,
        assign_to_bar,
        time_line
    )
    page.render("reports/redmine.html")

if __name__ == '__main__':
    redmine_url = 'http://redmine.prod.dtstack.cn/'  # redmine 的地址
    redmine_key = 'bfa6f11a1770b3c8358ce5e625f611a66aa796ee'  # 这个是自己redmine的key
    # project_name = 'stream-works'
    project_name = 'dataapi-v4-0-2_beta'  # redmine项目标识
    tracker_name = 'Bug'
    redmineObj = redmine_common.set_Redmine(redmine_url, redmine_key)
    tracker_id = redmine_common.get_trackerId_by_name(redmineObj, tracker_name)  # 跟踪标签需要手动填，不同项目跟踪标签不同
    query_id = None  # 自定义查询id
    issues = redmine_common.get_issues(redmineObj, project_name, query_id, tracker_id)
    issues_time = redmine_common.stat_issue_by_createOrClose_time(issues)
    page_simple_layout(issues, issues_time)
