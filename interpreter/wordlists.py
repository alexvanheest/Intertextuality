import re

# This file will be the ultimate reference point for of all wordlist names and active wordlists
# used by Intertextuality. Avoid naming them individually anywhere else in the project, as this
# will cause undue confusion.


class Wordlists:

    def __init__(self):
        self.wordlists = ["../wordlists/rapper-list.txt",
                         "../wordlists/cleaning-products.txt",
                         "../wordlists/food-brands.txt",
                         "../wordlists/sports.txt",
                         "../wordlists/us-cities.txt",
                         "../wordlists/brands.txt",
                         "../wordlists/alcohol.txt"
                         ]
        self.wl_dict = {}

    # Method that returns a dictionary of the wordlist names and
    def get_wordlist_dictionary(self):
        for item in self.wordlists:
            name = re.search("../wordlists/(.*).txt", item).group(1)
            name = name.split("-")
            final_name = ""
            for word in name:
                final_name += word.title() + " "
            self.wl_dict[item] = final_name[:-1]
        return self.wl_dict
