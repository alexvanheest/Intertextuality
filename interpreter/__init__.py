import matchers
from wordlists import Wordlists
import intertext
from lyric_word_lists import build_lyric_list_wiki_context


# Build trie from saved wordlists:
big_trie = intertext.build_trie_from_wordlists()

# Compare two songs given just their filepaths:
#intertext.compare_songs("../lyrics/nas-1994-illmatic/10-it-aint-hard-to-tell.txt", "../lyrics/survival-of-the-fittest-mobb-deep.txt")
intertext.compare_songs_wiki("Nas", "It Aint Hard To Tell", "Mobb Deep", "Survival of the Fittest")
#
# Compare a song to wordlists:
intertext.compare_song_to_trie("../lyrics/survival-of-the-fittest-mobb-deep.txt", big_trie)
intertext.compare_song_to_trie_wiki("Mobb Deep", "Survival of the Fittest", big_trie)

context_list = build_lyric_list_wiki_context("Nas", "Halftime")
# print "should be word:\t" + context_list[3][0]
# print "should be POS:\t" + context_list[3][3]
# print "should be line no and word no:\t" + str(context_list[3][1]) + ":" + str(context_list[3][2])

# TODO: Look into using a Wikipedia API / package to avoid needing so many wordlists.
# To make this effective, we'll need to combine words to nearby ones to develop some sense of
# context, probably through brute force. Since we're looking for all sorts of wordplay here,
# it wouldn't be too outlandish to brute force this.
# We're also going to need a way to handle disambiguation pages.
# To continue using the trie, which I want to, we could pickle a list of all Wikipedia article titles
# and remove the parenthetical parts? Then offer a much slower search for lev-similar phrases?
# TODO: For database additions, maybe offer a supervised / unsupervised mode?
# In supervised mode, it'll present each reference and check with user to see if it should be
# added. In unsupervised mode, it'll just auto-add things.
# TODO: Add testing suite to project.
# TODO: Look into mapping out themes across songs or albums.
# We could approach this once we have our categorization technique figured out.
# TODO: Look into other NLP projects to see what we can work into this project.
