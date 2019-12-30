from mycroft import MycroftSkill, intent_file_handler


class ShoppingList(MycroftSkill):
	def __init__(self):
		MycroftSkill.__init__(self)

	@intent_file_handler('list.shopping.intent')
	def handle_list_shopping(self, message):
		item_name = message.data.get('item')
		self.speak_dialog('list.shopping', {'item': item_name})
	
	@intent_file_handler('remove.from.shopping.list.intent')
	def handle_remove_from_shopping_list(self, message):
		item_name = message.data.get('item')
		self.speak_dialog('remove.from.shopping.list', {'item': item_name})

	@intent_file_handler('IsItemOnList.intent')
	def handle_is_item_on_list(self, message):
		item_name = message.data.get('item')
		self.speak_dialog('ItemNotOnList', {'item': item_name})


def create_skill():
	return ShoppingList()

