#!/usr/bin/env python3

from typing import IO
import models
import genanki
import csv
import glob

import pykakasi

from pathlib import Path

__file_paths = glob.glob("./**/*.csv", recursive=True)
__kks = pykakasi.kakasi()
# file path format: book(語彙,漢字)/chapater/type(jp, en, kanji)


def generate():
    print(f"Found {len(__file_paths)} files.\n{__file_paths}")

    decks = []
    for file_path in __file_paths:
        with open(file_path, "r") as file:
            csv_reader = csv.reader(file, delimiter="|")
            book, chapter, type_with_ext = Path(file.name).parts
            type = type_with_ext.removesuffix(".csv")

            if type == "vocab":
                decks += __generate_vocab_decks(book, chapter, csv_reader)
            else:
                decks.append(__generate_kanji_deck(book, chapter, csv_reader))
    anki_package = genanki.Package(decks)
    anki_package.write_to_file("so-matome.apkg")
    print("Complete...")


def __generate_vocab_decks(book: str, chapter: str,
                           csv_reader: list[str]) -> list[genanki.Deck]:
    decks = []
    jp_deck_id, en_deck_id = next(csv_reader)

    jp_deck = genanki.Deck(deck_id=int(jp_deck_id),
                           name=f"{book}::{chapter}::jp")
    en_deck = genanki.Deck(deck_id=int(en_deck_id),
                           name=f"{book}::{chapter}::en")
    decks += [jp_deck] + [en_deck]

    for line in csv_reader:
        (japanese, meaning, example) = line
        note = genanki.Note(model=models.GOI_EN,
                            fields=[
                                meaning,
                                __generate_furigana(japanese),
                                __generate_furigana(example)
                            ])
        en_deck.add_note(note)
        note = genanki.Note(model=models.GOI_JP,
                            fields=[
                                __generate_furigana(japanese), meaning,
                                __generate_furigana(example)
                            ])
        jp_deck.add_note(note)

    return decks


def __generate_kanji_deck(book: str, chapter: str,
                          csv_reader: list[str]) -> genanki.Deck:
    deck = genanki.Deck(deck_id=int(next(csv_reader)[0]),
                        name=f"{book}::{chapter}::kanji")

    for line in csv_reader:
        (ji, on, kun) = line
        note = genanki.Note(model=models.KANJI, fields=[ji, on, kun])
        deck.add_note(note)
    return deck


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


if __name__ == '__main__':
    generate()
