import json
import requests
import datetime
import turbosmsua 

turbo = turbosmsua.Turbosms('LOGIN', 'PASSWORD') # Логин и пароль для SOAP API сервиса turbosms
apiKey = 'API KEY' # ваш API ключ Новой Почты
date = datetime.date.today().strftime('%d.%m.%y') # сегодншняя дата. Или заменить на нужную в формате "дд.мм.гггг"
payload = {'apiKey': apiKey, 'modelName': 'InternetDocument', 'calledMethod': 'getDocumentList', 'DateTime': date}
sms = 'Ваш заказ прибудет {} по ТТН № {}' # шаблон sms сообщения
number = 'info' # здесь вписать номер или альфа имя с которого будут отправлены sms

r = requests.post('https://api.novaposhta.ua/v2.0/json/', data=json.dumps(payload))
j = r.json()

for x in j['data']:
    if x['ScanSheetNumber']: # Проверка, есть ли накладная в реестре отправлений. Так исключаются отменённые накладные
        print('Отправка смс за {}'.format(date))
        send = turbo.send_text(number, x['RecipientContactPhone'], sms.format(x['EstimatedDeliveryDate'].split(' ')[0], x['IntDocNumber']))
        print(x['IntDocNumber'], send['status'])
else:
    input('Всё выполнено. Нажмите enter, чтобы закрыть. ')
