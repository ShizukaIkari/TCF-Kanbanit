# Functions used to process the API response
import json
from Model import Board
from Model import Section
from Model import Card

# Receives the Google API response and returns a dict of dicts containing their text and coordinates
def build_myjson(g_document):
    # Is there a chance that 1 kanban pic returns more than one page?
    for page in g_document.pages:
        # Each card/section is represented by a dictionary containing its vertices and the text within
        kanban_cards = {}
        # List of cards/section dicts
        kanban_cards['cards'] = []
        # Post it or section
        for block in page.blocks:
            p_contents = ''
            # Where the text is located  
            for paragraph in block.paragraphs:
                # Individual word
                for word in paragraph.words:
                    w_content = ''
                    # Word letters, use property and text
                    for symbol in word.symbols:
                        BreakType = symbol.property.detected_break.type_
                        # Even though there's types of breaks, I decided that simply adding a space will do
                        if BreakType in [BreakType.SPACE, BreakType.SURE_SPACE, BreakType.EOL_SURE_SPACE, BreakType.HYPHEN, BreakType.LINE_BREAK]:
                            w_content += (symbol.text) + ' '
                        else:
                            w_content += (symbol.text)
                    p_contents += w_content
            block_dic = {'bounding_box': get_bounding_box(block.bounding_box), 'text': p_contents.strip()}
            kanban_cards['cards'].append(block_dic)
        if len(g_document.pages) > 1:
            print(g_document.pages)
        return kanban_cards # this way it's only checking 1 page

# Returns a tuple list containing the 4 vertices (x,y) from the bounding box of the block
def get_bounding_box(obj_bb):
    vertices_list = []
    for vertex in obj_bb.vertices:
        x,y = vertex.x, vertex.y
        vertices_list.append((x, y))
    return vertices_list

# Get kanban sections based on the position on the image: Considering text on the image top as sections
def find_sections(knbn_dic):
    sections = []
    # Sort by the first y of every card
    sort_ys(knbn_dic['cards'])
    # The "down y"/"second y" from the first card will serve as the base of section line
    base_y = knbn_dic['cards'][0]['bounding_box'][2][1]
    
    # card is a dict from the list of dicts
    for card in knbn_dic['cards']:
        # The "upper y" from the card in iteration
        first_y = card['bounding_box'][0][1]
        # The "down y" from the card in iteration
        last_y = card['bounding_box'][2][1]

        # if this upper y is in range from the base down y, it's a section
        if (base_y > first_y):
            sections.append(card)
            if last_y > base_y:
                base_y = last_y
        else:
            break
    
    return sections

# Bubble sort to sort the cards list
def sort_ys(knbn_dic):
    # knbn_dic is a list of dicts
    for iter_num in range(len(knbn_dic)-1, 0, -1):
        for idx in range(iter_num):
            first_y = knbn_dic[idx]['bounding_box'][0][1]
            next_y =  knbn_dic[idx+1]['bounding_box'][0][1]
            if first_y > next_y:
                temp = knbn_dic[idx]
                knbn_dic[idx] = knbn_dic[idx+1]
                knbn_dic[idx+1] = temp


# Receives kanban board object and json kanban, and a list with the dictionary sections, returns the kanban object filled
def set_cards_to_kanban(knbn_dic, lst_dic_sections, knbn_board):
    # Calculates the x means of sections and creates its objects
    sections_x_means = []
    for sec in lst_dic_sections:
        sec_mean = (sec['bounding_box'][0][0] + sec['bounding_box'][1][0])/2
        obj_section = Section.Section(sec['text'], knbn_board)
        sections_x_means.append((obj_section, sec_mean))
   
    # Calculates the x means of cards that aren't sections
    cards_x_means = []
    for card in knbn_dic['cards']:
        if card not in lst_dic_sections:
            card_mean = (card['bounding_box'][0][0] + card['bounding_box'][1][0])/2
            cards_x_means.append((card, card_mean))

    # Calculates for each card the distance between the card and the module
    for card_tuple in cards_x_means:
        # x_mean of a card
        x_card = card_tuple[1]

        # Iterates to find the minimum distance, min_sec receives the object that has the absolute minumum distance
        # Pythonic way to find the minimum distance and return the correspondent section, works in some jsons
        # and fails for "no reason" in others
        # min_sec = min((abs(x_card - sec_tuple[1]), sec_tuple[0]) for sec_tuple in sections_x_means)[1]
        
        # The distance between the first section and the card
        min_dist = abs(x_card - sections_x_means[0][1])
        min_sec = sections_x_means[0][0]
        for sec_tuple in sections_x_means:
            if (abs(x_card - sec_tuple[1]) < min_dist):
                min_dist = abs(x_card - sec_tuple[1])
                min_sec = sec_tuple[0]
                
        # Now that we know that this section is the closest to the card, we add it to the section.
        min_sec.add_card(card_tuple[0]['text'])

    return knbn_board    

# Outputs a file with info about the Kanban Board 
def kanban_report(knbn_board, report_name):
    with open('Responses/Reports/{}.txt'.format(report_name), 'w', encoding='cp1252', errors='ignore') as report_file:
        # str(kanban) handles the formatting of the report 
        report_file.writelines(str(knbn_board))
    print('Ok')

# Prints the board on the console
def print_board(knbn_board):
    print('*---{}---*'.format(knbn_board.get_title()))
    for s in knbn_board.get_sections():
        print_section(s)

def print_section(knbn_section):
    print('|{}|'.format('-' * (len(knbn_section.get_name()) + 2)))
    print('| {} |'.format(knbn_section.get_name()))
    for c in knbn_section.get_cards():
        print_card(c) 

def print_card(knbn_card):
    print('{}'.format('-' * (len('Card Id: ') + len(str(knbn_card.get_id())))))
    print('Card Id: {}'.format(knbn_card.get_id()))
    print('Card Text: {}'.format(knbn_card.get_text()))

# Reads the kanban in json format and converts it to the object notation
def read_jkanban(file_name):
    # Creates a Board object, using the name of the json file as title
    my_kanban = Board.Board()
    json_name = file_name.split('/')[-1]
    my_kanban.set_title(json_name.split('.')[0])

    with open(file_name, encoding='cp1252', errors='ignore') as jkanban:
        my_jkanban = json.load(jkanban)
        # Retrieves sections from json dict
        sections = find_sections(my_jkanban)
        # This creates and add section objects to the kanban object
        my_kanban = set_cards_to_kanban(my_jkanban, sections, my_kanban)
    
    return my_kanban