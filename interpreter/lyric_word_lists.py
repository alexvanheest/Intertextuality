from PyLyrics import PyLyrics
from nltk import pos_tag, word_tokenize

# Contains all methods to do with lyric word lists.
# To clarify, when I use the phrase "lyric word lists," I'm referring to something very specific:
# it's a Python list of words separated by spaces from the lyrics with punctuation removed.
# I'd make this a class, but it's just a list, so I think that'd be overkill.
# However, if we turned this into a class, we can store the words as a list and the lines as a list... hmmm...


# Method to convert a text file with lyrics into a list of words, removing unneeded punctuation.
def build_lyric_list(filepath):
    with open(filepath) as f:
        lyric_word_list = replace_and_listify(f.read())
    return lyric_word_list


# Method to build lyric list with an artist and song title instead of local lyrics
def build_lyric_list_wiki(artist, song):
    lyrics_as_string = PyLyrics.getLyrics(artist, song)
    lyric_word_list = replace_and_listify(lyrics_as_string)
    return lyric_word_list


# Method that performs standard replacements and list-ifies words in string-formatted lyrics
def replace_and_listify(lyric_word_list):
    return lyric_word_list.replace("[", "").replace("]", "").replace(":", "").replace("\n", " ") \
                          .replace("?", "").replace(",", "").replace(".", "").replace("!", "") \
                          .replace("\"", "").replace("'", "").replace("-", "").split(" ")


# Method to build a lyric list with wiki implementation and including line number and word number on line
def build_lyric_list_wiki_context(artist, song):
    lyrics_as_string = PyLyrics.getLyrics(artist, song)
    lyrics_as_lines = lyrics_as_string.split("\n")
    ret_list = []   # format of each word entry: [ word, line_no, word_no, POS ]
    for jdx in range(0,len(lyrics_as_lines)):
        # part of speech tag each line using nltk so we can add that to the context metadata for each word
        tokd_line = pos_tag(word_tokenize(lyrics_as_lines[jdx]))
        for idx in range(0,len(lyrics_as_lines[jdx].split())):
            ret_list.append([tokd_line[idx][0], jdx, idx, tokd_line[idx][1]])
    return ret_list