import genanki

__jp_style = '''
.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}

#front {
	font-size: 40px;
}
'''

__en_style = '''
.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}

#back {
	font-size: 40px;
}
'''

__kanji_style = __jp_style

GOI_JP = genanki.Model(
    model_id=1091735104,
    name="goi-jp",
    fields=[{
        "name": "Front"
    }, {
        "name": "Back"
    }, {
        "name": "Example"
    }],
    templates=[{
        "name":
        "Card 1",
        "qfmt":
        '<span id="front">{{kanji:Front}}</span>',
        "afmt":
        '<span id="front">{{furigana:Front}}</span><hr id=answer>{{furigana:Back}}<br><br>{{furigana:Example}}'
    }],
    css=__jp_style)
GOI_EN = genanki.Model(
    model_id=1091735103,
    name="goi-en",
    fields=[{
        "name": "Front"
    }, {
        "name": "Back"
    }, {
        "name": "Example"
    }],
    templates=[{
        "name":
        "Card 1",
        "qfmt":
        '<span id="front">{{kanji:Front}}</span>',
        "afmt":
        '<span id="front">{{furigana:Front}}</span><hr id=answer>{{furigana:Back}}<br><br>{{furigana:Example}}'
    }],
    css=__en_style)

KANJI = genanki.Model(
    model_id=1091735102,
    name="kanji",
    fields=[{
        "name": "Ji"
    }, {
        "name": "Onyomi"
    }, {
        "name": "Kunyomi"
    }, {
        "name": "Example"
    }],
    templates=[{
        "name":
        "Card 1",
        "qfmt":
        '<span id="front">{{kanji:Ji}}</span>',
        "afmt":
        '<span id="front">{{furigana:Ji}}</span><hr id=answer>{{Onyomi}}<br/>{{Kunyomi}}<br/>{{furigana:Example}}'
    }],
    css=__kanji_style)
