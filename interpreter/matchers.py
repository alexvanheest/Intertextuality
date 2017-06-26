from collections import Counter
import numpy as np
import pygtrie

# A series of methods that will be used to help match lyrics to references.


# Levenshtein distance (method from wikibooks.org)
def levenshtein(source, target):
    if len(source) < len(target):
        return levenshtein(target, source)

    # So now we have len(source) >= len(target).
    if len(target) == 0:
        return len(source)

    # We call tuple() to force strings to be used as sequences
    # ('c', 'a', 't', 's') - numpy uses them as values by default.
    source = np.array(tuple(source))
    target = np.array(tuple(target))

    # We use a dynamic programming algorithm, but with the
    # added optimization that we only need the last two rows
    # of the matrix.
    previous_row = np.arange(target.size + 1)
    for s in source:
        # Insertion (target grows longer than source):
        current_row = previous_row + 1

        # Substitution or matching:
        # Target and source items are aligned, and either
        # are different (cost of 1), or are the same (cost of 0).
        current_row[1:] = np.minimum(
                current_row[1:],
                np.add(previous_row[:-1], target != s))

        # Deletion (target grows shorter than source):
        current_row[1:] = np.minimum(
                current_row[1:],
                current_row[0:-1] + 1)

        previous_row = current_row

    return previous_row[-1]


# Method that turns Levenshtein distance into a fairly normalized value. Lesser means that
# the words are more similar.
def lev_av_percent(source, target):
    average_length = (len(source) + len(target)) / 2.0
    return levenshtein(source, target) / average_length


# Method that takes in a length (number of words), list of lyrics as words, and
# a Counter containing desired keywords and returns a list of matches as tuples
def matches_by_length_with_counters(length, lyric_word_list, target_counter):
    # Chunk words up based on specified length:
    ctr = 1
    match_list = []
    for idx in range(len(lyric_word_list) - length + 1):
        current_string = lyric_word_list[idx]
        while idx + ctr < idx + length:
            current_string += " " + lyric_word_list[idx+ctr]
            ctr += 1
        ctr = 1
        if target_counter[current_string] > 0:
            match_list.append(current_string)
    return match_list


# Wrapper method around matches_by_length that takes a range of values to pass as
# lengths.
def match_with_counters(min_length, max_length, lyric_word_list, target_counter):
    big_dictionary = {}
    for a in range(min_length, max_length+1):
        big_dictionary[a] = matches_by_length(a, lyric_word_list, target_counter)
    return big_dictionary


# Returns a list of words (of length specified) that have specified Levenshtein ratio.
def lev_by_length(length, lyric_words_list_one, lyric_words_list_two, lev_ratio):
    # Chunk words up based on length:
    ctr1 = 1
    ctr2 = 1
    match_list = []
    for idx in range(len(lyric_words_list_one) - length + 1):
        current_string_one = lyric_words_list_one[idx]
        while idx + ctr1 < idx + length:
            current_string_one += " " + lyric_words_list_one[idx+ctr1]
            ctr1 += 1
        for idx2 in range(len(lyric_words_list_two) - length + 1):
            current_string_two = lyric_words_list_two[idx2]
            while idx2 + ctr2 < idx2 + length:
                current_string_two += " " + lyric_words_list_two[idx2 + ctr2]
                ctr2 += 1
            if lev_av_percent(current_string_one, current_string_two) < lev_ratio:
                match_list.append(current_string_one)
            ctr2 = 1
        ctr1 = 1
    return match_list


# Runs above methods with a range of lengths
def lev_ratios(min_length, max_length, lyric_words_list_one, lyric_words_list_two, lev_ratio):
    total_match_list = []
    for x in range(min_length, max_length+1):
        print "WORD COUNT: " + str(x)
        total_match_list += lev_by_length(x, lyric_words_list_one, lyric_words_list_two, lev_ratio)
    total_match_list = list(set(total_match_list))
    total_match_list.sort(lambda x,y: cmp(len(x), len(y)))  # order by length (shortest first)
    print "Running match condenser..."
    total_match_list = match_condenser(total_match_list)
    total_match_list.sort(lambda x, y: cmp(len(x), len(y)))
    while len(match_condenser(total_match_list)) != len(match_condenser(total_match_list)):
        total_match_list = list(set(total_match_list))
        print "Running match condenser again..."
        match_condenser(total_match_list)
    return list(set(match_condenser(total_match_list)))


# Takes in the final total match list and if any are just parts of others, don't include it
# in the final returned list. Recursion Is Alive!!
# Not totally accurate yet... maybe run in a while loop and run again and again until it gets
# the same list length twice in a row??
def match_condenser(final_list):
    if len(final_list) == 1:   # there's only one element left: just return it
        return final_list
    else:
        # Separate first element in list from others: we will check first against others
        within = False      # set to true if the separated value is found within another value in list
        keyword = final_list[0]     # value separated from others
        print keyword           # debug
        for item in final_list[1:]:
            if keyword in item:
                within = True
                break

        if within is True:      # means that we don't need to include this separated value
            return match_condenser(final_list[1:])
        else:
            return final_list[0:1] + match_condenser(final_list[1:])


# Method I should use to call match_condenser. It sorts and removes duplicates before
# condensing.
def condense(final_list):
    # First, remove duplicates:
    final_list = list(set(final_list))
    # Then, sort:
    final_list.sort(lambda x, y: cmp(len(x), len(y)))
    # Finally, condense:
    return match_condenser(final_list)


# Method that takes in a trie and a word list and finds matches of a certain word length.
# Returns a dictionary where the key is the matching word/phrase and the value is the wordlist
# it's from.
# Caveat: We need a different method call for all different word counts, which is a bummer.
def match_by_length_with_trie(length, lyric_word_list, big_trie):
    # Chunk words up based on specified length:
    ctr = 1
    match_dict = {}
    for idx in range(len(lyric_word_list) - length + 1):
        current_string = lyric_word_list[idx]
        while idx + ctr < idx + length:
            current_string += " " + lyric_word_list[idx + ctr]
            ctr += 1
        ctr = 1
        if current_string in big_trie and current_string not in match_dict:     # only attempt to add if new
            match_dict[current_string] = big_trie[current_string]   # {current_string: type of reference}
    return match_dict


# Method to call several by-length methods in a row.
def match_with_trie(min_length, max_length, lyric_word_list, big_trie):
    final_dict = {}
    for x in range(min_length, max_length+1):
        final_dict = dict(final_dict.items() + match_by_length_with_trie(x, lyric_word_list, big_trie).items())
    return final_dict


# Builds a trie from a lyric list and a number of words. Also takes in a final trie as it builds
# directly onto it and returns it.
def build_trie_by_length(length, word_list, final_trie):
    ctr = 1
    for idx in range(len(word_list) - length + 1):
        current_string = word_list[idx]
        while idx + ctr < idx + length:
            current_string += " " + word_list[idx + ctr]
            ctr += 1
        ctr = 1
        final_trie[current_string] = True
    return final_trie


# Takes in a lyric list and a min and max phrase length and returns a trie
# with every combination of those phrases
def build_trie_range(min_length, max_length, word_list):
    final_trie = pygtrie.StringTrie()
    for x in range(min_length, max_length+1):
        print "Building trie for phrases of length " + str(x)
        final_trie = build_trie_by_length(x, word_list, final_trie)
    return final_trie
