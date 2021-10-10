from Penger.penger import Penger, Accordance
import tgbotSettings as tS
import json
import time

p = Penger(token = tS.token)


def start_command(self):
	text = tS.start_text
	p.sendMessageToChat(self.data, text)
	text = tS.dev_text_ru
	p.sendMessageToChat(self.data, text)


def help_command(self):
	text = tS.help_text
	p.sendMessageToChat(self.data, text)


def sources_command(self):
	text = tS.sources_text
	p.sendMessageToChat(self.data, text)


def latest_command(self):
	print(self.data)

	arg = "1"

	if len(self.data['text'].split()) > 1:
		arg = str(self.data['text'].split()[1])

	if arg.isdigit():
		if int(arg) >= 0 and int(arg) <=15:
			arg = int(arg)

			news_data = None

			with open('latest_news.json', "r") as file:
				news_data = json.load(file)

			for x in range(0,arg):
				s = ''

				s += news_data[x]["title"]
				s += '\n'
				s += '\n'
				s += "Published: " + news_data[x]['date']
				s += '\n'
				s += '\n'
				s += news_data[x]['smal_text']
				s += '\n'
				s += news_data[x]['url']

				p.sendMessageToChat(self.data, s)

				time.sleep(1)
		else:
			# p.sendMessageToChat(self.data, 'Invalid argument! The number must be from 0 to 15 inclusive.')
			p.sendMessageToChat(self.data, 'Неправильный аргумент! Им должно быть число от 0 до 15 включительно.\nНапример, ```/latest 7```')

	else:
		# p.sendMessageToChat(self.data, 'Invalid argument! The first argument must be a number from 0 to 15 inclusive.')
		p.sendMessageToChat(self.data, 'Неправильный аргумент! Им должно быть число от 0 до 15 включительно.\nНапример, [ /latest 7 ]')


def empty(data):
	# p.sendMessageToChat(data, 'I do not understand...')
	p.sendMessageToChat(data, 'Эту команду я не понимаю...\n\nО доступных командах можно узнать отправив мне /help')


def on_subscription_command(self):
	# p.sendMessageToChat(self.data, "You have subscribed to notifications about new publications! Thank You!")
	p.sendMessageToChat(self.data, "Вы подписались на уведомления о новых публикациях! Спасибо!")
	text = tS.dev_text_ru
	p.sendMessageToChat(self.data, text)


def off_subscription_command(self):
	# p.sendMessageToChat(self.data, "You have unsubscribed from notifications about new publications... :-(")
	p.sendMessageToChat(self.data, "Вы отписались от уведомлений о новых публикациях... :-(")
	p.sendMessageToChat(self.data, "Бот очень надеется, что вы снова подпишетесь командой /on.")
	pass


p.accordance = [
	Accordance('/start', start_command, 'all:all', enableArgument=True),
	Accordance('/help', help_command, 'all:all', enableArgument=True),
	Accordance('/sources', sources_command, 'all:all', enableArgument=True),
	Accordance('/on', on_subscription_command, 'all:all', enableArgument=True),
	Accordance('/off', off_subscription_command, 'all:all', enableArgument=True),
	Accordance('/latest', latest_command, 'all:all', enableArgument=True)
]
p.emptyAccordance = empty


def main():
	while True:
		p.updateAndRespond()
		time.sleep(10)


if __name__ == '__main__':
	main()
