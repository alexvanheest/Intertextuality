import matchers
import pygtrie
from wordlists import Wordlists
import intertext


# Build trie from saved wordlists:
big_trie = intertext.build_trie_from_wordlists()

# Compare two songs given just their filepaths:
intertext.compare_songs("../lyrics/nas-1994-illmatic/10-it-aint-hard-to-tell.txt", "../lyrics/survival-of-the-fittest-mobb-deep.txt")

# Compare a song to wordlists:
intertext.compare_song_to_trie("../lyrics/survival-of-the-fittest-mobb-deep.txt", big_trie)

# TODO: Look into database storage techniques... perhaps MongoDB???
# TODO: Look into getting lyrics directly from a website, perhaps if Genius has an API?
# TODO: Look into using a Wikipedia API / package to avoid needing so many wordlists.
# TODO: For database additions, maybe offer a supervised / unsupervised mode?
# In supervised mode, it'll present each reference and check with user to see if it should be
# added. In unsupervised mode, it'll just auto-add things.
# TODO: Add metadata to program, create git project, and get this online with MIT license.
# TODO: Create a list of dependencies for the project so it's easy to get and start using.
# TODO: If we use Wikipedia API, we need some way to distinguish what the reference is to if it
# leads to a disambiguation or something... we can try to get some context from around, but it would
# be tough with current implementation!
# TODO: Support context-based searches. If we ever want this, it's better to do sooner.
# Instead of importing just a list of words, make this list into a tuple: (word, (LINE_NO, WORD_NO))
# This will make getting context a breeze, since we can search down to the word position to find words
# most related to it. We can use tokenization of the line to find significant words (NNPs, verbs) that
# can help us make a firmer decision on what's what.
# TODO: Look into mapping out themes across songs or albums.
# We could approach this with something like a thesaurus / Wikipedia package
# TODO: Look into other NLP projects to see what we can work into this project.
