from mycroft import MycroftSkill, intent_file_handler, intent_handler


class ShoppingList(MycroftSkill):
	def __init__(self):
		MycroftSkill.__init__(self)

	#@intent_file_handler('add.to.shopping.list.intent')
	@intent_handler('add.to.shopping.list.intent')
	def handle_add_to_list(self, message):
		item1_name = message.data.get('item1')
		self.log.info(message)
		self.log.info('item1 is: ' + item1_name)
		item2_name = message.data.get('item2')

		self.speak_dialog('add.to.shopping.list', {'item1': item1_name})


def create_skill():
	return ShoppingList()

