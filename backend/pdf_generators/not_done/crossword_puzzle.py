'''
import random
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 20)
        self.cell(0, 10, 'Crossword Puzzle', border=True, ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def find_intersections(words):
    intersections = {}
    for i, word1 in enumerate(words):
        for j, word2 in enumerate(words):
            if i != j:
                for k, char1 in enumerate(word1):
                    for l, char2 in enumerate(word2):
                        if char1 == char2:
                            if (i, j) not in intersections:
                                intersections[(i, j)] = []
                            intersections[(i, j)].append((k, l))
    return intersections

def place_words(words):
    grid_size = 15
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    intersections = find_intersections(words)
    word_positions = {}

    def place_word(word, start_row, start_col, direction):
        if direction == 'H':
            for i, char in enumerate(word):
                grid[start_row][start_col + i] = char
        else:
            for i, char in enumerate(word):
                grid[start_row + i][start_col] = char

    def can_place_word(word, start_row, start_col, direction):
        if direction == 'H' and start_col + len(word) > grid_size:
            return False
        if direction == 'V' and start_row + len(word) > grid_size:
            return False
        if direction == 'H':
            return all(grid[start_row][start_col + i] in (' ', word[i]) for i in range(len(word)))
        else:
            return all(grid[start_row + i][start_col] in (' ', word[i]) for i in range(len(word)))

    def place_initial_word(word):
        start_row, start_col = grid_size // 2, grid_size // 2 - len(word) // 2
        place_word(word, start_row, start_col, 'H')
        word_positions[0] = (start_row, start_col, 'H')

    def place_remaining_words():
        for (i, j), positions in intersections.items():
            if i in word_positions and j not in word_positions:
                for k, l in positions:
                    if word_positions[i][2] == 'H':
                        start_row, start_col = word_positions[i][0] - l, word_positions[i][1] + k
                        if can_place_word(words[j], start_row, start_col, 'V'):
                            place_word(words[j], start_row, start_col, 'V')
                            word_positions[j] = (start_row, start_col, 'V')
                            break
                    else:
                        start_row, start_col = word_positions[i][0] + k, word_positions[i][1] - l
                        if can_place_word(words[j], start_row, start_col, 'H'):
                            place_word(words[j], start_row, start_col, 'H')
                            word_positions[j] = (start_row, start_col, 'H')
                            break

    place_initial_word(words[0])
    place_remaining_words()

    return grid

def generate_crossword_pdf(words):
    pdf = PDF('P', 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    
    pdf.set_font('helvetica', 'B', 12)
    grid = place_words(words)
    
    cell_size = 10
    pdf.set_font('helvetica', '', 12)
    for row in grid:
        for cell in row:
            if cell != ' ':
                pdf.cell(cell_size, cell_size, '', 1, 0, 'C')
            else:
                pdf.cell(cell_size, cell_size, '', 0, 0, 'C')
        pdf.ln(cell_size)
    
    pdf.ln(10)
    pdf.set_font('helvetica', 'I', 10)
    pdf.cell(0, 10, 'Word List:', ln=True)
    pdf.set_font('helvetica', '', 12)
    for word in words:
        pdf.cell(0, 10, word, ln=True)
    
    pdf.output('crossword_puzzle.pdf')

def main():
    num_words = int(input("Enter the number of words: "))
    words = [input(f"Enter word {i+1}: ") for i in range(num_words)]
    generate_crossword_pdf(words)

if __name__ == "__main__":
    main()
'''

import json
import random
from fpdf import FPDF
import sys

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 20)
        self.cell(0, 10, 'Crossword Puzzle', border=True, ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def find_intersections(words):
    intersections = {}
    for i, word1 in enumerate(words):
        for j, word2 in enumerate(words):
            if i != j:
                for k, char1 in enumerate(word1):
                    for l, char2 in enumerate(word2):
                        if char1 == char2:
                            if (i, j) not in intersections:
                                intersections[(i, j)] = []
                            intersections[(i, j)].append((k, l))
    return intersections

def place_words(words):
    grid_size = 15
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    intersections = find_intersections(words)
    word_positions = {}

    def place_word(word, start_row, start_col, direction):
        if direction == 'H':
            for i, char in enumerate(word):
                grid[start_row][start_col + i] = char
        else:
            for i, char in enumerate(word):
                grid[start_row + i][start_col] = char

    def can_place_word(word, start_row, start_col, direction):
        if direction == 'H' and start_col + len(word) > grid_size:
            return False
        if direction == 'V' and start_row + len(word) > grid_size:
            return False
        if direction == 'H':
            return all(grid[start_row][start_col + i] in (' ', word[i]) for i in range(len(word)))
        else:
            return all(grid[start_row + i][start_col] in (' ', word[i]) for i in range(len(word)))

    def place_initial_word(word):
        start_row, start_col = grid_size // 2, grid_size // 2 - len(word) // 2
        place_word(word, start_row, start_col, 'H')
        word_positions[0] = (start_row, start_col, 'H')

    def place_remaining_words():
        for (i, j), positions in intersections.items():
            if i in word_positions and j not in word_positions:
                for k, l in positions:
                    if word_positions[i][2] == 'H':
                        start_row, start_col = word_positions[i][0] - l, word_positions[i][1] + k
                        if can_place_word(words[j], start_row, start_col, 'V'):
                            place_word(words[j], start_row, start_col, 'V')
                            word_positions[j] = (start_row, start_col, 'V')
                            break
                    else:
                        start_row, start_col = word_positions[i][0] + k, word_positions[i][1] - l
                        if can_place_word(words[j], start_row, start_col, 'H'):
                            place_word(words[j], start_row, start_col, 'H')
                            word_positions[j] = (start_row, start_col, 'H')
                            break

    place_initial_word(words[0])
    place_remaining_words()

    return grid

def generate_crossword_pdf(words):
    pdf = PDF('P', 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    
    pdf.set_font('helvetica', 'B', 12)
    grid = place_words(words)
    
    cell_size = 10
    pdf.set_font('helvetica', '', 12)
    for row in grid:
        for cell in row:
            if cell != ' ':
                pdf.cell(cell_size, cell_size, '', 1, 0, 'C')
            else:
                pdf.cell(cell_size, cell_size, '', 0, 0, 'C')
        pdf.ln(cell_size)
    
    pdf.ln(10)
    pdf.set_font('helvetica', 'I', 10)
    pdf.cell(0, 10, 'Word List:', ln=True)
    pdf.set_font('helvetica', '', 12)
    for word in words:
        pdf.cell(0, 10, word, ln=True)
    
    pdf.output('generated_pdfs/crossword_puzzle.pdf')

if __name__ == "__main__":
    input_data = json.loads(sys.argv[1])
    generate_crossword_pdf(input_data.get("words", []))
