import requests, bs4, slackweb, os

# URL・トークンの定義
url = "https://transit.yahoo.co.jp/traininfo/area/6/"
slack = slackweb.Slack(url=os.environ['SLACK_URL'])

def lambda_handler(event, context):

    response = {
        'statusCode': 200,
        'isBase64Encoded': False,
        'headers': {'Content-Type': 'application/json'},
        'body': 'done'
    }

    fetch_result = data_fetch(url)

    # 取得先のタイトルを取得
    title = fetch_result.title.get_text()


    # 遅延情報の取得
    delay_info = fetch_result.find(id='mdStatusTroubleLine').find_all('a')
    delay_info_text = ''
    for info in delay_info:
        delay_info_text += "\n" + info.get_text() + "\n" + info.get('href')

    slack_send(slack, title, delay_info_text)

    return response

# slackに情報の送信
def slack_send(slack, title , text):
    attachments = []
    attachment = {
        "color":"#D00000",
        "title": title,
        "text": text,
        "mrkdwn_in": ["text", "pretext"]
    }
    attachments.append(attachment)
    slack.notify(attachments=attachments)

    return

# requestsでデータをスクレイピング   
def data_fetch(url):
    get_url = requests.get(url)
    bs4_obj = bs4.BeautifulSoup(get_url.text, 'html.parser')

    return bs4_obj