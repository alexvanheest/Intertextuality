from PyLyrics import PyLyrics

# Contains all methods to do with lyric word lists.
# To clarify, when I use the phrase "lyric word lists," I'm referring to something very specific:
# it's a Python list of words separated by spaces from the lyrics with punctuation removed.


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
