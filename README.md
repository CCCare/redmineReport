#### 准备工作
环境：python3.7

插件准备：

```
pip3 install python-redmine
pip3 install pyecharts
```

运行：
1. 修改redmine项目信息

```
redmine_url = 'http://redmine.prod.dtstack.cn/'  # redmine 的地址
redmine_key = 'bfa6f11a1770b3c8358ce5e625f611a66aa796ee'  # 这个是自己redmine的key
project_name = 'dataapi-v4-0-2_beta'  # redmine项目标识
tracker_name = 'Bug' # 跟踪标签名称，不同项目跟踪标签可能不同
```
2. 运行draw_charts.py

`python draw_charts.py
`
3. 打开redmine/reports/redmine.html即可查看报告
