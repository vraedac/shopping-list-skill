from mycroft import MycroftSkill, intent_file_handler


class ShoppingList(MycroftSkill):
	def __init__(self):
		MycroftSkill.__init__(self)
		self.test_runner_context = '_TestRunner'
		self.todoist_api = None

	@intent_file_handler('AddToList.intent')
	def handle_add_to_list(self, message):
		if not self._validate_todoist():
			return

		item_name = message.data.get('item')
		list_project = self._get_project()
			
		if list_project is not None and not message.data.get(self.test_runner_context):
			self.todoist_api.items.add(item_name, project_id=list_project['id'])
			self.todoist_api.commit()

		self.speak_dialog('AddToList', {'item': item_name})
	
	@intent_file_handler('RemoveFromList.intent')
	def handle_remove_from_list(self, message):
		if not self._validate_todoist():
			return

		item_name = message.data.get('item')
		item = next((i for i in self._get_items() if i['content'] == item_name), None)
		if item is not None:
			action_item = api.items.get_by_id(item['id'])
			action_item.delete()
			api.commit()

		# list_project = self._get_project()

		# if list_project is not None and not message.data.get(self.test_runner_context):
		# 	for task in self.todoist_api.state['items']:
		# 		if task['project_id'] == list_project['id'] and task['content'] == item_name:
		# 			task.delete()
		# 			self.todoist_api.commit()

		self.speak_dialog('RemoveFromList', {'item': item_name})

	@intent_file_handler('IsItemOnList.intent')
	def handle_is_item_on_list(self, message):
		if not self._validate_todoist():
			return

		item_name = message.data.get('item')
		item = next((i for i in self._get_items() if i['content'] == item_name), None)

		if item is not None:
			self.speak_dialog('ItemIsOnList', {'item': item_name})
		else:
			self.speak_dialog('ItemNotOnList', {'item': item_name})

	@intent_file_handler('WhatIsOnList.intent')
	def handle_whats_on_list(self, message):
		if not self._validate_todoist():
			return

		list_items = self._get_items()

		if len(list_items) > 0:
			suffix = ''
			if len(list_items) > 1:
				last_item = list_items.pop()
				suffix = ' and ' + last_item['content']
			
			item_string = ', '.join(i['content'] for i in list_items) + suffix
			self.speak_dialog('WhatIsOnList_someItems', {'val1': item_string})
		else:
			self.speak_dialog('WhatIsOnList_noItems')

	def _validate_todoist(self):
		if self.todoist_api and self.todoist_api.token:
			return True

		import todoist
		self.todoist_api = todoist.TodoistAPI(self.settings.get('todoist_api_key'))

		if not self.todoist_api.token:
			self.speak_dialog('ApiKeyNotSet')
			return False
		
		return True

	def _get_project(self):
		self.todoist_api.sync()
		projects = self.todoist_api.state['projects']

		result = None
		for proj in projects:
			if proj['name'] == 'Grocery List': # TODO make this a configurable setting
				result = proj

		return result

	def _get_items(self):
		self.todoist_api.sync()

		items = []
		project_id = next(p['id'] for p in self.todoist_api.state['projects'] if p['name'] == 'Grocery List')

		if project_id is not None:
			items = [item for item in self.todoist_api.projects.get_data(project_id).get('items')]

		return items


def create_skill():
	return ShoppingList()

