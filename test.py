# async def wait_room(order_id):
# 	await asyncio.sleep(10)
# 	order = get_order_id(int(order_id))
# 	member_customer = bot.get_user(int(order['customer_id']))
# 	try:
# 		tanks_wait = eval(order['waiting_tanks'])
# 	except:
# 		tanks_wait = []
# 	try:
# 		heals_wait = eval(order['waiting_heals'])
# 	except:
# 		heals_wait = []
# 	try:
# 		dps_wait = eval(order['waiting_dps'])
# 	except:
# 		dps_wait = []

#     list_executors = []
#     dict_rating = {}
    
# 	for item in (tanks_wait, heals_wait, dps_wait):
#         if item == dps_wait:
#             for ew in dps_wait:
#                 executor = get_executor(ew)
#                 dict_rating[ew] = executor['score'] + executor['cnt_orders']
#             if dps_wait != []:
#                 roles = order['roles']
#                 for role in roles:
#                     if role['role'] == 'Dps':
#                         del roles[role]
#                         if len(dps_wait) > 1:
#                             if role['role'] == 'Dps':
#                                 del roles[role]
#                         else:
#                             break
#             # else:
#             #     channel_orders = bot.get_channel(774270476305563679)
#             #     pre_message = await channel_orders.fetch_message(str(order['message_order']))
#             #     await pre_message.delete()
#             #     await channel_orders.send(f"В заказ №{order_id} набрано максимальное количество участников.")
#             #     update8('step', 10, order_id)

#             # maximum = [(d, dict_rating[d]) for d in dict_rating]
#             # maximum = sorted(maximum, key=itemgetter(1), reverse=True)
#             # executors_dps = list(dict(maximum[:2]).keys())
#             # for ed in executors_dps:
#             #     list_executors.append(ed)
#             # update8('executors_id', str(executors_tank), order_id)
#             # await member_customer.send(f"Заказ №{order_id} собран и начат.")
#             # channel2 = bot.get_channel(776341478539657267)
#             # room = await channel2.create_voice_channel(f'Комната {order_id}')
#             # update8("room", room.id, order_id)
#             # room_info = bot.get_channel(room.id)
#             # for e in executors_dps:
#             #     member_executor = bot.get_user(e)
#             #     invitelinknew = await room_info.create_invite(max_uses=1)
#             #     embedVar = discord.Embed(title=f"Ты зарегистрирован в заказ №{order_id} на роль Dps", description=f"Комната: {invitelinknew}", color=000000)
#             #     embedVar.add_field(name="Ссылка на персонажа:", value=order['link'], inline=True)
#             #     await member_executor.send(embed=embedVar)
#             #     execut = get_executor(e)
#             #     balance = int(order['price'])/int(order['cnt_executors']) + execut['balance']
#             #     update("executors", "balance", balance, e)
#             # channel_orders = bot.get_channel(774270476305563679)
#             # pre_message = await channel_orders.fetch_message(str(order['message_order']))
#             # await pre_message.delete()
#             # await channel_orders.send(f"В заказ №{order_id} набрано максимальное количество участников.")
#             # update8('step', 10, order_id)
#         elif item == tanks_wait:
#             for ew in tanks_wait:
#                 executor = get_executor(ew)
#                 dict_rating[ew] = executor['score'] + executor['cnt_orders']
#             if tanks_wait != []:
#                 roles = order['roles']
#                 for role in roles:
#                     if role['role'] == 'Tank':
#                         del roles[role]
#             # maximum = [(d, dict_rating[d]) for d in dict_rating]
#             # maximum = sorted(maximum, key=itemgetter(1), reverse=True)
#             # executors_tanks = list(dict(maximum[:1]).keys())
#             # for et in executors_tanks:
#             #     list_executors.append(et)
#             # update8('executors_id', str(executors_tank), order_id)
#             # await member_customer.send(f"Заказ №{order_id} собран и начат.")
#             # channel2 = bot.get_channel(776341478539657267)
#             # room = await channel2.create_voice_channel(f'Комната {order_id}')
#             # update8("room", room.id, order_id)
#             # room_info = bot.get_channel(room.id)
#             # for e in executors_tanks:
#             #     member_executor = bot.get_user(e)
#             #     invitelinknew = await room_info.create_invite(max_uses=1)
#             #     embedVar = discord.Embed(title=f"Ты зарегистрирован в заказ №{order_id} на роль Tank", description=f"Комната: {invitelinknew}", color=000000)
#             #     embedVar.add_field(name="Ссылка на персонажа:", value=order['link'], inline=True)
#             #     await member_executor.send(embed=embedVar)
#             #     execut = get_executor(e)
#             #     balance = int(order['price'])/int(order['cnt_executors']) + execut['balance']
#             #     update("executors", "balance", balance, e)
#         elif item == heals_wait:
#             for ew in heals_wait:
#                 executor = get_executor(ew)
#                 dict_rating[ew] = executor['score'] + executor['cnt_orders']
#             if heals_wait != []:
#                 roles = order['roles']
#                 for role in roles:
#                     if role['role'] == 'Heal':
#                         del roles[role]
#             # maximum = [(d, dict_rating[d]) for d in dict_rating]
#             # maximum = sorted(maximum, key=itemgetter(1), reverse=True)
#             # executors_heals = list(dict(maximum[:1]).keys())
#             # for eh in executors_heals:
#             #     list_executors.append(eh)
#             # update8('executors_id', str(executors_tank), order_id)
#             # await member_customer.send(f"Заказ №{order_id} собран и начат.")
#             # channel2 = bot.get_channel(776341478539657267)
#             # room = await channel2.create_voice_channel(f'Комната {order_id}')
#             # update8("room", room.id, order_id)
#             # room_info = bot.get_channel(room.id)
#             # for e in executors_heals:
#             #     member_executor = bot.get_user(e)
#             #     invitelinknew = await room_info.create_invite(max_uses=1)
#             #     embedVar = discord.Embed(title=f"Ты зарегистрирован в заказ №{order_id} на роль Heal", description=f"Комната: {invitelinknew}", color=000000)
#             #     embedVar.add_field(name="Ссылка на персонажа:", value=order['link'], inline=True)
#             #     await member_executor.send(embed=embedVar)
#             #     execut = get_executor(e)
#             #     balance = int(order['price'])/int(order['cnt_executors']) + execut['balance']
#             #     update("executors", "balance", balance, e)

#     try:
#         group_reg = eval(order['group_reg'])
#     except:
#         group_reg = []
#     for gr in group_reg:
#         executor = get_executor(gr)
#         dict_rating[gr] = executor['score'] + executor['cnt_orders']

#     maximum = [(d, dict_rating[d]) for d in dict_rating]
#     maximum = sorted(maximum, key=itemgetter(1), reverse=True)

#     if list(dict(maximum[:1]).keys())[0] in group_reg:
#         executors_clean = list(dict(maximum[:1]).keys())
#         update8('executors_id', executors_clean, order_id)
#         await member_customer.send(f"Заказ №{order_id} собран и начат.")
#         channel2 = bot.get_channel(776341478539657267)
#         room = await channel2.create_voice_channel(f'Комната {order_id}')
#         update8("room", room.id, order_id)
#         room_info = bot.get_channel(room.id)
#         member_executor = bot.get_user(list(dict(maximum[:1]).keys())[0])
#         invitelinknew = await room_info.create_invite(max_uses=5)
#         embedVar = discord.Embed(title=f"Ты зарегистрирован в заказ №{order_id}. Ниже ссылка-приглашение, ее можно использовать 5 раз", description=str(invitelinknew), color=000000)
#         embedVar.add_field(name="Ссылка на персонажа:", value=order['link'], inline=True)
#         await member_executor.send(embed=embedVar)
#         execut = get_executor(list(dict(maximum[:1]).keys())[0])
#         balance = int(order['price']) + execut['balance']
#         update("executors", "balance", balance, list(dict(maximum[:1]).keys())[0])
#         channel_orders = bot.get_channel(774270476305563679)
#         pre_message = await channel_orders.fetch_message(str(order['message_order']))
#         await pre_message.delete()
#         await channel_orders.send(f"В заказ №{order_id} набрано максимальное количество участников.")
#         update8('step', 10, order_id)
#     elif len(maximum) > 3 and order['executors_id'] == None:
#         executors_clean = list(dict(maximum[:4]).keys())
#         update8('executors_id', str(executors_clean), order_id)
#         await member_customer.send(f"Заказ №{order_id} собран и начат.")
#         channel2 = bot.get_channel(776341478539657267)
#         room = await channel2.create_voice_channel(f'Комната {order_id}')
#         update8("room", room.id, order_id)
#         room_info = bot.get_channel(room.id)
#         for e in executors_clean:
#             member_executor = bot.get_user(e)
#             invitelinknew = await room_info.create_invite(max_uses=1)
#             embedVar = discord.Embed(title=f"Ты зарегистрирован в заказ №{order_id} на роль Heal", description=f"Комната: {invitelinknew}", color=000000)
#             embedVar.add_field(name="Ссылка на персонажа:", value=order['link'], inline=True)
#             await member_executor.send(embed=embedVar)
#             execut = get_executor(e)
#             balance = int(order['price'])/int(order['cnt_executors']) + execut['balance']
#             update("executors", "balance", balance, e)
#         channel_orders = bot.get_channel(774270476305563679)
#         pre_message = await channel_orders.fetch_message(str(order['message_order']))
#         await pre_message.delete()
#         await channel_orders.send(f"В заказ №{order_id} набрано максимальное количество участников.")
#         update8('step', 10, order_id)
#     elif len(maximum) < 4:
#         executors_clean = list(dict(maximum).keys())
#         try:
#             save_ex = eval(order['executors_clean'])
#         except:
#             save_ex = []
#         if save_ex != []:
#             for ec in executors_clean:
#                 save_ex.append(ec)
#         update8('executors_id', str(save_ex), order_id)
#         else save_ex == []:
#             update8('executors_id', str(executors_clean), order_id)

#         channel2 = bot.get_channel(776341478539657267)
#         room = await channel2.create_voice_channel(f'Комната {order_id}')
#         update8("room", room.id, order_id)
#         room_info = bot.get_channel(room.id)
#         for e in executors_clean:
#             member_executor = bot.get_user(e)
#             invitelinknew = await room_info.create_invite(max_uses=1)
#             embedVar = discord.Embed(title=f"Ты зарегистрирован в заказ №{order_id}", description=str(invitelinknew), color=000000)
#             embedVar.add_field(name="Ссылка на персонажа:", value=order['link'], inline=True)
#             await member_executor.send(embed=embedVar)
#             execut = get_executor(e)
#             balance = int(order['price'])/int(order['cnt_executors']) + execut['balance']
#             update("executors", "balance", balance, e)
#         channel_orders = bot.get_channel(774270476305563679)
#         pre_message = await channel_orders.fetch_message(str(order['message_order']))
#         list_roles = system.return_roles(user_id)
#         if list_roles != []:
#             embedVar_order = discord.Embed(title="Добор в заказ:", description=f"№{order['id']} - {order['key_name']}", color=000000)
#             embedVar_order.add_field(name="Количество людей:", value=order['cnt_executors'], inline=True)
#             embedVar_order.add_field(name="Фракция:", value=order['fraction'], inline=True)
#             embedVar_order.add_field(name="Оставшиеся роли:", value=list_roles, inline=True)
#             embedVar_order.add_field(name="Комментарий:", value=order['comment'], inline=True)
#             embedVar_order.add_field(name="Цена:", value=str(order['price'])+'₽', inline=True)
#             await pre_message.edit(embed=embedVar_order)
#         else:
#             member_customer.send(f"Заказ №{order_id} собран и начат.")
#             channel_orders = bot.get_channel(774270476305563679)
#             pre_message = await channel_orders.fetch_message(str(order['message_order']))
#             await pre_message.delete()
#             await channel_orders.send(f"В заказ №{order_id} набрано максимальное количество участников.")
#             update8('step', 10, order_id)


