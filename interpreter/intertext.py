import pygtrie
from wordlists import Wordlists
import matchers


# This file will provide a series of methods based on the matchers and wordlists in this directory.
# It doesn't function like a class: rather, it's a series of wrappers around functionality provided
# by other files and objects in this project that is intended for wider use.


# This method will build and return a trie from the wordlists given in the Wordlist class.
def build_trie_from_wordlists():
    # Create Wordlists object
    wl = Wordlists()
    # Build the trie that will contain all of the words in each wordlist
    big_trie = pygtrie.StringTrie()
    for wordlist in wl.wordlists:
        with open(wordlist) as list_file:
            words_as_list = list_file.read().splitlines()
            for word in words_as_list:
                big_trie[word] = wordlist
    return big_trie


# Method to convert a text file with lyrics into a list of words, removing unneeded punctuation.
def build_lyric_list(filepath):
    with open(filepath) as f:
        lyric_word_list = f.read()\
            .replace("[", "").replace("]", "").replace(":", "").replace("\n", " ") \
            .replace("?", "").replace(",", "").replace(".", "").replace("!", "") \
            .replace("\"", "").replace("'", "").replace("-", "").split(" ")
    return lyric_word_list


# Method that takes two filepaths to lyrics and uses trie comparison to find and print similar phrases
def compare_songs(lyricpath1, lyricpath2):
    # Build lists
    path1_list = build_lyric_list(lyricpath1)
    path2_list = build_lyric_list(lyricpath2)

    # Build a trie for path1
    path1_trie = matchers.build_trie_range(4, 14, path1_list)

    # Compare the lyrics
    comparison_dict = matchers.match_with_trie(4, 14, path2_list, path1_trie)

    # Display non-unique results
    print "\nComplete Results:"
    for key, val in comparison_dict.iteritems():
        print key

    # Display unique results
    print "\n\nUnique Results:"
    unique_list = comparison_dict.keys()
    unique_list = matchers.condense(unique_list)
    for item in unique_list:
        print item


# Method that compares a song at a given path to a given trie
def compare_song_to_trie(lyricpath, big_trie):
    final_dict = matchers.match_with_trie(1, 10, build_lyric_list(lyricpath), big_trie)
    wl = Wordlists()
    wordlist_dict = wl.get_wordlist_dictionary()
    print "\n\nLyric Comparison to Wordlists:"
    for key, val in final_dict.iteritems():
        print wordlist_dict[val] + ":\t\t" + key
