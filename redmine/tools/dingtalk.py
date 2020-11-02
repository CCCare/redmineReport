from dingtalkchatbot.chatbot import DingtalkChatbot

template = ""
higher_bug_text = "### 新增高优先级BUG${n}个："

def send_dingtalk_markdown(webhook,title,text):
    if(text is not None or text != ''):
        dingtalk = DingtalkChatbot(webhook)
        print(text)
        # dingtalk.send_text(msg=message)
        dingtalk.send_markdown(title=title,text=text)

if __name__ == '__main__':
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=1327a4db1da11ec25e51569678f69241039e18e1426301e535b73961643ee665'  #填写你自己创建的机器人
    # dingtalk = DingtalkChatbot(webhook)
    # dingtalk.send_text(msg="【测试】我就是我, 是不一样的烟火")
    title = '线上BUG提醒'
    text = '# 测试这是支持markdown的文本 \n## 标题2  \n* 列表1 \n ![alt 啊](https://gw.alipayobjects.com/zos/skylark-tools/public/files/b424a1af2f0766f39d4a7df52ebe0083.png)'
    message = "【测试】我就是我, 是不一样的烟火"
    send_dingtalk_markdown(webhook,title,text)
