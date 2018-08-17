# FILE: ex12.py
# WRITER: Ofir Birka, Bar Vered
# EXERCISE: intro2cs ex12 2015-2016
# DESCRIPTION: Client

# Imports
from online_info_client import *

# Constants
CONNECT_MSG = 'join'
SHAPE_MSG = 'shape'
LINE = 'line'
RECTANGLE = 'rectangle'
OVEL = 'oval'
TRIANGLE = 'triangle'
LEAVE_MEG = 'leave'
ERROR_MSG = 'error'
SEPERATE_SECTION = ';'
END_CHAR = '\n'
USERS_MSG = 'users'
USERS_SPERATOR = ','
MSGDELIM = b'\n'
DELIM = ';'
FIELDSEP = b','
MAX_MSG_SIZE = 1048
ENCODING_STYLE = 'utf-8'


class Client:
    '''
    Represents a client in server-client module
    '''
    def __init__(self, username, server_address, server_port,group_name):
        self.__sock = self.generate_new_socket(server_address, server_port)
        self.__members_names = list()
        self.__groupname = group_name
        self.__username = username


    def generate_new_socket(self, server_address, server_port):
        '''
        generate a new socket and start a connection
        '''
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server_address, int(server_port)))
            return sock
        except:
            traceback.print_exc()

    def get_username(self):
        return self.__username

    def get_group_name(self):
        return self.__groupname

    def get_list_members(self):
        return self.__members_names

    def set_list_members(self, members):
        self.__members_names = members

    def add_member(self, member_name):
        split = member_name[0].split(',')
        if isinstance(member_name, str):
            self.__members_names.append(member_name)
        else:
            for name in split:
                if name in self.__members_names or name == self.__username:
                    pass
                else:
                    self.__members_names.append(name)

    def del_member_from_list(self, username):
        if username in self.__members_names:
            self.__members_names.remove(username)

    def exchange(self, msg):
        self.__sock.sendall(msg+MSGDELIM)
        return self.check_if_there_is_message_from_server()

    def check_if_there_is_message_from_server(self):
        data = b''
        r,w,x = select.select([self.__sock], [], [], 0.01)
        for sock in r:
            if sock == self.__sock:
                data += r[0].recv(MAX_MSG_SIZE)
        return ((data[:-1]).decode(encoding=ENCODING_STYLE)).split(DELIM)

    def send_join_to_server(self):
        '''
        Send a request for connect to server,
        :return: response from server
        '''
        msg = CONNECT_MSG + SEPERATE_SECTION + self.__username + \
              SEPERATE_SECTION + self.__groupname
        return self.exchange(bytes(msg.encode()))

    def recv_join_from_server(self, msg_from_server):
        '''
        Check if new user was joined, if yes add him to self
        '''
        s_username = msg_from_server
        self.__members_names.append(s_username)

    def send_add_shape_to_server(self, shape, coord, shape_color):
        '''
        Send a shape to server
        :return: response from server
        '''
        str_coord = ''
        for x,y in coord:
            str_coord += str(x) + ',' + str(y) + ','
        msg = SHAPE_MSG + SEPERATE_SECTION + shape + SEPERATE_SECTION + \
              str_coord[:-1] + SEPERATE_SECTION + shape_color
        return self.exchange(bytes(msg.encode()))

    def recv_shape_from_server(self, msg_from_server):
        '''
        Recieve a shape if this from a new member draw it
        '''
        s_username, s_shape, s_coordinates, s_color = \
            msg_from_server.split(SEPERATE_SECTION)
        return (s_shape, s_coordinates, s_color)

    def send_leave_to_server(self):
        '''
        Send a leave message
        :return: response from server
        '''
        msg = LEAVE_MEG + SEPERATE_SECTION + self.__username + END_CHAR
        return self.exchange(bytes(self.__username.encode()))

    def recv_left_from_server(self, msg_from_server):
        '''
        If request sent from the client who want's to
            leave - close the program
        Otherwise - got a 'leave' from a menber and update members list
        '''
        s_username = msg_from_server.split(SEPERATE_SECTION)
        if s_username == self.__username:
            # Request is from this client
            # Close the window
            pass
            self.__sock.close()
        else:
            # Got a message from server that one member was left
            self.__members_names.remove(s_username)

    def recv_change_in_members_from_server(self, msg_from_server):
        '''
        Get a message on changes in users. Update members list
        '''
        self.__members_names = msg_from_server.split(USERS_SPERATOR)
