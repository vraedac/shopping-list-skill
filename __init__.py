from mycroft import MycroftSkill, intent_file_handler

class ShoppingList(MycroftSkill):
	def __init__(self):
		MycroftSkill.__init__(self)
		self.todoist_api = None
		self.parent_project_id = None

	def initialize(self):
		self._ensure_todoist_parent_project()

	@intent_file_handler('AddToList.intent')
	def handle_add_to_list(self, message):
		if not self._ensure_todoist():
			return

		item_name = message.data.get('item')
		list_name = message.data.get('list_name')
		list_project = self._get_project(list_name)
			
		if list_project:
			self.todoist_api.items.add(item_name, project_id=list_project['id'])
			self.todoist_api.commit()
			self.speak_dialog('AddToList_success', {'item': item_name, 'list_name': list_name})
		else:
			self.speak_dialog('ListNotFound', {'list_name': list_name})
	
	@intent_file_handler('RemoveFromList.intent')
	def handle_remove_from_list(self, message):
		if not self._ensure_todoist():
			return

		item_name = message.data.get('item')
		list_name = message.data.get('list_name')
		list_project = self._get_project(list_name)

		if list_project:
			item = next((i for i in self._get_items(list_name) if i['content'].casefold() == item_name.casefold()), None)

			if item is not None:
				action_item = self.todoist_api.items.get_by_id(item['id'])
				action_item.delete()
				self.todoist_api.commit()

			self.speak_dialog('RemoveFromList_success', {'item': item_name, 'list_name': list_name})
		else:
			self.speak_dialog('ListNotFound', {'list_name': list_name})


	@intent_file_handler('IsItemOnList.intent')
	def handle_is_item_on_list(self, message):
		if not self._ensure_todoist():
			return

		item_name = message.data.get('item')
		list_name = message.data.get('list_name')
		list_project = self._get_project(list_name)

		if list_project:
			item = next((i for i in self._get_items(list_name) if i['content'].casefold() == item_name.casefold()), None)

			if item:
				self.speak_dialog('IsItemOnList_yes', {'item': item_name, 'list_name': list_name})
			else:
				self.speak_dialog('IsItemOnList_no', {'item': item_name, 'list_name': list_name})
		else:
			self.speak_dialog('ListNotFound', {'list_name': list_name})

	@intent_file_handler('WhatIsOnList.intent')
	def handle_whats_on_list(self, message):
		if not self._ensure_todoist():
			return

		list_name = message.data.get('list_name')
		list_project = self._get_project(list_name)

		if list_project:
			list_items = self._get_items(list_name)

			if len(list_items) > 0:
				suffix = ''
				if len(list_items) > 1:
					last_item = list_items.pop()
					suffix = ' and ' + last_item['content']
				
				item_string = ', '.join(i['content'] for i in list_items) + suffix
				self.speak_dialog('WhatIsOnList_someItems', {'list_name': list_name, 'val1': item_string})
			else:
				self.speak_dialog('WhatIsOnList_noItems', {'list_name': list_name})
		else:
			self.speak_dialog('ListNotFound', {'list_name': list_name})

	@intent_file_handler('CreateList.intent')
	def handle_create_list(self, message):
		if not self._ensure_todoist():
			return

		list_name = message.data.get('list_name')
		# existing_list = next((p for p in self.todoist_api.state['projects'] if p['parent_id'] == self.parent_project_id and p['name'] == list_name), None)
		existing_list = self._get_project(list_name)

		if not existing_list:
			self.todoist_api.projects.add(list_name, parent_id=self.parent_project_id)
			self.todoist_api.commit()
			self.speak_dialog('CreateList_success', {'list_name': list_name})
		else:
			self.speak_dialog('CreateList_alreadyExists', {'list_name': list_name})

	# this should be called as the first step by each skill to ensure Todoist is connected; will play the "API key not configured" dialog if not
	def _ensure_todoist(self):
		if self.todoist_api and self.todoist_api.token:
			return True

		if not self._init_todoist():
			self.speak_dialog('ApiKeyNotSet')
			return False
		
		return True

	# checks if the todoist API has been initialized successfully and attempts to initialize it if not.  returns true if successful, false otherwise
	def _init_todoist(self):
		if self.todoist_api and self.todoist_api.token:
			return True

		import todoist
		self.todoist_api = todoist.TodoistAPI(self.settings.get('todoist_api_key'))

		return not not self.todoist_api.token

	# checks if the todoist parent project exists and creates it if not.  returns true if successful, false otherwise
	def _ensure_todoist_parent_project(self):
		if self.parent_project_id:
			return True

		if (not self.todoist_api or not self.todoist_api.token) and not self._init_todoist():
			return False

		parent_project_name = self.settings.get('parent_project_name')
		if not parent_project_name:
			parent_project_name = 'Shopping Lists'

		self.todoist_api.sync()
		projects = self.todoist_api.state['projects']
		parent_project = next((p for p in projects if p['name'] == parent_project_name), None)
		
		if not parent_project:
			parent_project = self.todoist_api.projects.add(parent_project_name)
			self.todoist_api.commit()

		self.parent_project_id = parent_project['id']
		return True

	def _get_project(self, name):
		self.todoist_api.sync()
		result = next((p for p in self.todoist_api.state['projects'] if p['name'] and p['parent_id'] == self.parent_project_id and p['name'].casefold() == name.casefold()), None)
		return result

	def _get_items(self, list_name):
		self.todoist_api.sync()

		items = []
		project_id = next(p['id'] for p in self.todoist_api.state['projects'] if p['name'] and p['parent_id'] == self.parent_project_id and p['name'].casefold() == list_name.casefold())

		if project_id:
			items = [item for item in self.todoist_api.projects.get_data(project_id).get('items')]

		return items


def create_skill():
	return ShoppingList()

