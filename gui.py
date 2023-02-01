import flet
import generator
from flet import OutlinedButton, Page, Column, Text, ScrollMode, Container, margin


def main(page: Page):
    page.title = "Anki Deck Generator"
    page.scroll = ScrollMode.AUTO

    output = Text(value=None)
    txt = Text(value="\
Put csv files in the same directory.\n\
File path should looks like this: book(e.g. 語彙,漢字)/chapater/book type(vocab, kanji)\n\
Click Generate to start.")

    def generate_click(e):
        output.value = None
        for msg in generator.generate():
            print(msg)
            output.value = (output.value + "\n" if output.value else "") + msg
            page.update()

    page.add(
        Column([
            txt,
            Container(content=OutlinedButton("Generate",
                                             on_click=generate_click),
                      margin=margin.symmetric(vertical=8)), output
        ]))


flet.app(target=main)