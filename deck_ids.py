import random
import shelve

from contextlib import contextmanager
from typing import overload


class DeckIds(object):

    @contextmanager
    def open(self):
        try:
            self.ids = shelve.open("deck_ids.db")
            yield self
        finally:
            self.ids.close()

    def saveKey(self, key: str) -> int:
        try:
            return self.ids[key]
        except:
            id = self.__generate_id()
            try:
                if self.ids[key] == id:
                    self.saveKey(key=key)
            except:
                self.ids[key] = id

    def save(self, key: str, id: int or None = None) -> int:
        if id:
            self.ids[key] = id
            return id
        else:
            return self.saveKey(key)

    def __generate_id(self) -> int:
        return random.randrange(1 << 30, 1 << 31)

    def __str__(self) -> str:
        return str(list(self.ids.items()))


ids = DeckIds()