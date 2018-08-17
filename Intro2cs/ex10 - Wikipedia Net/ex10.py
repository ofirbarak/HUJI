# FILE: ex10.py
# WRITER: Ofir Birka
# EXERCISE: intro2cs ex10 2015-2016
# DESCRIPTION:  Wiki net 

############################################################
# Imports
############################################################

import operator
import copy


############################################################
# Constants
############################################################
DEFAULT_RANKING_NUMBER = 0.9
BEGIN_VALUE = 1
DEFAULT_VALUE_FOR_SUMMARIZE = 0
NAME = 0
COMPARE_IN_VALUE = 1
NO_NEIGHBORS = 0
DEFAULT_VALUE = 0
FIRST_CELL = 0

############################################################
# Functions
############################################################

def read_article_links(file_name):
    """
    Return tuple of articles names
    """
    f = open(file_name, 'r')
    text = f.read()
    text = text.split('\n')
    tuple_names_lst = []
    for row in text:
        if row != '':
            tuple_names_lst.append(tuple(row.split('\t')))
    return tuple_names_lst

############################################################
# Article Class
############################################################


class Article:
    def __init__(self, name):
        '''
        Initialise function
        '''
        self.__name = name                 
        self.__out_neighbors = set() 

    def get_name(self):
        """
        Get article name
        """
        return self.__name

    def add_neighbor(self, neighbor):
        """
        Add a neighbor object to neighbors
        """
        self.__out_neighbors.add(neighbor)

    def get_neighbors(self):
        """
        Return a list of neighbors (string)
        """
        return list(self.__out_neighbors)

    def __repr__(self):
        """
        Return a string that represent the article
        """
        neighbors = []
        # Get names of neighbors articles
        for neighbor in self.__out_neighbors:
            neighbors.append(neighbor.get_name())
        return str((self.get_name(), neighbors))

    def __len__(self):
        """
        Return number of neighbors
        """
        return len(self.__out_neighbors)

    def __contains__(self, article):
        """
        Return True if object article is out neighbor of self
        """
        if article in self.__out_neighbors:
            return True
        return False


############################################################
# WikiNetwork Class
############################################################


class WikiNetwork:
    def __init__(self, link_list=[]):
        """
        Initialize function
        """
        self.__articles_dict = dict()
        self.update_network(link_list)

    def update_network(self, link_list):
        """
        Update list according to new list
        """
        for article_name, neighbor in link_list:
            # Create an article if not exist
            if not self.__contains__(article_name):
                self.__articles_dict[article_name] = Article(article_name)
            # Create a neighbor if not exist
            if not self.__contains__(neighbor):
                self.__articles_dict[neighbor] = Article(neighbor)
            self.__articles_dict[article_name].add_neighbor(
                self.__articles_dict[neighbor])

    def get_articles(self):
        """
        Return all articles
        """
        return list(self.__articles_dict.values())

    def get_titles(self):
        """
        Return list of all articles's titles
        """
        return list(self.__articles_dict.keys())

    def __contains__(self, article_name):
        """
        Check if network contains a specific article
        """
        for article in self.get_titles():
            if article == article_name:
                return True
        return False

    def __len__(self):
        """
        Return number of articles in network
        """
        return len(self.__articles_dict)

    def __repr__(self):
        """
        Return a string represents the network
        """
        return str(self.__articles_dict.__repr__())

    def __getitem__(self, article_name):
        """
        Return an object
        """
        if self.__contains__(article_name):
            return self.__articles_dict[article_name]
        raise KeyError(article_name)

    def page_rank(self, iters, d=DEFAULT_RANKING_NUMBER):
        """
        Return a sorted list of ranking articles according to
            Page Rank algorithm
        """
        # Begin situation
        page_dict = {}
        titles = self.get_titles()
        for i in range(self.__len__()):
            page_dict[titles[i]] = BEGIN_VALUE
        # Run transforms
        for iteration_number in range(iters):
            pre_page_dict = copy.deepcopy(page_dict)
            for article in page_dict.keys():
                page_dict[article] = \
                    d*self.sigema_per_article(self.__getitem__(article),
                                              pre_page_dict) \
                    + (1-d)
        orginized_articles = \
            self.sort_big_to_smallest_and_return_names(page_dict)
        return orginized_articles

    def sigema_per_article(self, article_to_sum, rank_dict):
        """
        Help function
        This function summarize all ranking of all articles divide there outs
        I mean - Sigma(1<=i<=n)[rank(i)/out_neighbors(i)] , n - number of
        articles
        """
        sum_all = DEFAULT_VALUE_FOR_SUMMARIZE
        for article in self.get_articles():
            if article.__contains__(article_to_sum):
                sum_all += rank_dict[article.get_name()] / article.__len__()
        return sum_all

    def sort_big_to_smallest_and_return_names(self, list_to_sort):
        """
        Gets a dictionary and sort it from biggest to smallest and return
        the names list
        """
        sorted_page_list = sorted(sorted(list_to_sort.items()),
                                  key=operator.itemgetter(COMPARE_IN_VALUE),
                                  reverse=True)
        orginized_articles = []
        # Get names of biggest to smallest ranking articles
        for item in sorted_page_list:
            orginized_articles.append(item[NAME])
        return orginized_articles

    def jaccard_index(self, article_name):
        """
        Jaccard articles sorted
        :param article_name:
        :return: A sorted list of biggest index jsccard to smallest
        """
        if not self.__contains__(article_name):
            return None
        get_article_object = self.__getitem__(article_name)
        if get_article_object.__len__() <= NO_NEIGHBORS:
            return None
        jaccard_dict = {}
        for article_object in self.get_titles():
            jaccard_dict[article_object] = \
                self.get_jaccard_value(self.__getitem__(article_object),
                                       get_article_object)
        orginized_list = \
            self.sort_big_to_smallest_and_return_names(jaccard_dict)
        return orginized_list

    def get_jaccard_value(self, article1, article2):
        """
        Return the jaccard value - |A intersection B|/|A union B|
        """
        set_article1 = set(article1.get_neighbors())
        set_article2 = set(article2.get_neighbors())
        return len(set_article1.intersection(set_article2))/\
               len(set_article1.union(set_article2))

    def travel_path_iterator(self , article_name):
        """
        Return iterator according the path
        """
        path = iter([])
        if not self.__contains__(article_name):
            return path
        # Count number of 'in neighbors' each article in self
        in_neighbors_dict = {}
        for article_name_small in self.get_titles():
            in_neighbors_dict[article_name_small] = \
                DEFAULT_VALUE_FOR_SUMMARIZE
        for article in self.get_articles():
            for neighbor in article.get_neighbors():
                in_neighbors_dict[neighbor.get_name()] += 1
        # Get best path
        path = self.get_best_path([], article_name, in_neighbors_dict)
        return path.__iter__()

    def get_best_path(self, iter_path, article_name, in_neighbors):
        """
        Get the path and return a list of travel
        """
        article = self.__getitem__(article_name)
        if article.__len__() == NO_NEIGHBORS or article_name in iter_path:
            iter_path.append(article_name)
            return iter_path
        iter_path.append(article_name)
        neighbors_specific_article_in = dict()
        for neighbor in article.get_neighbors():
            neighbors_specific_article_in[neighbor.get_name()] = \
                in_neighbors[neighbor.get_name()]
        article = \
            self.sort_big_to_smallest_and_return_names(
                neighbors_specific_article_in)[FIRST_CELL]
        return self.get_best_path(iter_path, article, in_neighbors)

    def friends_by_depth(self, article_name, depth):
        """
        Return all articles from d distance
        """
        if not self.__contains__(article_name):
            return None
        return list(self.get_friend_less_given_distance(
            set(), self.__getitem__(article_name), depth))

    def get_friend_less_given_distance(self, friends, article, depth):
        """
        Return a set of all friends from a given distance
        """
        if depth == 0:
            friends.add(article.get_name())
            return friends
        friends.add(article.get_name())
        for neighbor in article.get_neighbors():
            friends.add(neighbor.get_name())
            friends.union(self.get_friend_less_given_distance(friends,
                                                              neighbor,
                                                              depth-1))
        return friends


############################################################
# Iterator Class
############################################################
class Iterator:
    def __init__(self, length):
        self.i = DEFAULT_VALUE
        self.length = length

    def __next__(self):
        if self.i < self.length:
            result = self.i
            self.i += 1
            return result
        else:
            raise StopIteration

    def __iter__(self):
        return self
