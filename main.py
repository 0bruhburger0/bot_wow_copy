import discord, config, asyncio, system, math, qiwi, random
from discord.ext import commands
from operator import itemgetter
from db import history_customer, get_all_orders, history_executor, ended, update8, update9, not_conf, active_orders_customer, active_orders_executor, get_order_id, get_order, get_executor, get_customer, update, cerate_executor, create_order, cerate_customer

bot = commands.Bot(command_prefix='!')

wait_run = []

channels_id = [669078856367341598, 704626948202299442, 671341565456810004, 675648277835677696, 
751682915208790137, 688345898094297119, 673235237739692060, 682259752436498446, 705136741735989379,
752962129442898130, 752962071695589396]


@bot.command()
async def role(ctx):
	if int(ctx.channel.id) == 669078856367341598:
		cerate_executor(int(ctx.message.author.id), str(ctx.message.author.name))
		user_id = int(ctx.message.author.id)
		roles = {'Below 500': 500, '1000+ Mythic+ Score': 1000, '1500+ Mythic+ Score': 1500, '2000+ Mythic+ Score': 2000,
		'2500+ Mythic+ Score': 2500, '3000+ Mythic+ Score': 3000, '3500+ Mythic+ Score': 3500}
		# print(ctx.message.author.roles)
		for role in roles:
			for i in ctx.message.author.roles:
				if str(i) == str(role):
					update("executors", "score", roles[role], user_id)
					print(role)


@bot.command()
async def stat(ctx, order_id):
	if int(ctx.channel.id) not in channels_id:
		order = get_order_id(order_id)
		print(order)
		if order['step'] == 9:
			if order['customer_id'] == int(ctx.message.author.id):
				list_roles = system.return_roles_cnt(order_id)
				embedVar = discord.Embed(title=f"Статистика по ролям для заказа №{order_id}:", description=list_roles, color=000000)
				await ctx.send(embed=embedVar)
			else:
				await ctx.send('Для тебя не доступна эта команда')
		else:
			await ctx.send(f'Заказ №{order_id} уже собран или закончен.')


@bot.command()
async def reg(ctx, order_id, code_room):
	if int(ctx.channel.id) not in channels_id:
		order = get_order_id(order_id)
		if int(order['step']) == 9:
			waiting_group = eval(order['waiting_group'])
			for wg in waiting_group:
				rating = get_executor['score']
				if rating != None:
					if int(wg) == int(code_room):
						item = waiting_group[wg]
						item.append(int(ctx.message.author.id))
					await ctx.send(f'Ты зарегистрирован в заказ №{order_id}')
				else:
					await ctx.send(f'У тебя нет роли, её можно получить в канале #paздача-ролей')
		else:
			await ctx.send('Ты ошибся заказом.')


@bot.command()
async def help_customer(ctx):
	embedVar = discord.Embed(title="Командны для заказчиков:", description="Support - PayBot#9110", color=000000)
	embedVar.add_field(name="Создание заказа:", value="!new_order [уровень ключа] [кол-во участников]\nБыстрый заказ: !new_order [уровень ключа] [кол-во участников] @[Фракция] @[Роль-Броня-Название ключа] @[Роль-Броня] @[Роль-Броня-Количество ролей] [ссылка] [комментарий]", inline=False)
	embedVar.add_field(name="Комментарий к заказу", value="!comment [комментарий]", inline=False)
	embedVar.add_field(name="Отменить заказ:", value="!close", inline=False)
	embedVar.add_field(name="История заказов:", value="!his", inline=False)
	embedVar.add_field(name="Изменить платежный токен:", value="!choose_token [платежный токен qiwi]", inline=False)
	embedVar.add_field(name="Юзер-панель:", value="!panel", inline=False)
	embedVar.add_field(name="Подтвердить заказ:", value="!end [id заказа]", inline=False)
	embedVar.add_field(name="Отклонить заказ:", value="!not_accept [id заказа] [причина]", inline=False)
	embedVar.add_field(name="Поcмотреть кол-во зарегистрировавшихся в заказ:", value="!stat [id заказа]", inline=False)
	embedVar.add_field(name="Оплатить заказ:", value="!pay [id заказа] - оплатить один заказ\n!pay all - оплатить все заказы", inline=False)
	await ctx.send(embed=embedVar)


@bot.command()
async def help_executor(ctx):
	embedVar = discord.Embed(title="Командны для исполнителей:", description="Support - PayBot#9110", color=000000)
	embedVar.add_field(name="Юзер-панель:", value="!cab", inline=False)
	embedVar.add_field(name="История заказов:", value="!history", inline=False)
	embedVar.add_field(name="Выбрать кошелёк:", value="!choose_wallet [номер qiwi кошелька]", inline=False)
	embedVar.add_field(name="Отправить заказ на проверку:", value="!prof [id заказа] [ссылка на скрин-доказательство]", inline=False)
	embedVar.add_field(name="Сообщение заказчику:", value="!msg [id заказа] [сообщение]", inline=False)
	embedVar.add_field(name="Получить/обновить роль на сервере:", value="!role update", inline=False)
	embedVar.add_field(name="Регистрация в групповой заказ:", value="!reg [id заказа] [код, который выдается лидеру]", inline=False)
	await ctx.send(embed=embedVar)


# @bot.command()
# async def cancel_order(ctx):
# 	if int(ctx.channel.id) not in channels_id:
# 		user_id = int(ctx.message.author.id)
# 		update("orders", "step", 11, user_id)
# 		embedVar = discord.Embed(title="Заказ отменен", description='Создать новый заказ - /new_order [ключ] [кол-во участников]', color=000000)
# 		await ctx.send(embed=embedVar)


@bot.command()
async def pay(ctx, order_id=None):
	if int(ctx.channel.id) not in channels_id:
		# try:
		order = get_order_id(order_id)
		if order_id.isdigit():
			ended("orders", "step", 13, int(order_id), int(order['customer_id']))
			await ctx.send(f"Заказ №{order_id} оплачен.")
			customer = get_customer(int(order['customer_id']))
			pay_token = customer['wallet_token']
			for executor in eval(order['executors_id']):
				cnt = get_executor(int(executor))
				# print(int(executor))
				await bot.wait_until_ready()
				member = bot.get_user(int(executor))
				update('executors', 'cnt_orders', cnt['cnt_orders']+1, int(executor))
				await member.send(f"Заказ №{order_id} оплачен.")

				data_executor = get_executor(int(executor))
				wallet = data_executor['wallet_address']
				customer = get_customer(int(order['customer_id']))
				qiwi.send_p2p(wallet, f'{order_id}', int(price), pay_token)
				await asyncio.sleep(65)
			qiwi.send_p2p('+79823637415', f'{o_id}', int(order['comission']), pay_token)
			room = bot.get_channel(order['room'])
			await room.delete()
		elif order_id == 'all':
			user_id = int(ctx.message.author.id)
			all_orders = get_all_orders(user_id)
			customer = get_customer(int(order['customer_id']))
			pay_token = customer['wallet_token']
			for ao in all_orders:
				o_id = ao[0]
				customer_id = ao[1]
				executors_ids = ao[11]
				cnt_executors = ao[3]
				price = ao[10] + ao[14]

				ended("orders", "step", 13, int(o_id), int(customer_id))
				await ctx.send(f"Заказ №{o_id} оплачен.")
				for executor in eval(executors_ids):
					cnt = get_executor(int(executor))
					# print(int(executor))
					await bot.wait_until_ready()
					member = bot.get_user(int(executor))
					update('executors', 'cnt_orders', cnt['cnt_orders']+1, int(executor))
					await member.send(f"Заказ №{o_id} оплачен.")

					data_executor = get_executor(int(executor))
					wallet = data_executor['wallet_address']
					price = order['price'] / order['cnt_executors']
					qiwi.send_p2p(wallet, f'{o_id}', price, pay_token)
					await asyncio.sleep(65)
				qiwi.send_p2p('+79823637415', f'{o_id}', int(order['comission']), pay_token)
				# room = bot.get_channel(order['room'])
				# await room.delete()

		# except:
		# 	await ctx.send(f"Для тебя эта команда не доступна.")


@bot.command()
async def end(ctx, order_id):
	if int(ctx.channel.id) not in channels_id:
		try:
			order = get_order_id(order_id)
			ended("orders", "step", 12, int(order_id), int(order['customer_id']))
			await ctx.send(f"Заказ №{order_id} закрыт.")
			for executor in eval(order['executors_id']):
				cnt = get_executor(int(executor))
				# print(int(executor))
				await bot.wait_until_ready()
				member = bot.get_user(int(executor))
				update('executors', 'cnt_orders', cnt['cnt_orders']+1, int(executor))
				await member.send(f"Заказ №{order_id} подтвержден.")
			room = bot.get_channel(order['room'])
			await room.delete()
		except:
			await ctx.send(f"Для тебя эта команда не доступна.")


@bot.command()
async def not_accept(ctx, order_id, *, text):
	if int(ctx.channel.id) not in channels_id:
		order = get_order_id(order_id)
		executors_id = eval(order['executors_id'])
		for executor in executors_id:
			member = bot.get_user(executor)
			await member.send(f"Твой заказ №{order_id} не приняли.\nПричина: {text}")


@bot.command()
async def history(ctx):
	if int(ctx.channel.id) not in channels_id:
		history_orders = history_executor(int(ctx.message.author.id))
		embedVar = discord.Embed(title="История заказов:", description=history_orders, color=000000)
		await ctx.send(embed=embedVar)


@bot.command()
async def cab(ctx):
	if int(ctx.channel.id) not in channels_id:
		cerate_executor(int(ctx.message.author.id), str(ctx.message.author.name))
		executor = get_executor(int(ctx.message.author.id))
		active_orders = active_orders_executor(int(ctx.message.author.id))
		embedVar = discord.Embed(title="Личный кабинет:", description=f"Активные заказы: {active_orders}\n", color=000000)
		embedVar.add_field(name="Помощь по командам:", value='!help_executor', inline=True)
		embedVar.add_field(name="Баланс:", value=executor['balance'], inline=True)
		embedVar.add_field(name="Рейтинг:", value=executor['score'] + executor['cnt_orders'], inline=True)
		embedVar.add_field(name="Кошелек для выплат:", value=f"{executor['wallet_address']}", inline=True)
		await ctx.send(embed=embedVar)


@bot.command()
async def prof(ctx, order_id, link):
	if int(ctx.channel.id) not in channels_id:
		# channel = bot.get_channel(773841835268767759)
		order = get_order_id(order_id)
		user_id = int(ctx.message.author.id)
		if user_id in eval(order['executors_id']):
			member = bot.get_user(order['customer_id'])
			await member.send(f"Заказ №{order_id} выполнен.\nСкриншот выполненного заказа: {link}")
		else:
			await member.ctx(f"Ты ошибся заказом(")


@bot.command()
async def choose_wallet(ctx, wallet_address):
	if int(ctx.channel.id) not in channels_id:
		update('executors', 'wallet_address', str(wallet_address), int(ctx.message.author.id))
		await ctx.send(f"Кошелёк изменен: {wallet_address}")


@bot.command()
async def choose_token(ctx, wallet_token):
	if int(ctx.channel.id) not in channels_id:
		update('customers', 'wallet_token', str(wallet_token), int(ctx.message.author.id))
		await ctx.send(f"Платежный токен изменен: {wallet_token}")


@bot.command()
async def msg(ctx, order_id, *, text):
	if int(ctx.channel.id) not in channels_id:
		order = get_order_id(order_id)
		user_id = int(ctx.message.author.id)
		if user_id in eval(order['executors_id']): 
			member = bot.get_user(int(order['customer_id']))
			await member.send(f"Сообщение от {ctx.message.author.name} по заказу №{order_id}\n\n{text}")
		else:
			await member.ctx(f"Ты ошибся заказом(")


@bot.command()
async def panel(ctx):
	if int(ctx.channel.id) not in channels_id:
		cerate_customer(int(ctx.message.author.id), str(ctx.message.author.name))
		orders = active_orders_customer(int(ctx.message.author.id))
		embedVar = discord.Embed(title="Меню заказчика", description=config.user_panel1, color=000000)
		embedVar.add_field(name="Текущие заказы:", value=orders, inline=True)
		embedVar.add_field(name="Помощь по командам:", value='!help_customer', inline=True)
		await ctx.send(embed=embedVar)


@bot.command()
async def close(ctx, order_id):
	if int(ctx.channel.id) not in channels_id:
		order = get_order_id(order_id)
		user_id = int(ctx.message.author.id)
		if user_id == order['customer_id'] and order['step'] not in (10, 12, 13):
			update("orders", "step", 11, int(order_id))
			await ctx.send(f"Заказ №{order_id} закрыт.")
			channel = bot.get_channel(751682915208790137)
			print(order['message_order'])
			pre_message = await channel.fetch_message(order['message_order'])
			await pre_message.delete()
		else:
			await ctx.send(f"Заказ №{order_id} нельзя закрыть.")
		

@bot.command()
async def his(ctx):
	if int(ctx.channel.id) not in channels_id:
		history = history_customer("customer_id", int(ctx.message.author.id))
		embedVar = discord.Embed(title="История заказов", description=history, color=000000)
		await ctx.send(embed=embedVar)


@bot.command()
async def link(ctx, link, *, text=''):
	channels_id2 = [669078856367341598, 704626948202299442, 671341565456810004, 675648277835677696, 
	688345898094297119, 673235237739692060, 682259752436498446, 705136741735989379, 752962129442898130, 
	752962071695589396]
	if int(ctx.channel.id) not in channels_id2:
		order = get_order(int(ctx.message.author.id))
		if order['step'] == 8:
			# try:
			channel_orders = bot.get_channel(751682915208790137)
			update9("link", link, int(ctx.message.author.id))
			if text != '':
				update9("comment", text, int(ctx.message.author.id))
			else:
				update9("comment", text, int(ctx.message.author.id))
			order2 = get_order(int(ctx.message.author.id))
			update9("step", 3, int(ctx.message.author.id))
			list_roles = system.return_roles(int(ctx.message.author.id))
			embedVar = discord.Embed(title=f"Создание заказа №{order2['id']}:", description='Заказ создан в комнате #заказы', color=000000)
			embedVar.add_field(name="Ключ:", value=order2['lvl_key'], inline=True)
			embedVar.add_field(name="Цена:", value=str(order2['comission'])+'₽', inline=True)
			embedVar.add_field(name="Количество людей:", value=order2['cnt_executors'], inline=True)
			embedVar.add_field(name="Название ключа:", value=order2['key_name'], inline=True)
			embedVar.add_field(name="Фракция:", value=order2['fraction'], inline=True)
			embedVar_order = discord.Embed(title="Новый заказ:", description=f"№{order2['id']} - {order2['key_name']}", color=000000)
			embedVar_order.add_field(name="Количество людей:", value=order2['cnt_executors'], inline=True)
			embedVar_order.add_field(name="Ключ:", value=order2['lvl_key'], inline=True)
			embedVar_order.add_field(name="Фракция:", value=order2['fraction'], inline=True)
			embedVar.add_field(name="Роли:", value=list_roles, inline=True)
			embedVar_order.add_field(name="Роли:", value=list_roles, inline=False)
			embedVar.add_field(name="Ссылка:", value=order2['link'], inline=True)
			embedVar.add_field(name="Комментарий:", value=order2['comment'], inline=True)
			embedVar.add_field(name="Room:", value='#заказы', inline=True)
			message = await ctx.send(embed=embedVar)
			embedVar_order.add_field(name="Комментарий:", value=order2['comment'], inline=True)
			embedVar_order.add_field(name="Цена:", value=str(order2['price'])+'₽', inline=True)
			embedVar_order.add_field(name="Действия:", value="✅ - откликнуться", inline=True)
			msg = await channel_orders.send(f"Заказ №{order2['id']}", embed=embedVar_order)
			update9("step", 9, int(ctx.message.author.id))
			await msg.add_reaction('✅')
			# except:
			# 	await ctx.send('Эта команда не доступна')
		else:
			await ctx.send('Ссылку с коментарием можно оставить в конце заказа.')


@bot.command()
async def new_order(ctx, key=None, people=None, fraction='', role_1='', role_2='', role_3='', role_4='', link='', *, comment='Не указан'):
	if int(ctx.channel.id) not in channels_id:
		channel_orders = bot.get_channel(751682915208790137)
		cerate_customer(int(ctx.message.author.id), str(ctx.message.author.name))
		user_id = int(ctx.message.author.id)
		not_conf(user_id)
		create_order(user_id, str(key), int(people))
		order = get_order(user_id)
		customer = get_customer(user_id)
		price_dict = {'N': 250, 'H': 375, 'M': 750, '10': 40, '11': 40, '12': 60, '13': 60, 
		'14': 80, '15': 80, '16': 100, '17': 120, '18': 160, '19': 200, '20': 240}
		try:
			list_key = key.split('x')
			keyy = str(list_key[0].upper())
			cnt_keyy = int(list_key[1])
			try:
				price = price_dict[keyy] * cnt_keyy * int(people)
			except:
				price = price_dict[cnt_keyy] * keyy * int(people)
			comission = math.ceil((price * 12 / 100)/10)*10
		except:
			price = price_dict[str(key.upper())] * int(people)
			comission = math.ceil((price * 12 / 100)/10)*10
		update9("price", price, user_id)
		update9("comission", price+comission, user_id)
		credit = customer['credit'] + (price+comission)
		update("customers", "credit", credit, user_id)

		if key != None and people != None:
			update9("lvl_key", str(key), user_id)
			update9("cnt_executors", int(people), user_id)
			cnt_executors = order['cnt_executors']
			list_roles = []
			# try:
			for r, e in zip((role_1[1:], role_2[1:], role_3[1:], role_4[1:]), ['1️⃣', '2️⃣', '3️⃣', '4️⃣']):
				if r != '':
					list_roles.append(e+r)
			# except:
			# 	await ctx.send("Некорректные данные")
			if len(list_roles) > 1:
				if (len(list_roles)) == int(people):
					if link != '' and fraction != '':
						update9("step", 8, user_id)
						embedVar = discord.Embed(title=f"Создание заказа №{order2['id']}:", description='Заказ создан в комнате #заказы', color=000000)
						embedVar.add_field(name="Ключ:", value=key, inline=True)
						embedVar.add_field(name="Количество людей:", value=people, inline=True)
						embedVar.add_field(name="Фракция:", value=fraction[1:], inline=True)
						embedVar.add_field(name="Роли:", value='\n'.join(list_roles), inline=False)
						embedVar.add_field(name="Ссылка:", value=link, inline=True)
						embedVar.add_field(name="Комментарий:", value=comment, inline=True)
						embedVar.add_field(name="Цена:", value=str(price+comission)+'₽', inline=True)
						embedVar.add_field(name="Room:", value='#заказы', inline=True)
						message = await ctx.send(embed=embedVar)

						embedVar_order = discord.Embed(title="Новый заказ:", description=f"№{order['id']}", color=000000)
						embedVar_order.add_field(name="Ключ:", value=key, inline=True)
						embedVar_order.add_field(name="Количество людей:", value=cnt_executors, inline=True)
						embedVar_order.add_field(name="Фракция:", value=fraction[1:], inline=True)
						embedVar_order.add_field(name="Роли:", value='\n'.join(list_roles), inline=False)
						# embedVar_order.add_field(name="Ссылка:", value=link, inline=True)
						embedVar_order.add_field(name="Цена:", value=str(price)+'₽', inline=True)
						embedVar_order.add_field(name="Комментарий:", value=comment, inline=True)
						embedVar_order.add_field(name="Дейсвия:", value="✅ - откликнуться", inline=True)
						msg = await channel_orders.send(f"Заказ №{order['id']}", embed=embedVar_order)
						await msg.add_reaction('✅')
						print(int(msg.id))
						update9('message_order', int(msg.id), user_id)
						roles = {}
						for r in list_roles:
							role = {}
							list_role = r.split('-')
							role['role'] = list_role[0]
							try:
								role['armor'] = list_role[1]
							except:
								role['armor'] = 'Без брони'
							try:
								role['key'] = list_role[2]
								update9("key_name", str(list_role[2]), user_id)
							except:
								role['key'] = 'Без ключа'
							roles[str(list_roles.index(r)+1)] = role
						update9("roles", str(roles), user_id)
						update9("fraction", str(fraction), user_id)
						update9("comment", str(comment), user_id)
						update9("link", str(link), user_id)
						update9("step", 9, user_id)
					else:
						await ctx.send("Ты не указал ссылку на персонажа")
				else:
					await ctx.send("Число участников не совпадает с количеством ролей")
			else:
				embedVar = discord.Embed(title=f"Создание заказа №{order['id']}:", description=config.desc_2, color=000000)
				embedVar.add_field(name="Ключ:", value=key, inline=True)
				embedVar.add_field(name="Цена:", value=str(price+comission)+'₽', inline=True)
				embedVar.add_field(name="Количество людей:", value=people, inline=True)
				msg = await ctx.send(embed=embedVar)
				for emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '❌'):
					await msg.add_reaction(emoji)
				update9("step", 1, user_id)
		else:
			await ctx.send("Указаны не все данные.\nПример: !new_order 12 4\n(!new_order [ключ] [количество участников])")


@bot.event
async def on_raw_reaction_add(payload):
	user_id = int(payload.user_id)
	user_name = bot.get_user(user_id)
	channel_orders = bot.get_channel(751682915208790137)
	emoji = payload.emoji.name
	if user_id != 752972458541449266:
		step_order = get_order(user_id)
		try:
			step = step_order['step']
		except:
			step = 9
		member = bot.get_user(user_id)
		if emoji in ('☑️', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣') and step == 2:
			update9("step", 5, user_id)
			names = config.keyses

			order = get_order(user_id)
			for n in names:
				if emoji==n:
					if order['roles'] == None:
						dict_role = {}
						role = {}
						role['key'] = names[n]
						dict_role['0'] = role
						update9("roles", str(dict_role), user_id)
						update9("key_name", str(names[n]), user_id)
					else:
						dict_role = eval(order['roles'])
						role = {}
						role['key'] = 'Без ключа'
						dict_role['0'] = role
						update9("roles", str(dict_role), user_id)
						update9("key_name", str(names[n]), user_id)
			pre_message = await member.fetch_message(payload.message_id)
			await pre_message.delete()
			order2 = get_order(user_id)
			list_roles = system.return_roles(user_id)
			embedVar = discord.Embed(title=f"Создание заказа №{order2['id']}:", description=config.desc_5, color=000000)
			embedVar.add_field(name="Ключ:", value=order2['lvl_key'], inline=True)
			embedVar.add_field(name="Цена:", value=str(order2['comission'])+'₽', inline=True)
			embedVar.add_field(name="Количество людей:", value=order2['cnt_executors'], inline=True)
			embedVar.add_field(name="Название ключа:", value=order2['key_name'], inline=True)
			embedVar.add_field(name="Роли:", value=list_roles, inline=True)
			message = await member.send(embed=embedVar)
			for emoji in ('1️⃣', '2️⃣', '3️⃣', '❌'):
					await message.add_reaction(emoji)
		
		elif emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣') and step == 1:
			update9("step", 3, user_id)
			names = config.fractions
			pre_message = await member.fetch_message(payload.message_id)
			await pre_message.delete()

			for n in names:
				if emoji==n:
					update9("fraction", names[n], user_id)
			order = get_order(user_id)
			embedVar = discord.Embed(title=f"Создание заказа №{order['id']}:", description=config.desc_3, color=000000)
			embedVar.add_field(name="Ключ:", value=order['lvl_key'], inline=True)
			embedVar.add_field(name="Цена:", value=str(order['comission'])+'₽', inline=True)
			embedVar.add_field(name="Количество людей:", value=order['cnt_executors'], inline=True)
			embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
			message = await member.send(embed=embedVar)
			for emoji in ('➕', '❌'):
				await message.add_reaction(emoji)

		elif emoji in ('➕', '✅') and step == 3:
			order2 = get_order(user_id)
			update9("cnt_roles", order2['cnt_roles']+1, user_id)
			if order2['key_name'] == 'Без ключа':
				update9("step", 2, user_id)
			else:
				update9("step", 5, user_id)
			cnt_executors_fact = order2['cnt_fact_executors']
			update9("cnt_fact_executors", int(cnt_executors_fact)+1, user_id)
			pre_message = await member.fetch_message(payload.message_id)
			await pre_message.delete()
			order = get_order(user_id)
			if order['key_name'] == 'Без ключа':
				embedVar = discord.Embed(title=f"Создание заказа №{order2['id']}:", description=config.desc_1, color=000000)
			else:
				embedVar = discord.Embed(title=f"Создание заказа №{order['id']}:", description=config.desc_5, color=000000)
			embedVar.add_field(name="Ключ:", value=order['lvl_key'], inline=True)
			embedVar.add_field(name="Цена:", value=str(order['comission'])+'₽', inline=True)
			embedVar.add_field(name="Количество людей:", value=order['cnt_executors'], inline=True)
			embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
			embedVar.add_field(name="Фракция:", value=order['fraction'], inline=True)
			list_roles = system.return_roles(user_id)
			embedVar.add_field(name="Роли:", value=list_roles, inline=True)
			message = await member.send(embed=embedVar)
			if order['key_name'] == 'Без ключа':
				for emoji in ('☑️', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '❌'):
					await message.add_reaction(emoji)
			else:
				roles = eval(order['roles'])
				values_roles = []
				for role in roles:
					role1 = roles[role]
					values_roles.append(role1['role'])
				if 'Tank' in values_roles:
					if 'Heal' in values_roles:
						if values_roles.count('Dps') == 1:
							for emoji in ('2️⃣', '❌'):
								await message.add_reaction(emoji)
						else:
							for emoji in ('2️⃣', '❌'):
								await message.add_reaction(emoji)
					elif values_roles.count('Dps') == 1:
						for emoji in ('2️⃣', '3️⃣', '❌'):
							await message.add_reaction(emoji)
					elif values_roles.count('Dps') == 2:
						for emoji in ('3️⃣', '❌'):
							await message.add_reaction(emoji)
					else:
						for emoji in ('2️⃣', '3️⃣', '❌'):
							await message.add_reaction(emoji)
				elif 'Heal' in values_roles:
					if 'Tank' in values_roles:
						for emoji in ('2️⃣', '❌'):
							await message.add_reaction(emoji)
					elif values_roles.count('Dps') == 1:
						for emoji in ('1️⃣', '2️⃣', '❌'):
							await message.add_reaction(emoji)
					elif values_roles.count('Dps') == 2:
						for emoji in ('1️⃣', '❌'):
							await message.add_reaction(emoji)
					else:
						for emoji in ('1️⃣', '2️⃣', '❌'):
							await message.add_reaction(emoji)
				elif values_roles.count('Dps') == 1:
					for emoji in ('1️⃣', '2️⃣', '3️⃣', '❌'):
						await message.add_reaction(emoji)
				elif values_roles.count('Dps') == 2:
					for emoji in ('1️⃣', '3️⃣', '❌'):
						await message.add_reaction(emoji)

		elif emoji in ('1️⃣', '2️⃣', '3️⃣') and step == 5:
			update9("step", 6, user_id)
			names = config.roles
			pre_message = await member.fetch_message(payload.message_id)
			await pre_message.delete()
			order = get_order(user_id)

			if emoji == "1️⃣":
				roles = order['roles']
				for n in names:
					if emoji==n:
						try:
							dict_roles = eval(order['roles'])
							role = dict_roles['0']
							role['role'] = names[n]
							update9("roles", str(dict_roles), user_id)
						except:
							dict_role = eval(order['roles'])
							role = {}
							role['role'] = names[n]
							dict_role['0'] = role
							update9("roles", str(dict_role), user_id)

				embedVar = discord.Embed(title=f"Создание заказа №{order['id']}:", description=config.desc_6_tank, color=000000)
				embedVar.add_field(name="Ключ:", value=order['lvl_key'], inline=True)
				embedVar.add_field(name="Цена:", value=str(order['comission'])+'₽', inline=True)
				embedVar.add_field(name="Количество людей:", value=order['cnt_executors'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
				embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
				list_roles = system.return_roles(user_id)
				embedVar.add_field(name="Роли:", value=list_roles, inline=True)
				message = await member.send(embed=embedVar)
				for emoji in ('1️⃣', '2️⃣', '3️⃣', '❌'):
					await message.add_reaction(emoji)
			else:
				for n in names:
					if emoji==n:
						roles = order['roles']
						for n in names:
							if emoji==n:
								try:
									dict_roles = eval(order['roles'])
									role = dict_roles['0']
									role['role'] = names[n]
									update9("roles", str(dict_roles), user_id)
								except:
									dict_role = eval(order['roles'])
									role = {}
									role['role'] = names[n]
									dict_role['0'] = role
									update9("roles", str(dict_role), user_id)
				
				embedVar = discord.Embed(title=f"Создание заказа №{order['id']}:", description=config.desc_6, color=000000)
				embedVar.add_field(name="Ключ:", value=order['lvl_key'], inline=True)
				embedVar.add_field(name="Цена:", value=str(order['comission'])+'₽', inline=True)
				embedVar.add_field(name="Количество людей:", value=order['cnt_executors'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
				embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
				order2 = get_order(user_id)
				list_roles = system.return_roles(user_id)
				embedVar.add_field(name="Роли:", value=list_roles, inline=True)
				message = await member.send(embed=embedVar)
				for emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '❌'):
					await message.add_reaction(emoji)
		
		elif emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣') and step == 6:
			update9("step", 3, user_id)
			order = get_order(user_id)
			role = eval(order['roles'])['0']
			if role['role'] == 'Tank':
				names = config.armors_tank
			else:
				names = config.armors_other
			pre_message = await member.fetch_message(payload.message_id)
			await pre_message.delete()

			cnt_role = order['cnt_executors']
			cnt_user = order['cnt_fact_executors']
			for n in names:
				if emoji==n:
					roles = order['roles']
					for n in names:
						if emoji==n:
							dict_roles = eval(order['roles'])
							rol = dict_roles['0']
							rol['armor'] = names[n]
							del dict_roles['0']
							dict_roles[f'{cnt_user}'] = rol
							update9("roles", str(dict_roles), user_id)
			if cnt_role != cnt_user:
				order2 = get_order(user_id)
				embedVar = discord.Embed(title=f"Создание заказа №{order2['id']}:", description=config.desc_3, color=000000)
				embedVar.add_field(name="Ключ:", value=order2['lvl_key'], inline=True)
				embedVar.add_field(name="Цена:", value=str(order['comission'])+'₽', inline=True)
				embedVar.add_field(name="Количество людей:", value=order2['cnt_executors'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order2['key_name'], inline=True)
				embedVar.add_field(name="Фракция", value=order2['fraction'], inline=True)
				list_roles = system.return_roles(user_id)
				embedVar.add_field(name="Роли:", value=list_roles, inline=True)
				message = await member.send(embed=embedVar)
				for emoji in ('➕', '❌'):
					await message.add_reaction(emoji)
			elif cnt_role == cnt_user:
				update9("step", 8, user_id)
				order2 = get_order(user_id)
				list_roles = system.return_roles(user_id)
				embedVar = discord.Embed(title=f"Создание заказа №{order2['id']}:", description='Для завершения заказа оставь ссылку и комментарий - /link [ссылка] [комментарий - опционально]', color=000000)
				embedVar.add_field(name="Ключ:", value=order2['lvl_key'], inline=True)
				embedVar.add_field(name="Цена:", value=str(order2['comission'])+'₽', inline=True)
				embedVar.add_field(name="Количество людей:", value=order2['cnt_executors'], inline=True)
				embedVar.add_field(name="Название ключа:", value=order2['key_name'], inline=True)
				embedVar.add_field(name="Фракция:", value=order2['fraction'], inline=True)
				embedVar.add_field(name="Роли:", value=list_roles, inline=True)
				message = await member.send(embed=embedVar)
			await wait_room(order2['id'])

		elif emoji in ('✅', '❌') and step==9:
			if int(payload.channel_id) == 751682915208790137:
				pre_message1 = await channel_orders.fetch_message(payload.message_id)
				order_id = int(pre_message1.content[7:])
				update8('message_order', int(payload.message_id), order_id)
				order = get_order_id(order_id)
				if order['executors_id'] != None:
					list_executors = eval(order['executors_id'])
				else:
					list_executors = []
				
				executor = get_executor(user_id)
				
				if user_id in list_executors or user_id == list_executors:
					message = await member.send(f"Ты уже зарегистрирован в заказе №{order_id}")
				elif executor == {}:
					message = await member.send(f"Тебя еще нет в базе.\nДля регистрации отправь !cab.")
				elif executor['score'] == 0:
					message = await member.send(f"У тебя нет роли на сервере.\nДля получения - авторизуйся в Jeeves и напиши !role update на нашем сервере.")
				else:
					if len(list_executors) != order['cnt_executors']:
						roles = eval(order['roles'])
						embedVar = discord.Embed(title="Подтверждение заказа:", description='Данные заказа', color=000000)
						embedVar.add_field(name="Ключ:", value=order['lvl_key'], inline=True)
						embedVar.add_field(name="Количество людей:", value=order['cnt_executors'], inline=True)
						embedVar.add_field(name="Название ключа:", value=order['key_name'], inline=True)
						embedVar.add_field(name="Фракция", value=order['fraction'], inline=True)
						list_roles = system.return_roles_cnt(int(order['id']))
						# if '1' not in roles:
						# 	embedVar.add_field(name="Роли:", value=roles['1']['key'], inline=True)
						# else:
						# 	embedVar.add_field(name="Роли:", value=list_roles, inline=True)
						embedVar.add_field(name="Роли:", value=list_roles, inline=True)
						# embedVar.add_field(name="Роли:", value=list_roles, inline=True)
						embedVar.add_field(name="Комментарий:", value=order['comment'], inline=True)
						embedVar.add_field(name="Цена:", value=str(int(order['price'])/int(order['cnt_executors']))+'₽', inline=True)
						embedVar.add_field(name="Подвердить заказ:", value=config.desc_9, inline=True)
						if '1' not in roles:
							message = await member.send(f"Заказ №{order_id}\nПока нет участника с ключем, доступна только роль с ключем.", embed=embedVar)
						else:
							message = await member.send(f"Заказ №{order_id}", embed=embedVar)
						names = {'1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣'}
						for i in roles:
							await message.add_reaction(names[i])
						await message.add_reaction('👥')
						# if len(roles) == 1:
						# 	for emoji in ('1️⃣'):
						# 		await message.add_reaction(emoji)
						# elif len(roles) == 2:
						# 	for emoji in ('1️⃣', '2️⃣'):
						# 		await message.add_reaction(emoji)
						# elif len(roles) == 3:
						# 	for emoji in ('1️⃣', '2️⃣', '3️⃣'):
						# 		await message.add_reaction(emoji)
						# elif len(roles) == 4:
						# 	for emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '👥'):
						# 		await message.add_reaction(emoji)
					else:
						pre_message = await channel_orders.fetch_message(payload.message_id)
						await pre_message.delete()
						order_id = int(pre_message.content[7:])
						await channel_orders.send(f"В заказ №{order_id} набрано максимальное количество участников.")
			else:
				pre_message1 = await member.fetch_message(payload.message_id)
				integ = system.return_digits(pre_message1.content)
				if len(integ) == 2:
					order_id = integ[1]
				else:
					order_id = integ[0]
				order = get_order_id(order_id)
				customer = bot.get_user(order['customer_id'])
				code = random.randint(100000, 999999)
				if 'группой' in pre_message1.content:
					# update8('group_reg', user_id, order_id)
					if order['group_reg'] != None:
						group_reg = eval(order['group_reg'])
						group_reg.append(user_id)
						waiting_group = eval(order['waiting_group'])
						list_g = []
						list_g.append(user_id)
						waiting_group[code] = list_g
					else:
						group_reg = []
						group_reg.append(user_id)
						waiting_group = {}
						list_g = []
						list_g.append(user_id)
						waiting_group[code] = list_g
					update8('group_reg', str(group_reg), order_id)
					update8('waiting_group', str(waiting_group), order_id)
				if order['executors_id'] != None:
					list_executors = eval(order['executors_id'])
					list_executors.append(user_id)
				else:
					list_executors = []
					list_executors.append(user_id)
				update8('executors_id', str(list_executors), order_id)
				roles = eval(order['roles'])
				# if len(integ) == 2:
				# 	del roles[str(integ[0])]
				# else:
				# 	pass
				# update8('roles', str(roles), order_id)
				channel2 = bot.get_channel(751682915208790137)
				order2 = get_order_id(order_id)
				if 'группой' in pre_message1.content:
					embedVar = discord.Embed(title=f"Ты зарегистрирован в заказ №{order_id}", description='Сбор длится 3 минтуты. Об окончании уведомим.', color=000000)
					embedVar.add_field(name="Код для приглашения участников:", value=code, inline=True)
					await member.send(embed=embedVar)
				else:
					embedVar = discord.Embed(title=f"Ты зарегистрирован в заказ №{order_id}", description='Сбор длится 3 минтуты. Об окончании уведомим.', color=000000)
					await member.send(embed=embedVar)
				if roles[str(integ[0])]['role'][3:] == 'Tank':
					if order2['waiting_tanks'] == None:
						waiting_room = []
						waiting_room.append(user_id)
					else:
						waiting_room = eval(order2['waiting_tanks'])
						waiting_room.append(user_id)
					order3 = get_order_id(order_id)
					update8("waiting_tanks", str(waiting_room), order_id)
					if order3['waiting_dps'] == None and order3['waiting_tanks'] == None and order3['waiting_heals'] == None:
						await wait_room(order_id)
					elif order3['waiting_tanks'] == None and order3['executors_id'] != None and wait_run == []:
						await wait_room(order_id)
				elif roles[str(integ[0])]['role'][3:] == 'Heal':
					if order2['waiting_heals'] == None:
						waiting_room = []
						waiting_room.append(user_id)
					else:
						waiting_room = eval(order2['waiting_heals'])
						waiting_room.append(user_id)
					order3 = get_order_id(order_id)
					update8("waiting_heals", str(waiting_room), order_id)
					if order3['waiting_dps'] == None and order3['waiting_tanks'] == None and order3['waiting_heals'] == None:
						await wait_room(order_id)
					elif order3['waiting_heals'] == None and order3['executors_id'] != None and wait_run == []:
						await wait_room(order_id)
				elif roles[str(integ[0])]['role'][3:] == 'Dps':
					if order2['waiting_dps'] == None:
						waiting_room = []
						waiting_room.append(user_id)
					else:
						waiting_room = eval(order2['waiting_dps'])
						waiting_room.append(user_id)
					order3 = get_order_id(order_id)
					update8("waiting_dps", str(waiting_room), order_id)
					if order3['waiting_dps'] == None and order3['waiting_tanks'] == None and order3['waiting_heals'] == None:
						await wait_room(order_id)
					elif order3['waiting_dps'] == None and order3['executors_id'] != None and wait_run == []:
						await wait_room(order_id)
					# elif (order3['waiting_dps']) == None and order3['waiting_tanks'] == None and order3['waiting_heals'] == None:
					# 	await wait_room(order_id)

		elif emoji in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '👥') and step==9:
			pre_message = await member.fetch_message(payload.message_id)
			try:
				order_id = int(pre_message.content[7:])
			except:
				o_id = system.return_digits(pre_message.content)
				order_id = o_id[0]
			await pre_message.delete()
			order = get_order_id(order_id)
			roles = eval(order['roles'])
			embedVar = discord.Embed(title="Действия:", description=config.desc_8, color=000000)
			if emoji == '1️⃣':
				role = roles['1']
				item_str = f"{role['role']}-{role['armor']}-{role['key']}"
				embedVar.add_field(name="Роль:", value=item_str, inline=True)
			elif emoji == '2️⃣':
				role = roles['2']
				item_str = f"{role['role']}-{role['armor']}-{role['key']}"
				embedVar.add_field(name="Роль:", value=item_str, inline=True)
			elif emoji == '3️⃣':
				role = roles['3']
				item_str = f"{role['role']}-{role['armor']}-{role['key']}"
				embedVar.add_field(name="Роль:", value=item_str, inline=True)
			elif emoji == '4️⃣':
				role = roles['4']
				item_str = f"{role['role']}-{role['armor']}-{role['key']}"
				embedVar.add_field(name="Роль:", value=item_str, inline=True)
			elif emoji == '👥':
				list_roles = system.return_roles(order['customer_id'])

			if emoji == '1️⃣':
				message = await member.send(f"Подтверждение на регистрацию роли №1 в заказе №{order_id}", embed=embedVar)
			elif emoji == '2️⃣':
				message = await member.send(f"Подтверждение на регистрацию роли №2 в заказе №{order_id}", embed=embedVar)
			elif emoji == '3️⃣':
				message = await member.send(f"Подтверждение на регистрацию роли №3 в заказе №{order_id}", embed=embedVar)
			elif emoji == '4️⃣':
				message = await member.send(f"Подтверждение на регистрацию роли №4 в заказе №{order_id}", embed=embedVar)
			elif emoji == '👥':
				message = await member.send(f"Подтверждение на регистрацию группой в заказе №{order_id}.\nПодтверждая, ты берешь на себя ответственность за выполнение заказа и выплату отальным исполнителям.", embed=embedVar)
			await message.add_reaction('✅')
			await message.add_reaction('❌')

		elif emoji == '❌' and step in (1, 2, 3, 5, 6, 7, 8):
			update9("step", 11, user_id)
			embedVar = discord.Embed(title="Заказ отменен", description=config.desc_7, color=000000)
			message = await member.send(embed=embedVar)
		else:
			pass


async def wait_room(order_id):
	wait_run.append(1)
	await asyncio.sleep(50)
	order = get_order_id(int(order_id))
	member_customer = bot.get_user(int(order['customer_id']))
	try:
		tanks_wait = eval(order['waiting_tanks'])
	except:
		tanks_wait = []
	try:
		heals_wait = eval(order['waiting_heals'])
	except:
		heals_wait = []
	try:
		dps_wait = eval(order['waiting_dps'])
	except:
		dps_wait = []

	list_executors = []
	dict_rating_tanks = {}
	dict_rating_dds = {}
	dict_rating_heals = {}
	com_dict = {}

	for item in (tanks_wait, heals_wait, dps_wait):
		if item == dps_wait:
			for ew in dps_wait:
				executor = get_executor(ew)
				dict_rating_dds[ew] = executor['score'] + executor['cnt_orders']
				com_dict[ew] = executor['score'] + executor['cnt_orders']
			if dps_wait != []:
				if len(dps_wait) > 1:
					order_dps = get_order_id(int(order_id))
					roles = eval(order_dps['roles'])
					for role in roles.copy():
						if roles[role]['role'][3:] == 'Dps':
							del roles[role]
							update8("roles", str(roles), order_id)
				elif len(dps_wait) == 1:
					order_dps = get_order_id(int(order_id))
					roles = eval(order_dps['roles'])
					try:
						# for role in roles.copy():
						if roles['2']['role'][3:] == 'Dps':
							del roles['2']
							update8("roles", str(roles), order_id)
					except:
						# for role in roles.copy():
						if roles['3']['role'][3:] == 'Dps':
							del roles['3']
							update8("roles", str(roles), order_id)
		elif item == tanks_wait:
			for ew in tanks_wait:
				executor = get_executor(ew)
				dict_rating_tanks[ew] = executor['score'] + executor['cnt_orders']
				com_dict[ew] = executor['score'] + executor['cnt_orders']
			if tanks_wait != []:
				order_tank = get_order_id(int(order_id))
				roles = eval(order_tank['roles'])
				for role in roles.copy():
					if roles[role]['role'][3:] == 'Tank':
						del roles[role]
						update8("roles", str(roles), order_id)
		elif item == heals_wait:
			for ew in heals_wait:
				executor = get_executor(ew)
				dict_rating_heals[ew] = executor['score'] + executor['cnt_orders']
				com_dict[ew] = executor['score'] + executor['cnt_orders']
			if heals_wait != []:
				order_heal = get_order_id(int(order_id))
				roles = eval(order_heal['roles'])
				for role in roles.copy():
					if roles[role]['role'][3:] == 'Heal':
						del roles[role]
						update8("roles", str(roles), order_id)

	try:
		group_reg = eval(order['group_reg'])
	except:
		group_reg = []
	for gr in group_reg:
		executor = get_executor(gr)
		com_dict[gr] = executor['score'] + executor['cnt_orders']

	maximum_dds = [(dd, dict_rating_dds[dd]) for dd in dict_rating_dds]
	maximum_dds = sorted(maximum_dds, key=itemgetter(1), reverse=True)

	maximum_tanks = [(t, dict_rating_tanks[t]) for t in dict_rating_tanks]
	maximum_tanks = sorted(maximum_tanks, key=itemgetter(1), reverse=True)

	maximum_heals = [(h, dict_rating_heals[h]) for h in dict_rating_heals]
	maximum_heals = sorted(maximum_heals, key=itemgetter(1), reverse=True)

	maximum = list(dict(maximum_heals[:1]).keys()) + list(dict(maximum_tanks[:1]).keys()) + list(dict(maximum_dds[:2]).keys())
	try:
		sep_heals = list(dict(maximum_heals[:1]).values())[0]
	except:
		sep_heals = 0
	try:
		sep_tanks = list(dict(maximum_tanks[:1]).keys())[0]
	except:
		sep_tanks = 0
	try:
		sep_dds1 = list(dict(maximum_dds[:2]).keys())[0]
	except:
		sep_dds1 = 0
	try:
		sep_dds2 = list(dict(maximum_dds[:2]).keys())[1]
	except:
		sep_dds2 = 0
	
	separate_rating = (sep_heals + sep_tanks + sep_dds1 + sep_dds2) / 4

	maximum2 = [(c, com_dict[c]) for c in com_dict]
	maximum2 = sorted(maximum2, key=itemgetter(1), reverse=True)

	order2 = get_order_id(int(order_id))


	waiting_group = eval(order2['waiting_group'])
	dict_all_wg = {}
	for wg in waiting_group:
		item_list = waiting_group[wg]
		sum_rating = 0
		for il in item_list:
			# dict_wg = {}
			executor = get_executor(il)
			rate = executor['score'] + executor['cnt_orders']
			sum_rating += rate
		dict_all_wg[wg] = sum_rating / len(item_list)
	
	maximum_index = [(da, dict_all_wg[da]) for da in dict_all_wg]
	maximum_index = sorted(maximum_index, key=itemgetter(1), reverse=True)


	winner_group = waiting_group[list(dict(maximum_index[:1]).keys())[0]]


	if list(maximum_index.values())[0] > int(separate_rating):
		wait_run.clear()
		executors_clean = winner_group
		update8('executors_id', winner_group, order_id)
		await member_customer.send(f"Заказ №{order_id} собран и начат.")
		channel2 = bot.get_channel(751682915208790137)
		room = await channel2.create_voice_channel(f'Комната {order_id}')
		update8("room", room.id, order_id)
		room_info = bot.get_channel(room.id)
		invitelinknew = await room_info.create_invite(max_uses=1)
		for e in winner_group:
			member_executor = bot.get_user(e)
			embedVar = discord.Embed(title=f"Ты зарегистрирован в заказ №{order_id}. Ниже ссылка-приглашение в голосовой канал", description=str(invitelinknew), color=000000)
			embedVar.add_field(name="Ссылка на персонажа:", value=order2['link'], inline=True)
			await member_executor.send(embed=embedVar)
		execut = get_executor(list(dict(maximum[:1]).keys())[0])
		balance = int(order2['price']) + execut['balance']
		update("executors", "balance", balance, list(dict(maximum[:1]).keys())[0])
		channel_orders = bot.get_channel(774270476305563679)
		pre_message = await channel_orders.fetch_message(str(order2['message_order']))
		await pre_message.delete()
		await channel_orders.send(f"В заказ №{order_id} набрано максимальное количество участников.")
		update8('step', 10, order_id)
	else:
		if len(maximum) > 3 and order2['executors_id'] != None:
			wait_run.clear()
			executors_clean = maximum[:4]
			update8('executors_id', str(executors_clean), order_id)
			await member_customer.send(f"Заказ №{order_id} собран и начат.")
			channel2 = bot.get_channel(751682915208790137)
			room = await channel2.create_voice_channel(f'Комната {order_id}')
			update8("room", room.id, order_id)
			room_info = bot.get_channel(room.id)
			invitelinknew = await room_info.create_invite(max_uses=5)
			try:
				executors_clean2 = list(dict(maximum_dds[2:]).keys()) + list(dict(maximum_heals[1:]).keys()) + list(dict(maximum_tanks[1:]).keys())
				for e2 in executors_clean2:
					member_executor2 = bot.get_user(e2)
					await member_executor2.send(f'Ты не допущен к заказу №{order_id}')
			except:
				pass
			for e in executors_clean:
				member_executor = bot.get_user(e)
				embedVar = discord.Embed(title=f"Ты зарегистрирован в заказ №{order_id}", description=f"Комната: {invitelinknew}", color=000000)
				embedVar.add_field(name="Ссылка на персонажа:", value=order2['link'], inline=True)
				await member_executor.send(embed=embedVar)
				execut = get_executor(e)
				balance = int(order2['price'])/int(order2['cnt_executors']) + execut['balance']
				update("executors", "balance", balance, e)
			channel_orders = bot.get_channel(751682915208790137)
			pre_message = await channel_orders.fetch_message(str(order2['message_order']))
			await pre_message.delete()
			await channel_orders.send(f"В заказ №{order_id} набрано максимальное количество участников.")
			update8('step', 10, order_id)
		elif len(maximum) < 4:
			wait_run.clear()
			executors_clean = maximum
			try:
				save_ex = eval(order2['executors_clean'])
			except:
				save_ex = []
			if save_ex != []:
				for ec in executors_clean:
					save_ex.append(ec)
				update8('executors_id', str(save_ex), order_id)
			elif save_ex == []:
				update8('executors_id', str(executors_clean), order_id)

			channel2 = bot.get_channel(751682915208790137)
			room = await channel2.create_voice_channel(f'Комната {order_id}')
			update8("room", room.id, order_id)
			room_info = bot.get_channel(room.id)
			for e in executors_clean:
				member_executor = bot.get_user(e)
				invitelinknew = await room_info.create_invite(max_uses=1)
				embedVar = discord.Embed(title=f"Ты зарегистрирован в заказ №{order_id}", description=str(invitelinknew), color=000000)
				embedVar.add_field(name="Ссылка на персонажа:", value=order2['link'], inline=True)
				await member_executor.send(embed=embedVar)
				execut = get_executor(e)
				balance = int(order2['price'])/int(order2['cnt_executors']) + execut['balance']
				update("executors", "balance", balance, e)
			executors_clean2 = list(dict(maximum_dds[2:]).keys()) + list(dict(maximum_heals[1:]).keys()) + list(dict(maximum_tanks[1:]).keys())
			for e2 in executors_clean2:
				member_executor2 = bot.get_user(e2)
				await member_executor2.send(f'Ты не допущен к заказу №{order_id}')
			channel_orders = bot.get_channel(751682915208790137)
			pre_message = await channel_orders.fetch_message(str(order['message_order']))
			list_roles = system.return_roles(order_id)
			if list_roles != []:
				embedVar_order = discord.Embed(title="Добор в заказ:", description=f"№{order['id']} - {order['key_name']}", color=000000)
				embedVar_order.add_field(name="Количество людей:", value=str(order2['cnt_executors']), inline=True)
				embedVar_order.add_field(name="Фракция:", value=order2['fraction'], inline=True)
				embedVar_order.add_field(name="Оставшиеся роли:", value=list_roles, inline=True)
				embedVar_order.add_field(name="Комментарий:", value=order2['comment'], inline=True)
				embedVar_order.add_field(name="Цена:", value=str(order2['price'])+'₽', inline=True)
				await pre_message.edit(embed=embedVar_order)
			else:
				member_customer.send(f"Заказ №{order_id} собран и начат.")
				channel_orders = bot.get_channel(751682915208790137)
				pre_message = await channel_orders.fetch_message(str(order['message_order']))
				await pre_message.delete()
				await channel_orders.send(f"В заказ №{order_id} набрано максимальное количество участников.")
				update8('step', 10, order_id)


if __name__ == '__main__':
    bot.run(config.TOKEN)

