import telepot
import threading
import time

settings = {
	'messages_per_second':3,
	'token':'your_bot_api_token_here'
}

bot = telepot.Bot(settings['token'])
antiflood = {}

def delete(chat, ids, bot):
	try:
		for x in ids:
			bot.deleteMessage((chat, x))
			print("[i] " + str(chat) + " -> deleted " + str(x))
	except Exception as e:
		print("[!] Delete : " + str(e))

def handle(msg):
	try:
		chat = msg['chat']['id']
		user = msg['from']['id']
		date = msg['date']
		msgid = msg['message_id']
		if  msg['chat']['type'] != 'private':
			if not chat in antiflood:
				antiflood[chat] = {}
		
			if not user in antiflood[chat]:
				antiflood[chat][user] = {}

			if not date in antiflood[chat][user]:
				antiflood[chat][user][date] = []

			wd = antiflood[chat][user][date]
			wd.append(msgid)

			if len(wd) >= settings['messages_per_second']:
				bot.kickChatMember(chat, user)
				print("[i] " + str(chat) + " -> banned " + str(user))
				t = threading.Thread(target=delete, args=(chat, wd, bot,),)
				t.start()
	except Exception as e:
		print("[!] Bamboon : " + str(e))

if __name__ == '__main__':
	print('\n'.join([" ____                  _                        ", "|  _ \                | |                       ", "| |_) | __ _ _ __ ___ | |__   ___   ___  _ __   ", "|  _ < / _` | '_ ` _ \| '_ \ / _ \ / _ \| '_ \  ", "| |_) | (_| | | | | | | |_) | (_) | (_) | | | | ", "|____/ \__,_|_| |_| |_|_.__/ \___/ \___/|_| |_| "]))
	print('          - created by TheFamilyTeam -')
	print("\n[i] Token: " + settings['token'])
	print("====================")
	try:
		bot.message_loop(handle)
	except Exception as e:
		print("[!] Loop : " + str(e))

	while 1:
		try:
			time.sleep(10)
			antiflood = {}
		except KeyboardInterrupt:
			print("====================\n[i] Goodbye!")
			exit()
