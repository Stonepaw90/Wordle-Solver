#import random
import streamlit as st
# Made by Abraham Holleran
#SQRT = {i: i ** .5 for i in range(1, n + 1)}
#CBRT = {i: i ** (1 / 3) for i in range(1, n + 1)}
n = 5
def contains_duplicates(string):
    return len(set(string)) < len(string)
    # true if duplicates


def get_dictionary(word_len, remove_duplicates=False):
    """
    word_len: the length of words that you want the resulting dictionary to be.
    This function opens the words_alpha file and returns only the words of length word_len. It will remove words with duplicate letters if you desire.
    returns:: a list of all english words of length word_len
    """
    word_file = open("words_alpha.txt")
    words = word_file.readlines()
    word_file.close()
    trimmed_dictionary = [i[:-1] for i in words if len(i[:-1]) == word_len]
    if remove_duplicates:
        no_duplicates = [i for i in trimmed_dictionary if len(set(i)) == word_len]
        return no_duplicates
    else:
        return trimmed_dictionary


def common_letters(word_dictonary):
    """
    word_dictionary: The dictionary of words
    This function counts the occurances of each letter in the dictionary
    returns:: a dictionary object containing each letter paired with its number of occurances.
    """
    letters = {}
    for word in word_dictonary:
        for letter in word:
            if letter not in letters:
                letters[letter] = 0  # 1 will be added soon
            letters[letter] += 1
    return letters


def best_words(dictionary, letter_frequency, duplicates_weight=1):
    #letter_frequency
    """
    dictionary:: the dictionary to look through
    letter_frequency:: the number of occurances of each letter
    duplicates:: a bool that triggers duplicates in letters off
    This function finds the words in the dictionary that contain the most common letters.
    It evaluates each dictionary word by summing up the occurences for each letter.
    returns a list of tuples and the tuples are the weight with the word.
    """
    word_list = []
    for word in dictionary:
        word_set = word
        weight = 0
        for l in word_set:
            # weight += (1/SQRT[word.count(l)])*letter_frequency[l]
            weight += 1 / word.count(l) * letter_frequency[l] * duplicates_weight
        word_list.append((weight, word))

    return sorted(word_list, reverse=True)


def wordle_filter_by_result(dict_word, guess_word, result_of_guess):
    """
    Checks each word and sees if it could be correct
    dict_word:: the word to Checks
    guess_word:: the most recent guess that allows us to filter the dictionary
    result_of_guess:: a key to help us see which letters of the guess are right.
    for example: bwwbc
    c means correct letter correct location, used when you guess the right letter in the final word.
    w means correct letter wrong location, used when your word contains a letter in the final word.
    b means wrong letter, used when a letter is not in the final answer
    returns:: boolean for if the test passed or failed
    """
    for idx, letter in enumerate(result_of_guess):
        if letter == "g":
            if guess_word[idx] != dict_word[idx]:
                return False
        elif letter == "y":
            if (guess_word[idx] not in dict_word[:idx] + dict_word[idx + 1:]):
                return False
        elif letter == "b":
            if guess_word[idx] in dict_word:
                return False
    return True


def wordle_filter_dict(recent_guess, guess_result, dicti):
    """
    This function goes through the list dictionary and only returns the elements that pass
    the filter test.
    returns:: a list
    """
    result = []
    for word in dicti:
        if wordle_filter_by_result(dict_word=word, guess_word=recent_guess, result_of_guess=guess_result):
            result.append(word)
    return result


#def main(n=5):
#    fivedict = get_dictionary(n, False)
#    fivedict = wordle_filter_dict(recent_guess="penis", guess_result="bybbb", dicti=fivedict)
#    fivedict = wordle_filter_dict(recent_guess="ghoul", guess_result="byybb", dicti=fivedict)
#    fivedict = wordle_filter_dict(recent_guess="hoard", guess_result="yybyb", dicti=fivedict)
#    # fivedict = wordle_filter_dict(recent_guess = "xylic", guess_result = "bgbgg", dicti = fivedict)
#    top_26_dict = common_letters(fivedict)
#    guess = best_words(fivedict, top_26_dict)[0][1]
#    st.write(guess)


st.title("Solver for [Wordle](https://www.nytimes.com/games/wordle/index.html)")
st.markdown('''
### Coded by [Abraham Holleran](https://github.com/Stonepaw90) :sunglasses:
''')
st.write(
    "Welcome to a solver for Wordle! Just enter the result of your guess and the solver will print out your best option for a guess. In this version of Wordle, duplicate letters are weighted less. Also, format the result of your guess by typing a g for a correct letter guessed, y for a letter in the wrong spot, and b for a letter that's not in the correct wordle. For example, you might enter \"bbgyb\". Enjoy!")


fivedict = get_dictionary(n, False)
col = st.columns(2)

# guess_1 = col[0].text_input("What was your first guess?", max_chars = 5)
# result_1 = col[1].text_input("What was the result of your first guess, using only b,y,g?", max_chars = 5)
# guess_2 = col[0].text_input("What was your second guess?", max_chars = 5)
# result_2 = col[1].text_input("What was the result of your second guess, using only b,y,g?", max_chars = 5)
# guess_3 = col[0].text_input("What was your third guess?", max_chars = 5)
# result_3 = col[1].text_input("What was the result of your third guess, using only b,y,g?", max_chars = 5)
# guess_4 = col[0].text_input("What was your forth guess?", max_chars = 5)
# result_4 = col[1].text_input("What was the result of your forth guess, using only b,y,g?", max_chars = 5)
# guess_5 = col[0].text_input("What was your fifth guess?", max_chars = 5)
# result_5 = col[1].text_input("What was the result of your fifth guess, using only b,y,g?", max_chars = 5)
# guess_6 = col[0].text_input("What was your sixth guess?", max_chars = 5)
# result_6 = col[1].text_input("What was the result of your sixth guess, using only b,y,g?", max_chars = 5)
ordinal = ["first", "second", "third", "forth", "fifth", "sixth"]
guess_list = []
result_list = []
for i in range(6):
    pass
guess_1 = col[0].text_input("What was your first guess?", max_chars = 5)
result_1 = col[1].text_input("What was the result of your first guess, using only b,y,g?", max_chars = 5)
guess_2 = col[0].text_input("What was your second guess?", max_chars = 5)
result_2 = col[1].text_input("What was the result of your second guess, using only b,y,g?", max_chars = 5)
guess_3 = col[0].text_input("What was your third guess?", max_chars = 5)
result_3 = col[1].text_input("What was the result of your third guess, using only b,y,g?", max_chars = 5)
guess_4 = col[0].text_input("What was your forth guess?", max_chars = 5)
result_4 = col[1].text_input("What was the result of your forth guess, using only b,y,g?", max_chars = 5)
guess_5 = col[0].text_input("What was your fifth guess?", max_chars = 5)
result_5 = col[1].text_input("What was the result of your fifth guess, using only b,y,g?", max_chars = 5)
guess_6 = col[0].text_input("What was your sixth guess?", max_chars = 5)
result_6 = col[1].text_input("What was the result of your sixth guess, using only b,y,g?", max_chars = 5)




for i in [result_1, result_2, result_3, result_4, result_5, result_6]:
    done = False
    break_flag = False
    if i == "ggggg":
        st.title("You did it! Congratulations.")
        done = True
    for j in i:
        if j not in ["g","y","b"]:
            break_flag = True
    if break_flag:
      st.write("Please enter either `g`, `y`, or `b`.")
      st.exit()
if not done:
    input_dict = {
        guess_1: result_1,
        guess_2: result_2,
        guess_3: result_3,
        guess_4: result_4,
        guess_5: result_5,
        guess_6: result_6,
    }
    fivedict = wordle_filter_dict(recent_guess=guess_1, guess_result=result_1, dicti=fivedict)
    fivedict = wordle_filter_dict(recent_guess=guess_2, guess_result=result_2, dicti=fivedict)
    fivedict = wordle_filter_dict(recent_guess=guess_3, guess_result=result_3, dicti=fivedict)
    fivedict = wordle_filter_dict(recent_guess=guess_4, guess_result=result_4, dicti=fivedict)
    fivedict = wordle_filter_dict(recent_guess=guess_5, guess_result=result_5, dicti=fivedict)
    fivedict = wordle_filter_dict(recent_guess=guess_6, guess_result=result_6, dicti=fivedict)
    top_26_dict = common_letters(fivedict)
    guess = best_words(fivedict, top_26_dict)[0][1]
    st.title(f"Your best guess is: {guess}")