import json
import datetime


def convertMs2String(milliseconds):
    dt = datetime.datetime.fromtimestamp(milliseconds )
    return dt

def convertJsonMessages2text(filename):
    with open(filename, "r", encoding="UTF8") as file:
        content = file.read()
    messages = json.loads(content)
    text = ""
    for m in messages:
        text += f"{convertMs2String(m['date'])} {m['message_id']}  {m['user_id']} {m['reply_message_id']}  {m['text']}  <br>\n"
    return text


if __name__ == "__main__":
    text = convertJsonMessages2text("d:/ml/chat/andromedica.json")
    print(text)
