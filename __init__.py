from mycroft import MycroftSkill, intent_file_handler


class ShoppingList(MycroftSkill):
	def __init__(self):
		MycroftSkill.__init__(self)
		import todoist
		self.todoist_api = todoist.TodoistAPI('1a40a20b47e1d4e22824c820c9cd057bc738467e')

	@intent_file_handler('list.shopping.intent')
	def handle_list_shopping(self, message):
		item_name = message.data.get('item')
		# self.todoist_api.sync()
		# projects = self.todoist_api.state['projects']

		# listProject = None
		# for proj in projects:
		# 	if proj['name'] == 'Grocery List': # TODO make this a configurable setting
		# 		listProject = proj

		listProject = __get_project__()
			
		if listProject is not None:
			self.todoist_api.items.add(item_name, project_id=listProject['id'])
			self.todoist_api.commit()

		self.speak_dialog('list.shopping', {'item': item_name})
	
	@intent_file_handler('remove.from.shopping.list.intent')
	def handle_remove_from_shopping_list(self, message):
		item_name = message.data.get('item')
		self.speak_dialog('remove.from.shopping.list', {'item': item_name})

	@intent_file_handler('IsItemOnList.intent')
	def handle_is_item_on_list(self, message):
		item_name = message.data.get('item')
		self.speak_dialog('ItemNotOnList', {'item': item_name})

	def __get_project__(self):
		self.todoist_api.sync()
		projects = self.todoist_api.state['projects']

		result = None
		for proj in projects:
			if proj['name'] == 'Grocery List': # TODO make this a configurable setting
				result = proj
		# self.log.info('about to print projects state:')
		# self.log.info(projects)

		return result



def create_skill():
	return ShoppingList()

