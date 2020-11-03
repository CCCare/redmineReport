#### 准备工作
环境：python3.7

插件准备：

```
pip3 install python-redmine
pip3 install pyecharts
pip3 install DingtalkChatbot
pip3 install schedule
```

工具：PyCharm

运行：
1. 修改配置文件<br>
conf/redmine.cfg <br>
(1) `redmine_dtstack`模块为redmine地址及验证信息，默认不用修改 <br>
(2) `qa_report`模块为生成报告所需的一些配置信息 <br>
(3) `online_alarm`模块为线上问题提醒的配置信息 <br>
conf/dingTalk.cfg<br>
该配置文件用于配置钉钉机器人发送消息<br>

2. 生成日常项目测试报告<br>
(1). 进入到工程下的redminereport/redmine/目录中，执行下面命令：

`python draw_charts.py
`

(2). 打开redmine/reports/redmine.html即可查看报告<br>
(3). 统计维度：
* 按跟踪标签
* 按BUG优先级
* 按BUG经办人
* BUG创建时间和关闭时间对比

3. 线上问题提醒<br>
进入redmine/alarm执行alarm_bug.py即可发送消息
