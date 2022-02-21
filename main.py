import streamlit as st
import pandas as pd
import numpy as np
# Made by Abraham Holleran
# This was ported over to streamlit in a half hour, it's not polished at all.
# I want to get rid of the duplicate lines of code for each result and each guess.

st.set_page_config(page_title = "Wordle Solver")

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
    word_dict = {}
    for word in dictionary:
        word_set = word
        weight = 0
        for l in word_set:
            # weight += (1/SQRT[word.count(l)])*letter_frequency[l]
            weight += 1 / word.count(l) * letter_frequency[l] * duplicates_weight
        word_dict[word] = int(weight)
    return word_dict


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


st.title("Solver for [Wordle](https://www.nytimes.com/games/wordle/index.html)")
st.markdown('''
### Coded by [Abraham Holleran](https://github.com/Stonepaw90) :sunglasses:
''')
st.write(
    "Welcome to a solver for Wordle! Just enter the guesses and their results and the solver will print out your best options to guess. In this version of Wordle, duplicate letters are weighted less. Also, format the result of your guess by typing a g for a correct letter guessed, y for a letter in the wrong spot, and b for a letter that's not in the correct wordle. For example, you might enter \"bbgyb\". Enjoy!")


fivedict = get_dictionary(n, False)
col = st.columns(2)
ordinal = ['first', 'second', 'third', 'forth', 'fifth', 'sixth']
guess_list = []
result_list = []
for i in range(6):
    guess_list.append(col[0].text_input(f"What was your {ordinal[i]} guess?", max_chars = 5))
    result_list.append(col[1].text_input(f"What was the result of your {ordinal[i]} guess, using only b,y,g?", max_chars=5))

for i in result_list:
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
    input_dict = dict(zip(guess_list, result_list))
    for i, j in input_dict.items():
        fivedict = wordle_filter_dict(recent_guess=i, guess_result=j, dicti=fivedict)
    top_26_dict = common_letters(fivedict)
    word_dict = best_words(fivedict, top_26_dict)
    if len(word_dict) > 1:
        num_display = st.slider("How many suggested guesses should we display? (max 50)", min_value=1, max_value=min(len(word_dict), 50), step = 1, value = 1)
    else:
        st.write("There is just one option.")
        num_display = 1
    df = pd.DataFrame(word_dict.items(), columns = ["Words", "Values"]) #convert to dataframe
    df = df.sort_values(by = 'Values', ascending=False) #Sort by values, not alphabetical
    df = df.reset_index(drop = True) #reset index to 0, 1, 2...
    df = df.head(num_display) #Take top guesses to display
    if num_display == 1:
        st.title("Your best guess is:")
    else:
        st.title("Your best guesses are:")
    st.table(df)
