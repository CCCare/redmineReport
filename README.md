#### 准备工作
环境：python3.7

插件准备：

```
pip3 install python-redmine
pip3 install pyecharts
```

工具：PyCharm

运行：
1. 修改redmine项目信息

```
redmine_url = 'http://redmine.prod.dtstack.cn/'  # redmine 的地址
redmine_key = 'bfa6f11a1770b3c8358ce5e625f611a66aa796ee'  # 这个是自己redmine的key, redmine页面点击“我的账号”-点击右侧的“API访问键”的“显示”，即可查看
project_name = 'dataapi-v4-0-2_beta'  # redmine项目标识
tracker_name = 'Bug' # 跟踪标签名称，不同项目跟踪标签可能不同
query_id = None  # （int类型）可以根据redmine中设置的自定义查询，作为统计的样本；传None即不通过自定义查询获取样本
```
2. 运行draw_charts.py

进入到工程下的redminereport/redmine目录中，执行下面命令：

`python draw_charts.py
`

3. 打开redmine/reports/redmine.html即可查看报告

4. 统计维度：
(1). 按跟踪标签
(2). 按BUG优先级
(3). 按BUG经办人
(4). BUG创建时间和关闭时间对比