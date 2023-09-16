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

with open('Bybel.json', 'r', encoding='utf-8') as f:
    BYBEL_TEKS = json.loads(f.read())


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
doc.append(NoEscape(r'\hyphenpenalty=10000'))
doc.append(NoEscape(r'\exhyphenpenalty=10000'))

# Set custom header and footer
doc.preamble.append(NoEscape(r'\pagestyle{fancy}'))
doc.preamble.append(NoEscape(r'\fancyhf{}'))  # Clear existing header and footer
doc.preamble.append(NoEscape(r'\fancyhead[C]{\fontsize{18}{20}\selectfont\textbf{\rightmark}}'))  # Larger book name and chapter in header
doc.preamble.append(NoEscape(r'\fancyfoot[C]{\thepage}'))  # Page number in footer

# Title logic as before
doc.preamble.append(Command('title', 'The Bible'))
doc.preamble.append(Command('author', 'Anonymous'))
doc.append(NoEscape(r'\maketitle'))


# from unidecode import unidecode
doc.preamble.append(Package('lettrine'))

doc.append(NoEscape(r'\begin{multicols}{2}'))  # Start 2-column layout
for book_index, book in enumerate(BYBEL_TEKS):
    if book_index > 1:
        break
    for chapter_index, chapter in enumerate(book):
        doc.append(NoEscape(f'\\renewcommand{{\\rightmark}}{{{BYBEL_BOEKNAME[book_index]} {chapter_index + 1}}}'))  # Set header
        
        # Reduce vertical space before the lettrine
        doc.append(NoEscape(f'\\vspace*{{-0.5em}}'))
        
        # doc.append(NoEscape(f'\\noindent\\fontsize{{16}}{{16}}\\selectfont\\underline{{\\textbf{{{chapter_index}}}}}\\textbf{{ }}\\normalsize'))
        # doc.append(NoEscape(f'\\begin{{center}}\\fontsize{{24}}{{24}}\\selectfont\\textbf{{{chapter_index}}}\\normalsize\\end{{center}}'))
        # doc.append(NoEscape(f'\\noindent\\rule{{\\textwidth}}{{1pt}}\\begin{{center}}\\fontsize{{24}}{{24}}\\selectfont\\textbf{{Chapter {chapter_index}}}\\normalsize\\end{{center}}\\noindent\\rule{{\\textwidth}}{{1pt}}'))
        doc.append(NoEscape(f'\\lettrine[lines=2, lraise=0.1, findent=0.5em, nindent=0em]{{\\textbf{{{chapter_index + 1}}}}}{{}}\\normalsize'))

        for verse_index, verse in enumerate(chapter):
            verse = verse.strip()
            if verse_index > 0:
               doc.append(NoEscape(f"\\textsuperscript{{\\fontsize{{9}}{{9}}\\selectfont\\textbf{{ {verse_index + 1} }}}}{verse}"))
            else:
                doc.append(NoEscape(f'{verse}'))
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

