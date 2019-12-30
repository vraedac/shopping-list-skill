from mycroft import MycroftSkill, intent_file_handler


class ShoppingList(MycroftSkill):
	def __init__(self):
		MycroftSkill.__init__(self)

	@intent_file_handler('add.to.shopping.list.intent')
	def handle_add_to_list(self, message):
		item1_name = message.data.get('item1')
		item2_name = message.data.get('item2')

		self.speak_dialog('add.to.shopping.list', {'item1': item_name})


def create_skill():
	return ShoppingList()

