#!/usr/bin/env python3

from typing import IO, Generator, Literal
import models
import genanki
import csv
import glob

import pykakasi

from pathlib import Path
from deck_ids import ids

__kks = pykakasi.kakasi()
# file path format: book(語彙,漢字)/chapater/type(jp, en, kanji)


def generate() -> Generator[str, None, None]:
    __file_paths = glob.glob("./**/*.csv", recursive=True)

    if __file_paths and len(__file_paths) > 0:
        yield (f"Found {len(__file_paths)} files.\n{__file_paths}")
        for msg in __generate_decks(__file_paths):
            yield msg
    else:
        yield (
            "No csv files found. Please make sure you have csv files in the same directory."
        )


def __generate_decks(paths: list[str]) -> Generator[str, None, None]:
    decks = []
    for path in paths:
        with open(path, "r") as file:
            csv_reader = csv.DictReader(file, delimiter="|")
            book, chapter, type_with_ext = Path(file.name).parts
            type = type_with_ext.removesuffix(".csv")

            if type == "vocab":
                yield (f"Generating vocab decks for {book}, {chapter}...")
                decks += __generate_vocab_decks(book, chapter, csv_reader)
            else:
                decks += __generate_kanji_deck(book, chapter, csv_reader)
                yield (f"Generating kanji deck of {book}, {chapter}")

    anki_package = genanki.Package(decks)
    anki_package.write_to_file("so-matome.apkg")
    yield ("Complete...")


def __generate_vocab_decks(book: str, chapter: str,
                           csv_reader: csv.DictReader) -> list[genanki.Deck]:
    decks = []
    with ids.open():
        jp_deck_name = f"{book}::{chapter}::jp"
        en_deck_name = f"{book}::{chapter}::en"

        jp_deck_id = ids.saveKey(jp_deck_name)
        en_deck_id = ids.saveKey(en_deck_name)

        jp_deck = genanki.Deck(deck_id=jp_deck_id, name=jp_deck_name)
        en_deck = genanki.Deck(deck_id=en_deck_id, name=en_deck_name)
        decks += [jp_deck] + [en_deck]

        for row in csv_reader:
            (japanese, meaning, example) = row.values()
            note = genanki.Note(model=models.GOI_EN,
                                fields=[
                                    meaning,
                                    __generate_furigana(japanese),
                                    __generate_furigana(__get_str(example))
                                ])
            en_deck.add_note(note)
            note = genanki.Note(model=models.GOI_JP,
                                fields=[
                                    __generate_furigana(japanese), meaning,
                                    __generate_furigana(__get_str(example))
                                ])
            jp_deck.add_note(note)

    return decks


def __generate_kanji_deck(book: str, chapter: str,
                          csv_reader: csv.DictReader) -> list[genanki.Deck]:
    decks = []
    with ids.open():
        deck_name = f"{book}::{chapter}::kanji"
        deck_id = ids.save(deck_name)
        deck = genanki.Deck(deck_id=deck_id, name=deck_name)
        decks.append(deck)

        for row in csv_reader:
            (ji, on, kun, example) = row.values()
            note = genanki.Note(model=models.KANJI,
                                fields=[
                                    ji,
                                    __get_str(on),
                                    __get_str(kun),
                                    __generate_furigana(__get_str(example))
                                ])
            deck.add_note(note)

    return decks


def __generate_furigana(jp: str) -> str:
    words = __kks.convert(jp)
    new_str = ""
    for (index, word) in enumerate(words):
        if word["orig"] == word["hira"]:
            new_str += word["orig"]
        else:
            formatted_word = f"{word['orig']}[{word['hira']}]"
            if index > 0:
                formatted_word = " " + formatted_word
            new_str += formatted_word
    return new_str


def __get_str(value) -> str:
    return value if value else ""


if __name__ == '__main__':
    for string in generate():
        print(string)
