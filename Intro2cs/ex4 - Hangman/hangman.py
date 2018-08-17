#######################################
# FILE : ex4.py
# WRITER : Ofir_Birka , ofir , 316389410
# EXERCISE : intro2cs ex4 2015-2016
# DESCRIPTION: The game 'HangMan'
#######################################
# Imports
from hangman_helper import  *

# Constants
__INIT_ALPHA_ORDER__ = 97
DEFAULT_VALUE = 0
HINT = 1
LETTER = 2
PLAY_AGAIN = 3
NUMBER_OF_LETTERS_IN_ENGLISH = 26
LENGTH_LETTER = 1


# Functions
def update_word_pattern(word, pattern, letter):
    """
    Update word according to pattern and a letter
    :param word: Guessing word
    :param pattern: Pattern of word, with guessed letters
    :param letter: Letter to fill in word
    :return: Pattern to guess after fill the guessed letter
    """
    ret_word = list(pattern)
    for index_latter_in_word in range(len(word)):
        if ret_word[index_latter_in_word] == '_':
            if word[index_latter_in_word] == letter:
                ret_word[index_latter_in_word] = letter

    return ''.join(ret_word)


def run_single_game(words_list):
    """
    Run single game
    :param words_list: Words list (from random in file hangman.py
    :return: No return
    """
    # Initialize game
    # 1. Get a word from list, using hangman_helper.py
    word = get_random_word(words_list)
    # 2.1 Guess list is empty, first pattern is empty and legth =
    #       length of the word
    #guess_list = list() # List of all guesses (including the wrong guesses)
    # pattern = '______' (length '_' as length of 'word'
    pattern = '_' * len(word)
    error_count = DEFAULT_VALUE # Number of wrong guesses
    # 3. Message for user = DEFAULT_MSG (from hangman_helper.py)
    msg_for_user = DEFAULT_MSG
    wrong_guess_lst = list() # List of wrong guesses without returning words

    # Playing the game
    while (error_count < MAX_ERRORS) and ('_' in pattern):
        # Print the current situation
        display_state(pattern, error_count, wrong_guess_lst, msg_for_user)
        # Getting input
        input_help = get_input()
        # Is input for insert a letter
        if input_help[0] == LETTER:
            letter = input_help[1]
            # If unexpected input: Legth > 1 or No letter or No lower case -->
            #   send message and wait for next input
            if len(letter)> LENGTH_LETTER or not letter.isalpha() or not letter.islower():
                msg_for_user = NON_VALID_MSG
            # Else if letter already chosen
            elif letter in wrong_guess_lst or letter in pattern:
                msg_for_user = ALREADY_CHOSEN_MSG + letter
            # Else if guessed letter in the word
            elif letter in word:
                # Update pattern
                pattern = update_word_pattern(word, pattern, letter)
                #guess_list.append(letter)
                msg_for_user = DEFAULT_MSG
            # Else letter not in word
            else:
                # Check wrong_guess_lst needs to be updated
                if letter not in wrong_guess_lst:
                    wrong_guess_lst.append(letter)
                # Add letter to guess_list because it already passed the if that
                #   check if that letter was guessed
                error_count += 1
                msg_for_user = DEFAULT_MSG
        # Is input for getting a hint (there is not need to check it,
        #       it is obvious, but done for more security)
        elif input_help[0] == HINT and input_help[1]:
            words_list_filter = filter_words_list(words_list, pattern, wrong_guess_lst)
            msg_for_user = HINT_MSG + choose_letter(words_list_filter, pattern)

    # End of game
    if '_' not in pattern:
        # Player win
        msg_for_user = WIN_MSG
    else:
        # Player loss
        msg_for_user = LOSS_MSG + word
    # Call hangman_helper.display_state
    display_state(pattern, error_count, wrong_guess_lst, msg_for_user, True)


def filter_words_list(words, pattern, wrong_guess_list):
    """
    Filter letters and return the words list accordingly
    """
    # Filter words
    length_pattern = len(pattern) # Done because of high use in the loop
    words_copy = list(words)
    for word in words:
        to_remove = False
        # Filter words that not in length of the pattern
        if len(word) != length_pattern:
            # Delete that element
            to_remove = True
        else:
            # Filter words not identity to pattern (in letters)
            for letter_in_word in range(len(word)):
                # If contain same letters in same place in revealed letters
                #   in pattern
                if pattern[letter_in_word] != '_':
                    if word[letter_in_word] != pattern[letter_in_word]:
                        to_remove = True
                        break
                # The letter in word is placed wrong
                elif word[letter_in_word] in pattern:
                    to_remove = True
                    break
                # Filter words that there are letters are in wrong_guess_list
                if word[letter_in_word] in wrong_guess_list:
                    to_remove = True
                    break
        if to_remove:
            words_copy.remove(word)

    return words_copy


def letter_to_index(letter):
    '''
    Returns the index of the given letter in an alphabet list
    '''
    return ord(letter.lower()) - __INIT_ALPHA_ORDER__


def index_to_letter(index):
    '''
    Returns the index of the given letter in an alphabet list
    '''
    return chr(index + __INIT_ALPHA_ORDER__)


def choose_letter(words, pattern):
    """
    Return the most common letter in words list
    """
    count_amount_each_letter = [0]*NUMBER_OF_LETTERS_IN_ENGLISH
    for word in words:
        for letter in word:
            if letter not in pattern:
                count_amount_each_letter[letter_to_index(letter)] += 1

    return index_to_letter(count_amount_each_letter.index(
        max(count_amount_each_letter)))


def main():
    """
    Main function
    """
    words_list = load_words()
    response = (PLAY_AGAIN, True) # Default value to begin the loop
    while response[0] == PLAY_AGAIN and response[1]:
        run_single_game(words_list)
        response = get_input()


if __name__ == "__main__":
    start_gui_and_call_main(main)
    close_gui()
