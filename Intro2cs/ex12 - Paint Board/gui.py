# FILE: ex12.py
# WRITER: Ofir Birka, Bar Vered
# EXERCISE: intro2cs ex12 2015-2016
# DESCRIPTION:  Draw Game

# Imports
from tkinter import *
import client
from tkinter import messagebox
import copy

# Constants
DEFAULT_COLOR = 'blue'
DEFAULT_COLOR_BYTE = b'blue'
NUM_OF_ARGUMENTS = 5
HELP_TEXT = 'Here, you can see other members who have joined your group, ' \
            'you can draw shapes by clicking on the button of the wanted shape, ' \
            'and you can also choose a color from a list of colors. ' \
            'You can also see other members drawings, and who drew each one.'
BACKGROUND_COLOR = 'white'
HELP_FRAME_HEIGHT = 20
HELP_APPLICATION_SIZE = '300x300'
LINE = 'line'
OVAL = 'oval'
RECTANGLE = 'rectangle'
TRIANGLE  = 'triangle'
QUIT_MSG = 'Are you sure want to exit?'
JOIN = 'join'
SHAPE = 'shape'
USERS = 'users'
LEAVE = 'leave'
ERROR = 'error'
ERROR_SIZE = '300x300'
DEFAULT_FONT = "Helvetica,"
DELAY = 100
DEFAULT_SHAPE = LINE
LEGIT_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabc' \
                    'defghijklmnopqrstuvwxyz1234567890_'


class Shape:
    '''
    Represents a shape
    '''
    def __init__(self, type=DEFAULT_SHAPE, color=DEFAULT_COLOR_BYTE, coord=[]):
        self.__type = type
        self.__color = color
        self.__coord = coord

    def get_represetion_of_shape(self):
        '''
        Return tuple (type<string>, color<string>,  coordinates<list>)
        '''
        return (self.__type, self.__color, self.__coord)

    def set_color(self, color):
        self.__color = color

    def set_type(self, type):
        self.__type = type

    def get_type(self):
        return self.__type

    def get_color(self):
        return self.__color

    def add_coords(self, event):
        '''
        adds shapes coords to client
        '''
        self.__coord.append((event.x, event.y))

    def get_coords(self):
        # returns the coords so the program will know where to create a shape
        return self.__coord

    def reset_coords(self):
        # resets the current coords
        self.__coord = []


class Gui:
    '''
    Represents a graphical user interface
    '''
    def __init__(self, root, USER_NAME, SERVER_ADDRESS,
                 SERVER_PORT, GROUP_NAME):
        # Generate Client object
        self.__client = client.Client(USER_NAME, SERVER_ADDRESS,
                                      SERVER_PORT, GROUP_NAME)
        self.__members_list = []
        # Window
        self.__root = root
        # Help
        self.__up_line_frame = Frame(bg=BACKGROUND_COLOR, height=HELP_FRAME_HEIGHT)
        self.__shape = Shape()
        self.__messages_from_server = []
        self.__up_line_3 = Frame()
        self.__scroll = Scrollbar(self.__up_line_3)
        self.__members_list = Listbox(self.__up_line_3,
                                      yscrollcommand=self.__scroll.set)
        self.initialize_game()
        self.draw_arcitecture_game()

    def get_root(self):
        return self.__root

    def initialize_game(self):
        '''
        Create the arcitecture of the game and return root
        '''
        # Connect to server
        self.__messages_from_server.append(
            self.__client.send_join_to_server())

        # Root name
        self.__root.wm_title(self.__client.get_username())
        self.__initial = StringVar(self.__root)
        self.__initial.set(DEFAULT_COLOR) # Default color
        # Pack up bar
        self.__up_line_frame.pack(fill=X)

    def show_help(self):
        # shows how to use the application
        top_level = Toplevel()
        top_level.title('Application Help')
        top_level.geometry(HELP_APPLICATION_SIZE)
        top_level.focus_set()
        message = Message(top_level,text=HELP_TEXT)
        message.pack()

    def change_shape_type(self, type):
        self.__shape.reset_coords()
        self.__shape.set_type(type)

    def handle_draw(self, event):
        '''
        Handle all types of shapes - line, oval, rectangle, triangle
        '''
        if self.__shape.get_type() == LINE:
            return self.line_click(event)
        elif self.__shape.get_type() == OVAL:
            return self.circle_click(event)
        elif self.__shape.get_type() == RECTANGLE:
            return self.rectangle_click(event)
        elif self.__shape.get_type() == TRIANGLE:
            self.triangle_click(event)
        return

    def recv_shape_from_server(self, shape):
        coords = shape.get_coords()
        # Draw the shape
        if shape.get_type() == LINE:
            # Draw shape on board
            x0, y0 = coords[0]
            x1, y1 = coords[1]
            graphs.create_line(x0, y0, x1, y1, fill=self.__shape.get_color())
        elif shape.get_type() == OVAL:
            x0, y0 = coords[0]
            x1, y1 = coords[1]
            graphs.create_oval(x0, y0, x1, y1,
                               fill=self.__shape.get_color())
        elif shape.get_type() == RECTANGLE:
            x0, y0 = coords[0]
            x1, y1 = coords[1]
            graphs.create_rectangle(x0, y0, x1, y1,
                                    fill=self.__shape.get_color())
        elif shape.get_type() == TRIANGLE:
            x0, y0 = coords[0]
            x1, y1 = coords[1]
            x2, y2 = coords[2]
            graphs.create_polygon(x0, y0, x1, y1, x2, y2,
                                  fill=self.__shape.get_color())
        graphs.create_text(x0, y0, text=self.__client.get_username())

    def send_shape_to_server(self):
        shape = self.__shape
        self.__messages_from_server.append(
            self.__client.send_add_shape_to_server(shape.get_type(),
                                               shape.get_coords(),
                                               shape.get_color()))
        self.__shape.reset_coords()

    def line_click(self, event):
        self.__shape.add_coords(event)
        coords = self.__shape.get_coords()
        if len(coords) == 2:
            # Send shape to server
            self.send_shape_to_server()

    def circle_click(self, event):
        self.__shape.add_coords(event)
        coords = self.__shape.get_coords()
        if len(coords) == 2:
            self.send_shape_to_server()

    def rectangle_click(self, event):
        self.__shape.add_coords(event)
        coords = self.__shape.get_coords()
        if len(coords) == 2:
            self.send_shape_to_server()

    def triangle_click(self, event):
        self.__shape.add_coords(event)
        coords = self.__shape.get_coords()
        if len(coords) == 3:
            self.send_shape_to_server()

    def on_closing(self):
        self.__client.send_leave_to_server()
        if messagebox.askokcancel("Quit", QUIT_MSG):
            self.__root.destroy()

    def recv_messages(self):
        '''
        Taking care of messages that sent from server
        '''
        # Check if there is messages from server
        message_from_server = \
            self.__client.check_if_there_is_message_from_server()
        if message_from_server != ['']:
            self.__messages_from_server.append(message_from_server)
        messages_copy = copy.deepcopy(self.__messages_from_server)
        for msg in messages_copy:
            type_msg = msg[0]
            if type_msg == USERS:
                self.__client.add_member([msg[1]])
            elif type_msg == JOIN:
                self.__client.add_member(msg[1])
            elif type_msg == SHAPE:
                list_coord = msg[3].split(',')
                list_tuple_coords = []
                for value in range(0,len(list_coord)-1, 2):
                    list_tuple_coords.append((list_coord[value],
                                              list_coord[value+1]))
                new_shape = Shape(msg[2], msg[4], list_tuple_coords)
                # Send new shape to draw
                self.recv_shape_from_server(new_shape)
            elif type_msg == LEAVE:
                self.update_users(True)
                # Delete user that left from members list
                self.__client.del_member_from_list(msg[1])
            elif type_msg == ERROR:
                self.print_error(msg[1])
            self.__messages_from_server.remove(msg)

    def print_error(self, msg):
        top_level = Toplevel()
        top_level.title(ERROR)
        top_level.geometry(ERROR_SIZE)
        top_level.focus_set()
        message = Message(top_level,text=msg)
        message.pack()

    def update_users(self, type=False):
        ezer_list = \
            list(self.__members_list.get(2, self.__members_list.size()))
        if type:
            self.__members_list.delete(2, self.__members_list.size())
        for member in self.__client.get_list_members():
            if member not in ezer_list:
                self.__members_list.insert(END, member)

    def draw_arcitecture_game(self):
        '''
        Draw the general view of the gui
        '''
        # Stage 1 ------------------------------------------------------------
        # Show help button
        help_button = Button(self.__up_line_frame,
                             text='Help', bg=BACKGROUND_COLOR,
                             command=self.show_help,
                             font=(DEFAULT_FONT,10))
        help_button.pack(side=LEFT)
        # Second line
        up_line_2 = Frame(height=20)
        up_line_2.pack(fill=X)
        color_label = Label(up_line_2, text="Color:")
        color_label.pack(side=LEFT, fill=BOTH)
        # Draw color tag colors
        global initial
        initial = StringVar(up_line_2)
        initial.set(DEFAULT_COLOR) # initial value
        color_option = OptionMenu(up_line_2, initial,'red','green',
                                 'yellow', 'black', 'violet',
                                  'orange').pack(side=LEFT)
        # Up line 3
        self.__up_line_3.pack(fill=X)
        # List name
        self.__members_list.insert(END, self.__client.get_group_name())
        self.__members_list.insert(END, 'online_users:')
        self.__members_list.pack(side=LEFT, fill=BOTH)
        # Scroll
        self.__scroll.config(command=self.__members_list.yview)
        self.__scroll.pack(side=LEFT, fill=Y)
        # Create the place for drawing
        global graphs
        graphs = Canvas(self.__up_line_3, width=500, height=500, bg=BACKGROUND_COLOR)
        graphs.bind('<Button-1>', self.handle_draw)
        graphs.pack(side=LEFT)
        # draw the shapes buttons
        line = Button(up_line_2, text=LINE,
                      command=lambda : self.change_shape_type(LINE))\
            .pack(side=RIGHT)
        circle = Button(up_line_2, text=OVAL,
                        command=lambda : self.change_shape_type(OVAL))\
            .pack(side=RIGHT)
        rectangle = Button(up_line_2, text=RECTANGLE,
                        command=lambda : self.change_shape_type(RECTANGLE))\
            .pack(side=RIGHT)
        triangle = Button(up_line_2, text=TRIANGLE,
                        command=lambda : self.change_shape_type(TRIANGLE))\
            .pack(side=RIGHT)
        ################################### End Gui###########################
        # Call to loop game
        self.game_loop()

    def game_loop(self):
        # Check if user want to leave root
        self.__root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Stage 4: Get messages
        self.recv_messages()
        # Update members list
        self.update_users()
        # Set color
        self.__shape.set_color(initial.get())
        # Callback
        self.__root.after(DELAY, self.game_loop)

def main():
    '''
    Handle the game
    '''
    if len(sys.argv) != NUM_OF_ARGUMENTS:
        print("the correct way is: python client.py "
              "<USER_NAME><SERVER_ADDRES>"
              "<SERVER_PORT><GROUP_NAME>")
        sys.exit()
    else:
        USER_NAME = sys.argv[1]
        SERVER_ADDRESS = sys.argv[2]
        SERVER_PORT = sys.argv[3]
        GROUP_NAME = sys.argv[4]
        if len(USER_NAME) > 20 or len(GROUP_NAME) > 20:
            print('UserName or GroupName should be less '
                  'than 20 letters')
            sys.exit()
        for letter in list(USER_NAME+GROUP_NAME):
            if letter not in LEGIT_LETTERS:
                print('UserName or GroupName should a '
                      'letter or number or _')
                sys.exit()
    root = Tk()
    gui = Gui(root, USER_NAME, SERVER_ADDRESS, SERVER_PORT, GROUP_NAME)
    root.mainloop()

if __name__ == '__main__':
    main()
