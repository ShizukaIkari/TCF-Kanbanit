from Model import Card
# Class representing a Kanban Section
class Section: 
    def __init__(self, name, kanban_board):
        # Section's title e.g. To Do, In progress ...
        self.__name = name
        # Cards object's list
        self.__cards = []
        # Reference to the section's board, a section can't exist without a board
        self.__board = kanban_board
        self.__board.add_section(self)
    
    # Add card object to the section's object, incrementing the section's board card count.
    def add_card(self, card_text):
        card_id = self.__board.get_cards_count() + 1
        new_card = Card.Card(card_id, card_text)
        self.__cards.append(new_card)
        self.__board.increment_cards_count()
    
    # Getters and setters to object's attributes
    def get_cards(self):
        return self.__cards
    
    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name
    
    def get_board(self):
        return self.__board
    
    def set_board(self, kanban_board):
        self.__board = kanban_board
    
    # Object's string form
    def __str__(self):
        sec_txt = "Section name: {}\n# of Cards in: {}\n".format(self.__name, len(self.__cards))
        if len(self.__cards) > 0:
            sec_txt += 'Cards:\n'
            for c in self.__cards:
                sec_txt += str(c)
        return sec_txt