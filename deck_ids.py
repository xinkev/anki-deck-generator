import random
import logging
import shelve


class DeckIds(object):

    def generate(self, key: str) -> int:
        logging.info("Generating id for " + key)
        with shelve.open("deck_ids.db") as ids:
            try:
                id = ids[key]
                logging.info("Found an existing id. Gonna use it.")
                return id
            except KeyError as e:
                logging.info("Generating key")

                id = self.__generate_id()
                while id in list(ids.values()):
                    logging.info(
                        "Key generated but found an existing key. generating again"
                    )
                    id = self.__generate_id()

                ids[key] = id

                return id

    def __generate_id(self) -> int:
        return random.randrange(1 << 30, 1 << 31)

    def __str__(self) -> str:
        return str(list(self.ids.items()))


ids = DeckIds()