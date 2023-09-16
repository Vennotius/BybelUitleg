import json
import subprocess

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


from pylatex import Document, Command, NewPage, NewLine, UnsafeCommand
from pylatex.utils import NoEscape
from pylatex.package import Package

doc = Document()

# Add the utf8x option for inputenc
#doc.preamble.append(Package('inputenc', options='utf8x'))


# Add packages for multicol and fancyhdr
doc.preamble.append(Package('multicol'))
doc.preamble.append(Package('fancyhdr'))

# Set custom header and footer
doc.preamble.append(NoEscape(r'\pagestyle{fancy}'))
doc.preamble.append(NoEscape(r'\fancyhf{}'))  # Clear existing header and footer
doc.preamble.append(NoEscape(r'\fancyhead[C]{\textbf{\rightmark}}'))  # Book name and chapter in header
doc.preamble.append(NoEscape(r'\fancyfoot[C]{\thepage}'))  # Page number in footer

# Title logic as before
doc.preamble.append(Command('title', 'The Bible'))
doc.preamble.append(Command('author', 'Anonymous'))
doc.append(NoEscape(r'\maketitle'))


# from unidecode import unidecode

for book_index, book in enumerate(BYBEL_TEKS):
    if book_index > 0:
        break
    for chapter_index, chapter in enumerate(book):
        doc.append(NoEscape(r'\begin{multicols}{2}'))  # Start 2-column layout
        doc.append(NoEscape(f'\\renewcommand{{\\rightmark}}{{{BYBEL_BOEKNAME[book_index]} Chapter {chapter_index + 1}}}'))  # Set header
        doc.append(NoEscape(f'\\noindent\\fontsize{{24}}{{24}}\\selectfont\\textbf{{{chapter_index}}}\\normalsize'))
        for verse_index, verse in enumerate(chapter):
            if verse_index > 0:
                doc.append(NoEscape(f'\\textsuperscript{{\\textbf{{{verse_index + 1}}}}} {verse}'))
            else:
                doc.append(NoEscape(f' {verse}'))
            doc.append(NewLine())
        doc.append(NoEscape(r'\end{multicols}'))  # End 2-column layout





import traceback

try:
    doc.generate_pdf("bible", clean_tex=True)
except subprocess.CalledProcessError as e:
    print("Error occurred while generating PDF.")
    print("Command:", e.cmd)
    print("Return code:", e.returncode)
    print("Captured Output:", e.output)
    traceback.print_exc()

