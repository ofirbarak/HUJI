#######################################
# FILE : ex5.py
# WRITERS : Ofir_Birka , ofir , ********* |
#   Netanel_Faummy , netanelf , *********
# EXERCISE : intro2cs ex5 2015-2016
# DESCRIPTION: Stores comparing
#######################################

# Imports
import xml.etree.ElementTree as ET

# Constants
FINE_RATIO = 1.25

# Functions
def get_attribute(store_db, ItemCode, tag):
    '''
    Returns the attribute (tag) 
    of an Item with code: Itemcode in the given store

    '''
    return store_db[ItemCode][tag]


def string_item(item):
    '''
    Textual representation of an item in a store.
    Returns a string in the format of '[ItemCode] (ItemName)'

    '''
    return "[%s]\t{%s}"%(item['ItemCode'], item['ItemName'])


def string_store_items(store_db):
    '''
    Textual representation of a store.
    Returns a string in the format of:
    string representation of item1
    string representation of item2
    ...
    '''
    store_string = ''
    for item in store_db.values():
        store_string += string_item(item) + '\n'
    return store_string


def read_prices_file(filename):
    '''
    Read a file of item prices into a dictionary.  The file is assumed to
    be in the standard XML format of "misrad haclcala".
    Returns a tuple: store_id and a store_db, 
    where the first variable is the store name
    and the second is a dictionary describing the store. 
    The keys in this db will be ItemCodes of the different items and the
    values smaller  dictionaries mapping attribute names to their values.
    Important attributes include 'ItemCode', 'ItemName', and 'ItemPrice'
    '''
    tree = ET.parse(filename)
    root = tree.getroot()
    store_dict = dict()
    for item in root.find('Items'):
        item_dic = dict()
        for element in item:
            item_dic[element.tag] = element.text
        store_dict[item_dic['ItemCode']] = item_dic
    return tree.find('StoreId').text, store_dict


def filter_store(store_db, filter_txt):
    '''
    Create a new dictionary that includes only the items 
    that were filtered by user.
    I.e. items that text given by the user is part of their ItemName. 
    Args:
    store_db: a dictionary of dictionaries as created in read_prices_file.
    filter_txt: the filter text as given by the user.
    '''
    small_store = dict()
    for code in store_db:
        if filter_txt in store_db[code]['ItemName']:
            small_store[code] = store_db[code]
    return small_store


def create_basket_from_txt(basket_txt):
    '''
    Receives text representation of few items (and maybe some garbage 
      at the edges)
    Returns a basket- list of ItemCodes that were included in basket_txt
    '''
    basket_lst = list()
    split_string = basket_txt.split('\n')
    for part in split_string:
        if '[' in part and ']' in part:
            basket_lst.append(part[part.index('[')+1 : part.index(']')])
    return basket_lst


def get_basket_prices(store_db, basket):
    '''
    Arguments: a store - dictionary of dictionaries and a basket - 
       a list of ItemCodes
    Go over all the items in the basket and create a new list 
      that describes the prices of store items
    In case one of the items is not part of the store, 
      its price will be None.
    '''
    # Creating empty list of the current basket prices.
    basket_prices_list = [None] * len(basket)
    for index in range(len(basket)):
        # Checking if the item's code exists in the store.
        if basket[index] in store_db:
            # Checking the ItemPrice by calling the store_db[basket index]
            basket_prices_list[index] = \
                float(store_db[basket[index]]["ItemPrice"])
    return basket_prices_list


def sum_basket(price_list):
    '''
    Receives a list of prices
    Returns a tuple - the sum of the list (when ignoring Nones) 
      and the number of missing items (Number of Nones)
    '''
    prices_sum = 0
    number_of_items_not_priced = 0
    # Counting the number of missing item's prices and summing all the others.
    for price in price_list:
        if price is None:
            number_of_items_not_priced += 1
        else:
            prices_sum += price
    return prices_sum, number_of_items_not_priced


def basket_item_name(stores_db_list, ItemCode):
    ''' 
    stores_db_list is a list of stores (list of dictionaries of 
      dictionaries)
    Find the first store in the list that contains the item and return its
    string representation (as in string_item())
    If the item is not avaiable in any of the stores return only [ItemCode]
    '''
    for index in range(len(stores_db_list)):
        current_store = stores_db_list[index]
        if ItemCode in current_store:
            return string_item(current_store[ItemCode])
    return '[' + ItemCode + ']'


def save_basket(basket, filename):
    ''' 
    Save the basket into a file
    The basket reresentation in the file will be in the following format:
    [ItemCode1] 
    [ItemCode2] 
    ...
    [ItemCodeN]
    '''
    with open(filename, 'w') as basket_file:
        for item in basket:
            basket_file.write('[%s]\n'%(item))


def load_basket(filename):
    '''
    Create basket (list of ItemCodes) from the given file.
    The file is assumed to be in the format of:
    [ItemCode1] 
    [ItemCode2] 
    ...
    [ItemCodeN]
    '''
    read_basket = list()
    basket_file = open(filename, 'r')
    for item in basket_file.read().format().splitlines():
        read_basket.append(item[1:-1])
    return read_basket


def best_basket(list_of_price_list):
    '''
    Arg: list of lists, where each inner list is list of prices as created
    by get_basket_prices.
    Returns the cheapest store (index of the cheapest list) given that a 
    missing item has a price of its maximal price in the other stores *1.25
    '''
    sum_price = [0]*len(list_of_price_list)
    for index_list_price in range(len(list_of_price_list)):
        sub_list = list_of_price_list[index_list_price]
        for price in sub_list:
            # if price is None - Summing the current sum with the FINE the
            # store should get because of the missing item. Otherwise just
            # summing the item's price.
            if price is None:
                sum_price[index_list_price] += \
                    max_price_of_item(sub_list.index(price),
                                      list_of_price_list) * FINE_RATIO
            else:
                sum_price[index_list_price] += price
    return sum_price.index(min(sum_price))


def max_price_of_item(missing_item_index, list_of_price_list):
    '''
    This function will get list of lists, where each inner list is list of
    prices as created by get_basket_prices and index of the missing item.
    We'll return the maximum price of this item sold in other stores.
    '''
    price_every_store = [0] * len(list_of_price_list)
    for index_store in range(len(list_of_price_list)):
        element = list_of_price_list[index_store][missing_item_index]
        if element is not None:
            price_every_store[index_store] = element
    return max(price_every_store)