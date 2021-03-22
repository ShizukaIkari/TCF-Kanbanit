# Main Class, represents the Kanban board
class Board:
   
    def __init__(self):
        # List of Section objects
        self.__sections = []
        # Title of the kanban board
        self.__title = ''
        # Number of cards inside of the board
        self.__card_count = 0
    
    # Returns the list of Section's objects from Board object 
    def get_sections(self):
        return self.__sections
    
    # Returns the Section's names from Board object 
    def get_sections_names(self):
        names = []
        for sec in self.__sections:
            names.append(sec.get_name())
        return names
    
    # Append the section object to the list, it's used when creating a new section
    def add_section(self, sect):
        self.__sections.append(sect)
        # Card count is updated at this point
    
    # Getter and setter to the kanban title
    def get_title(self):
        return self.__title
    
    def set_title(self, title_name):
        self.__title = title_name
    
    # Returns the card count
    def get_cards_count(self):
        return self.__card_count
    
    # Card number is incremented when adding a card to a section
    def increment_cards_count(self):
        self.__card_count += 1
    
    # String format to the Board
    def __str__(self):
        board_text = 'Kanban image name: {}\n# of Sections: {}\n# of Cards: {}\nKanban Content:\n'.format(self.__title, len(self.__sections),
        self.__card_count)
        for s in self.__sections:
            board_text+= str(s)
        return board_text
