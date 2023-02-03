from deck_ids import ids

if __name__ == "__main__":
    with ids.open():
        ids.generate("漢字::Chapter 5::kanji", 1782011013)
        ids.generate("漢字::Chapter 5::jp", 1949414604)
        ids.generate("漢字::Chapter 5::en", 1710431784)

        ids.generate("漢字::Chapter 6::kanji", 2078368541)
        ids.generate("漢字::Chapter 6::jp", 1452725153)
        ids.generate("漢字::Chapter 6::en", 2083697682)

        ids.generate("語彙::Chapter 5::jp", 1774175474)
        ids.generate("語彙::Chapter 5::en", 1585563342)

        ids.generate("語彙::Chapter 6::jp", 1301141718)
        ids.generate("語彙::Chapter 6::en", 1606073686)

        print(ids)