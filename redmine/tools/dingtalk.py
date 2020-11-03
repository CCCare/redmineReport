from dingtalkchatbot.chatbot import DingtalkChatbot

template = ""
higher_bug_text = "### 新增高优先级BUG${n}个："

def send_dingtalk_markdown(webhook,title,text):
    if(text is not None or text != ''):
        dingtalk = DingtalkChatbot(webhook)
        dingtalk.send_markdown(title=title,text=text,at_mobiles=['15257183801','13738375762','18310593253'])

if __name__ == '__main__':
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=aff741f23bba7e599d512586944537f623464c46d75af860990e2c21435e7d37'  #填写你自己创建的机器人
    # dingtalk = DingtalkChatbot(webhook)
    # dingtalk.send_text(msg="【测试】我就是我, 是不一样的烟火")
    title = '线上BUG提醒'
    text = '# 测试这是支持markdown的文本 \n## 标题2  \n* 列表1 \n ![alt 啊](https://gw.alipayobjects.com/zos/skylark-tools/public/files/b424a1af2f0766f39d4a7df52ebe0083.png)'
    message = "【测试】我就是我, 是不一样的烟火"
    send_dingtalk_markdown(webhook,title,text)
