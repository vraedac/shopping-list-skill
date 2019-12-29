from mycroft import MycroftSkill, intent_file_handler


class ShoppingList(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('list.shopping.intent')
    def handle_list_shopping(self, message):
        self.speak_dialog('list.shopping')


def create_skill():
    return ShoppingList()

