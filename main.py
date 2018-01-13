import telepot
import threading
import time

settings = {
	'antibot':True,
	'antiforward':True,
	'messages_per_second':3,
	'token':'your_api_token_here',
	'private_settings':{
		'private':False,
		'groups':[],
	}
}

bot = telepot.Bot(settings['token'])
antiflood = {}

def private_setting():
	return settings['private_settings']['private'] == True

def private_allow(group):
	return group in settings['private_settings']['groups']

def delete(chat, ids, bot):
	try:
		for x in ids:
			bot.deleteMessage((chat, x))
			print("[i] " + str(chat) + " -> deleted " + str(x))
	except Exception as e:
		print("[!] Delete : " + str(e))

def antibot(msg):
	if settings['private_settings']['private'] and msg['chat']['id'] in settings['private_settings']['groups']:
		if 'new_chat_members' in msg:
			new = msg['new_chat_members']
			for x in new:
				if x['is_bot'] == True:
					chat = msg['chat']['id']
					bot.kickChatMember(chat, x['id'])
					print("[i] " + str(chat) + " -> banned bot " + str(x['id']))

def handle(msg):
	try:
		chat = msg['chat']['id']
		user = msg['from']['id']
		date = msg['date']
		msgid = msg['message_id']
		if settings['antiforward']:
			if 'forward_from_chat' in msg:
				if msg['forward_from_chat']['type'] == 'channel':
					delete(chat, [msgid], bot)
					print("[i] " + str(chat) + " -> deleted (forward) " + str(msgid))
					
		if not 'edit_date' in msg:
			if msg['chat']['type'] != 'private':
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

def magic(update):
	try:
		t1 = threading.Thread(target=handle, args=(update,),)
		t2 = threading.Thread(target=antibot, args=(update,),)
		if private_setting():
			if private_allow(str(update['chat']['id'])):
				t1.start()
				if settings['antibot']:
					t2.start()
			else:
				print("[i] Unallowed group ("+str(update['chat']['id'])+"), leaving... ")
				bot.leaveChat(update['chat']['id'])
		else:
			t1.start()
			if settings['antibot']:
				t2.start()
	except Exception as e:
		print("[!] Magic : " + str(e))



if __name__ == '__main__':
	print('\n'.join([" ____                  _                        ", "|  _ \                | |                       ", "| |_) | __ _ _ __ ___ | |__   ___   ___  _ __   ", "|  _ < / _` | '_ ` _ \| '_ \ / _ \ / _ \| '_ \  ", "| |_) | (_| | | | | | | |_) | (_) | (_) | | | | ", "|____/ \__,_|_| |_| |_|_.__/ \___/ \___/|_| |_| "]))
	print('          - created by TheFamilyTeam -')
	print("\n[i] Token: " + settings['token'])
	print("[i] Antibot: " + ('Yes' if settings['antibot'] else 'No'))
	print("[i] Private Mode: " + ('Yes' if private_setting() else 'No') + " (" + (', '.join(settings['private_settings']['groups']) if settings['private_settings']['groups'] else "No groups") + ")")
	print("====================")
	try:
		bot.message_loop(magic)
	except Exception as e:
		print("[!] Loop : " + str(e))

	while 1:
		try:
			time.sleep(10)
			antiflood = {}
		except KeyboardInterrupt:
			print("====================\n[i] Goodbye!")
			exit()
