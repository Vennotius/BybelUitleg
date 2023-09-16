import json

BYBEL_BOEKNAME = [
    "Génesis",
    "Exodus",
    "Levítikus",
    "Númeri",
    "Deuteronomium",
    "Josua",
    "Rigters",
    "Rut",
    "I Samuel",
    "II Samuel",
    "I Konings",
    "II Konings",
    "I Kronieke",
    "II Kronieke",
    "Esra",
    "Nehemía",
    "Ester",
    "Job",
    "Psalm",
    "Spreuke",
    "Prediker",
    "Hooglied",
    "Jesaja",
    "Jeremia",
    "Klaagliedere",
    "Eségiël",
    "Daniël",
    "Hoséa",
    "Joël",
    "Amos",
    "Obadja",
    "Jona",
    "Miga",
    "Nahum",
    "Hábakuk",
    "Sefánja",
    "Haggai",
    "Sagaría",
    "Maleági",
    "Matthéüs",
    "Markus",
    "Lukas",
    "Johannes",
    "Handelinge",
    "Romeine",
    "I Korinthiërs",
    "II Korinthiërs",
    "Galásiërs",
    "Efésiërs",
    "Filippense",
    "Kolossense",
    "I Thessalonicense",
    "II Thessalonicense",
    "I Timótheüs",
    "II Timótheüs",
    "Titus",
    "Filémon",
    "Hebreërs",
    "Jakobus",
    "I Petrus",
    "II Petrus",
    "I Johannes",
    "II Johannes",
    "III Johannes",
    "Judas",
    "Openbaring"
]

BYBEL_TEKS = []

with open('Bybel.json', 'r') as f:
    BYBEL_TEKS = json.loads(f.read())



from pylatex import Document, Section, Command, NewPage, NewLine
from pylatex.utils import NoEscape

doc = Document()
doc.preamble.append(Command('title', 'The Bible'))
doc.preamble.append(Command('author', 'Anonymous'))
doc.append(NoEscape(r'\maketitle'))



def add_bible_text(doc, bible_data):
    for book in bible_data:
        with doc.create(Section(book['book'], numbering=False)):
            for chapter_index, chapter in enumerate(book['chapters'], start=1):
                doc.append(f"Chapter {chapter_index}")
                doc.append(NewLine())
                
                for verse_index, verse in enumerate(chapter, start=1):
                    doc.append(f"{verse_index}. {verse}")
                    doc.append(NewLine())

# Example Bible data
sample_data = [
    {
        'book': 'Genesis',
        'chapters': [
            ['In the beginning God created the heavens and the earth.', 'And the earth was formless and void.'],
            ['Thus the heavens and the earth were completed.', 'And by the seventh day God completed His work.']
        ]
    },
    {
        'book': 'Exodus',
        'chapters': [
            ['Now these are the names of the sons of Israel.', 'Reuben, Simeon, Levi and Judah;'],
            ['Issachar, Zebulun and Benjamin;', 'Dan and Naphtali, Gad and Asher.']
        ]
    }
]

add_bible_text(doc, sample_data)


doc.generate_pdf("bible", clean_tex=True)
