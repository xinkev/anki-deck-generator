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
    print ("Finding CSV files...")
    csv_files = find_file_paths("./**/*.csv")
    generate_messages(csv_files)
    anki_package: genanki.Package = None

    decks = generate_decks(csv_files)

    if decks:
        print("Creating Anki package...")
        anki_package = genanki.Package(decks)

    if anki_package:
        print ("Finding media files...")
        jpg_files = find_file_paths("./**/*.jpg")
        generate_messages(jpg_files)

        if jpg_files or len(jpg_files)>0:
            print ("Adding JPG files to the package...")
            anki_package.media_files = jpg_files

        anki_package.write_to_file("so-matome.apkg")
        print ("Complete...")
    else:
        print ("Hmm... I think something went wrong.")


def generate_messages(filepaths: list[str]) -> str:
    if filepaths and len(filepaths) > 0:
        return f"Found {len(filepaths)} files.\n{filepaths}"
    else:
        return "No files found. Please make sure you have files in the same directory."
        


def find_file_paths(pathname: str) -> list[str]:
    return glob.glob(pathname, recursive=True)


def generate_decks(
        paths: list[str]) -> Generator[str, None, list[genanki.Deck]]:
    decks = []
    for path in paths:
        with open(path, "r") as file:
            csv_reader = csv.DictReader(file, delimiter="|")
            book, chapter, type_with_ext = Path(file.name).parts
            type = type_with_ext.removesuffix(".csv")

            if type == "vocab":
                print (f"Generating vocab decks for {book}, {chapter}...")
                decks += generate_vocab_decks(book, chapter, csv_reader)
            else:
                decks += generate_kanji_deck(book, chapter, csv_reader)
                print (f"Generating kanji deck of {book}, {chapter}")
    return decks


def generate_vocab_decks(book: str, chapter: str,
                         csv_reader: csv.DictReader) -> list[genanki.Deck]:
    decks = []

    jp_deck_name = f"{book}::{chapter}::jp"
    en_deck_name = f"{book}::{chapter}::en"

    jp_deck_id = ids.generate(jp_deck_name)
    en_deck_id = ids.generate(en_deck_name)

    jp_deck = genanki.Deck(deck_id=jp_deck_id, name=jp_deck_name)
    en_deck = genanki.Deck(deck_id=en_deck_id, name=en_deck_name)
    decks += [jp_deck] + [en_deck]

    for row in csv_reader:
        (japanese, meaning, example) = row.values()
        note = genanki.Note(model=models.GOI_EN,
                            fields=[
                                meaning,
                                generate_furigana(japanese),
                                generate_furigana(__get_str(example))
                            ])
        en_deck.add_note(note)
        note = genanki.Note(model=models.GOI_JP,
                            fields=[
                                generate_furigana(japanese), meaning,
                                generate_furigana(__get_str(example))
                            ])
        jp_deck.add_note(note)

    return decks


def generate_kanji_deck(book: str, chapter: str,
                        csv_reader: csv.DictReader) -> list[genanki.Deck]:
    decks = []
    deck_name = f"{book}::{chapter}::kanji"
    deck_id = ids.generate(deck_name)
    deck = genanki.Deck(deck_id=deck_id, name=deck_name)
    decks.append(deck)

    for row in csv_reader:
        (ji, on, kun, example) = row.values()
        note = genanki.Note(model=models.KANJI,
                            fields=[
                                ji,
                                __get_str(on),
                                __get_str(kun),
                                generate_furigana(__get_str(example))
                            ])
        print("adding note to -> " + deck_name + "::" + str(deck_id))
        deck.add_note(note)

    return decks


def generate_furigana(jp: str) -> str:
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
    return value if value else " "


if __name__ == '__main__':
    generate()
