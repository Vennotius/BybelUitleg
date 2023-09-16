import json
import re
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

with open('Bybel_20230916.json', 'r', encoding='utf-8') as f:
    BYBEL_TEKS = json.loads(f.read())

def is_beginning_of_pericope(boek_nommer, hoofstuk_nommer, vers_nommer, vers):
    # Initialize these lists with your specific values
    psalm119Perikope = []
    u = []

    # Method logic
    if vers.startswith(" —"):
        return False

    vers_nommer += 1
    if boek_nommer == 18 and hoofstuk_nommer == 118 and vers_nommer in psalm119Perikope:
        return True

    vers_split = vers.split(' ', 1)
    eerste_woord = vers_split[0].strip(',')
    tweede_woord = vers_split[1].strip(',')

    if all(char.isupper() for char in eerste_woord) and eerste_woord not in u and eerste_woord != "HERE":
        return True

    if all(char.isupper() for char in tweede_woord) and tweede_woord not in u and tweede_woord != "HERE":
        return True

    return False



from pylatex import Document, NewPage, Command, Package, NewLine, UnsafeCommand
from pylatex.utils import NoEscape

doc = Document()

doc.preamble.append(Package('helvet'))
# doc.preamble.append(Package('garamondx'))
doc.preamble.append(Package('mathpazo'))

# Add geometry package with custom margin settings
doc.preamble.append(Package('geometry', options=['a4paper', 'top=3cm', 'bottom=3cm', 'left=2cm', 'right=2cm']))

# Add the utf8x option for inputenc
#doc.preamble.append(Package('inputenc', options='utf8x'))

# Activate the Helvetica (Arial-like) font
# doc.append(NoEscape(r'\renewcommand{\rmdefault}{phv}'))  # Set Helvetica as the default text font
# doc.append(NoEscape(r'\renewcommand{\sfdefault}{phv}'))  # Set Helvetica as the default sans-serif font
# doc.append(NoEscape(r'\renewcommand{\rmdefault}{zgmr}'))  # Set Garamond as the default text font
# Add garamondx package for Garamond font

# Activate the Palatino font
doc.append(NoEscape(r'\renewcommand{\rmdefault}{ppl}'))  # Set Palatino as the default text font


# Add packages for multicol and fancyhdr
doc.preamble.append(Package('multicol'))
doc.preamble.append(Package('fancyhdr'))

# Set custom spacing between columns
doc.append(NoEscape(r'\setlength{\columnsep}{0.8cm}'))

# Redefine what 'normalsize' means
doc.append(NoEscape(r'\renewcommand{\normalsize}{\fontsize{12}{18}\selectfont}'))

# Left align the text and disable hyphenation
doc.append(NoEscape(r'\raggedright'))
doc.append(NoEscape(r'\hyphenpenalty=100'))
doc.append(NoEscape(r'\exhyphenpenalty=100'))

# Set custom header and footer
doc.preamble.append(NoEscape(r'\pagestyle{fancy}'))
doc.preamble.append(NoEscape(r'\fancyhf{}'))  # Clear existing header and footer
doc.preamble.append(NoEscape(r'\fancyhead[C]{\fontsize{18}{20}\selectfont\textbf{\rightmark}}'))  # Larger book name and chapter in header
doc.preamble.append(NoEscape(r'\fancyfoot[C]{\thepage}'))  # Page number in footer

# Title logic as before
# doc.preamble.append(Command('title', 'The Bible'))
# doc.preamble.append(Command('author', 'Anonymous'))
# doc.append(NoEscape(r'\maketitle'))


# from unidecode import unidecode
doc.preamble.append(Package('lettrine'))

for book_index, book in enumerate(BYBEL_TEKS):
    if False and book_index != 0:
        continue

    # New Page and Centered Title for Each Book
    doc.append(NewPage())
    doc.append(NoEscape(f'\\begin{{center}}\\fontsize{{36}}{{36}}\\selectfont\\textbf{{{BYBEL_BOEKNAME[book_index]}}}\\normalsize\\end{{center}}'))
    doc.append(NoEscape(r'\hrule'))  # Add horizontal line under the title
    doc.append(NoEscape(r'\begin{multicols}{2}'))  # Start 2-column layout

    for chapter_index, chapter in enumerate(book):
        doc.append(NoEscape(f'\\renewcommand{{\\rightmark}}{{{BYBEL_BOEKNAME[book_index]} {chapter_index}}}'))  # Set header with chapter number

        for verse_index, verse in enumerate(chapter):
            verse = verse.strip() + ' '
            
            if verse_index > 0 and is_beginning_of_pericope(book_index, chapter_index, verse_index, verse): 
                doc.append(NewLine())
                doc.append(NewLine())

            # doc.append(NoEscape(r'\begin{minipage}{\linewidth}'))
            if verse_index > 0:
                doc.append(NoEscape(f"\\textsuperscript{{\\fontsize{{9}}{{9}}\\selectfont\\textbf{{ {verse_index + 1} }}}}{{}}\\normalsize"))
            else:
                # Reduce vertical space before the lettrine
                doc.append(NoEscape(f'\\vspace*{{-0.5em}}'))
                doc.append(NoEscape(f'\\lettrine[lines=2, lraise=0.1, findent=0.5em, nindent=0em]{{\\textbf{{{chapter_index + 1}}}}}{{}}\\normalsize'))

            doc.append(NoEscape(f'{verse}'))
            # doc.append(NoEscape(r'\end{minipage}'))

            # doc.append(NewLine())

            should_put_verses_on_own_line = book_index == 18 or book_index == 19
            is_end_of_chapter = verse_index == len(chapter) - 1
            if should_put_verses_on_own_line or is_end_of_chapter: 
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

