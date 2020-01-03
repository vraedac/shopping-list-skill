from mycroft import MycroftSkill, intent_file_handler


class ShoppingList(MycroftSkill):
	def __init__(self):
		MycroftSkill.__init__(self)
		import todoist
		self.todoist_api = todoist.TodoistAPI('1a40a20b47e1d4e22824c820c9cd057bc738467e')

	@intent_file_handler('AddToList.intent')
	def handle_add_to_list(self, message):
		item_name = message.data.get('item')
		list_project = self._get_project()
			
		if list_project is not None:
			self.todoist_api.items.add(item_name, project_id=list_project['id'])
			self.todoist_api.commit()

		self.speak_dialog('AddToList', {'item': item_name})
	
	@intent_file_handler('RemoveFromList.intent')
	def handle_remove_from_list(self, message):
		item_name = message.data.get('item')
		list_project = self._get_project()

		if list_project is not None:
			for task in self.todoist_api.state['items']:
				if task['project_id'] == list_project['id'] and task['content'] == item_name:
					task.delete()
					self.todoist_api.commit()

		self.speak_dialog('RemoveFromList', {'item': item_name})

	@intent_file_handler('IsItemOnList.intent')
	def handle_is_item_on_list(self, message):
		self.log.info('in the IsItemOnList intent')
		item_name = message.data.get('item')
		list_project = self._get_project()
		found = False

		if list_project is not None:
			for task in self.todoist_api.state['items']:
				if task['project_id'] == list_project['id'] and task['content'] == item_name:
					found = True
					break

		if found == True:
			self.speak_dialog('ItemIsOnList', {'item': item_name})
		else:
			self.speak_dialog('ItemNotOnList', {'item': item_name})

	@intent_file_handler('WhatIsOnList.intent')
	def handle_whats_on_list(self, message):
		self.log.info('in the WhatIsOnList intent')
		list_items = []
		list_project = self._get_project()

		if list_project is not None:
			for item in self.todoist_api.state['items']:
				if item['project_id'] == list_project['id']:
					list_items.append(item['content'])
		
		self.log.info('items:')
		self.log.info(list_items)
		if len(list_items) > 0:
			suffix = ''
			if len(list_items) > 1:
				last_item = list_items.pop()
				suffix = ' and ' + last_item
			
			# item_string = ', '.join(list_items) + suffix
			item_string = 'bacon '
			self.log.info('item string: ' + item_string)
			self.speak_dialog('WhatIsOnList_someItems', {'val1': item_string})
		else:
			self.speak_dialog('WhatIsOnList_noItems')


	def _get_project(self):
		self.todoist_api.sync()
		projects = self.todoist_api.state['projects']

		result = None
		for proj in projects:
			if proj['name'] == 'Grocery List': # TODO make this a configurable setting
				result = proj

		return result



def create_skill():
	return ShoppingList()

