from db import get_order_id, get_order, get_executor, update8


def return_roles(order_id: int):
	try:
		order = get_order_id(order_id)
		print(order)
		list_roles = []
		raw_roles = eval(order['roles'])
		print(raw_roles)
		# emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
		for r in raw_roles:
			item = raw_roles[r]
			try:
				item_str = f"{item['role']}-{item['armor']}-{item['key']}"
			except:
				try:
					item_str = f"{item['role']}-{item['armor']}"
				except:
					item_str = f"{item['role']}"
			list_roles.append(item_str)
		roles = '\n'.join(list_roles)
	except:
		roles = 'Не указано'
	return roles


def return_roles_cnt(order_id: int):
	# try:
	order = get_order_id(order_id)
	print(order)
	list_roles = []
	raw_roles = eval(order['roles'])
	print(raw_roles)
	# emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
	for r in raw_roles:
		item = raw_roles[r]
		print(item['role'])
		if item['role'][3:] == 'Tank':
			try:
				cnt = eval(order['waiting_tanks'])
			except:
				cnt = []
		elif item['role'][3:] == 'Heal':
			try:
				cnt = eval(order['waiting_heals'])
			except:
				cnt = []
		elif item['role'][3:] == 'Dps':
			try:
				cnt = eval(order['waiting_dps'])
			except:
				cnt = []
		
		len_cnt = len(cnt)
		try:
			item_str = f"{item['role']}-{item['armor']}-{item['key']}: {len_cnt}"
		except:
			try:
				item_str = f"{item['role']}-{item['armor']}: {len_cnt}"
			except:
				item_str = f"{item['role']}: {len_cnt}"
		list_roles.append(item_str)
	roles = '\n'.join(list_roles)
	# except:
	# 	roles = 'Не указано'
	return roles


def return_digits(content):
	s = content
	l = len(s)
	integ = []
	i = 0
	while i < l:
		s_int = ''
		a = s[i]
		while '0' <= a <= '9':
			s_int += a
			i += 1
			if i < l:
				a = s[i]
			else:
				break
		i += 1
		if s_int != '':
			integ.append(int(s_int))
	return integ


def return_executors(order_id: int):
	order = get_order_id(order_id)
	# print(order)
	# try:
	try:
		executors_tanks = eval(order['custom_tanks'])
	except:
		executors_tanks = []
	try:
		executors_heals = eval(order['custom_heals'])
	except:
		executors_heals = []
	try:
		executors_dps = eval(order['custom_dps'])
	except:
		executors_dps = []
	
	try:
		executors = eval(order['all_custom_executors'])
		print(executors, "executorssssssss")
	except:
		executors = []

	list_exexutors_raw = []
	for executor in executors:
		info_executor = get_executor(executor)
		# print(info_executor, 'info_executor')
		if executor in executors_tanks:
			role = "Tank"
			# print(executor, "executor_tank")
			# executors_tanks.remove(executor)
			# update8("custom_tanks", str(executors_tanks), int(order_id))
			num = executors.index(executor) + 1
			str_e = f"№{num} | {info_executor['executor_name']} | \
					Очки: {info_executor['score'] + info_executor['cnt_orders']} | \
					[Логи]({info_executor['logs']}) | {role}"
			list_exexutors_raw.append(str_e)
		# print(list_exexutors_raw)
	for executor in executors:
		info_executor = get_executor(executor)
		# print(info_executor, 'info_executor')
		if executor in executors_heals:
			role = "Heal"
			# print(executor, "executor_heal")
			# executors_heals.remove(executor)
			# update8("custom_heals", str(executors_heals), int(order_id))
			num = executors.index(executor) + 1
			str_e = f"№{num} | {info_executor['executor_name']} | \
					Очки: {info_executor['score'] + info_executor['cnt_orders']} | \
					[Логи]({info_executor['logs']}) | {role}"
			list_exexutors_raw.append(str_e)
		# print(list_exexutors_raw)
	for executor in executors:
		info_executor = get_executor(executor)
		# print(info_executor, 'info_executor')
		if executor in executors_dps:
			role = "Dps"
			# print(executor, "executors_dps")
			# executors_dps.remove(executor)
			# update8("custom_dps", str(executors_dps), int(order_id))
			num = executors.index(executor) + 1
			str_e = f"№{num} | {info_executor['executor_name']} | \
					Очки: {info_executor['score'] + info_executor['cnt_orders']} | \
					[Логи]({info_executor['logs']}) | {role}"
			list_exexutors_raw.append(str_e)
		# print(list_exexutors_raw)
	list_exexutors = '\n'.join(list_exexutors_raw)
	return list_exexutors
	# except:
	# 	list_exexutors = 'В заказ еще никто не зарегистрировался'
	# 	return list_exexutors