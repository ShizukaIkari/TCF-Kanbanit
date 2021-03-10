# A kanban card or post it. Contains only Id and Text
class Card:
    # Card's objects are being created when adding to a section, so the Id is being populated by the board's cards number
    # E.g. the 1st card has the id = 1, so on.
    def __init__(self, id, text):
        self.__card_id = id
        self.__card_text = text
    
    # Getters and setters to the object's attributes
    def set_id(self, id):
        self.__card_id = id

    def get_id(self):
        return self.__card_id 

    def set_text(self, text):
        self.__card_text = text

    def get_text(self):
        return self.__card_text
    
    # Object's string form
    def __str__(self):
        return 'Id: {}\n{}\n'.format(self.__card_id, self.__card_text)

