'''
import random
import string
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.image('math.png', 10, 8, 25)
        self.set_font('helvetica', 'B', 20)
        self.cell(80)
        self.cell(30, 10, 'Word Search', border=True, ln=True, align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def get_user_input():
    num_words = int(input("Enter the number of words: "))
    words = [input(f"Enter word {i+1}: ").upper() for i in range(num_words)]
    x = int(input("Enter the grid width (x): "))
    y = int(input("Enter the grid height (y): "))
    return words, x, y

def create_grid(words, x, y):
    grid = [['' for _ in range(x)] for _ in range(y)]
    directions = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1)]
    
    def can_place(word, row, col, dir_x, dir_y):
        for i in range(len(word)):
            new_row = row + dir_y * i
            new_col = col + dir_x * i
            if new_row < 0 or new_row >= y or new_col < 0 or new_col >= x or (grid[new_row][new_col] != '' and grid[new_row][new_col] != word[i]):
                return False
        return True
    
    def place_word(word):
        placed = False
        while not placed:
            dir_x, dir_y = random.choice(directions)
            start_row = random.randint(0, y - 1)
            start_col = random.randint(0, x - 1)
            if can_place(word, start_row, start_col, dir_x, dir_y):
                for i in range(len(word)):
                    grid[start_row + dir_y * i][start_col + dir_x * i] = word[i]
                placed = True
    
    for word in words:
        place_word(word)
    
    for row in range(y):
        for col in range(x):
            if grid[row][col] == '':
                grid[row][col] = random.choice(string.ascii_uppercase)
    
    return grid

def create_pdf(grid, words):
    pdf = PDF('P', 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('times', '', 12)
    
    cell_width = 200 / len(grid[0])
    cell_height = 10
    
    for row in grid:
        for letter in row:
            pdf.cell(cell_width, cell_height, letter, border=1, align='C')
        pdf.ln(cell_height)
    
    pdf.ln(10)  # Add some space between the grid and the words list
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, 'Words to Find:', ln=True)
    pdf.set_font('times', '', 12)
    
    for word in words:
        pdf.cell(0, 10, word, ln=True)
    
    pdf.output('word_search.pdf')

def main():
    words, x, y = get_user_input()
    grid = create_grid(words, x, y)
    create_pdf(grid, words)

if __name__ == "__main__":
    main()
'''

'''
import json
import random
import string
from fpdf import FPDF
import sys

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 20)
        self.cell(0, 10, 'Word Search', border=True, ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def create_grid(words, x, y):
    grid = [['' for _ in range(x)] for _ in range(y)]
    directions = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1)]
    
    def can_place(word, row, col, dir_x, dir_y):
        for i in range(len(word)):
            new_row = row + dir_y * i
            new_col = col + dir_x * i
            if new_row < 0 or new_row >= y or new_col < 0 or new_col >= x or (grid[new_row][new_col] != '' and grid[new_row][new_col] != word[i]):
                return False
        return True
    
    def place_word(word):
        placed = False
        while not placed:
            dir_x, dir_y = random.choice(directions)
            start_row = random.randint(0, y - 1)
            start_col = random.randint(0, x - 1)
            if can_place(word, start_row, start_col, dir_x, dir_y):
                for i in range(len(word)):
                    grid[start_row + dir_y * i][start_col + dir_x * i] = word[i]
                placed = True
    
    for word in words:
        place_word(word)
    
    for row in range(y):
        for col in range(x):
            if grid[row][col] == '':
                grid[row][col] = random.choice(string.ascii_uppercase)
    
    return grid

def create_pdf(grid, words):
    pdf = PDF('P', 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    
    cell_width = 200 / len(grid[0])
    cell_height = 10
    
    for row in grid:
        for letter in row:
            pdf.cell(cell_width, cell_height, letter, border=1, align='C')
        pdf.ln(cell_height)
    
    pdf.ln(10)
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, 'Words to Find:', ln=True)
    pdf.set_font('times', '', 12)
    
    for word in words:
        pdf.cell(0, 10, word, ln=True)
    
    pdf.output('generated_pdfs/word_search.pdf')

if __name__ == "__main__":
    input_data = json.loads(sys.argv[1])
    words = input_data.get("words", [])
    x = input_data.get("width", 10)
    y = input_data.get("height", 10)
    grid = create_grid(words, x, y)
    create_pdf(grid, words)
'''

























import random
import string
from fpdf import FPDF
import json
import sys


class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 20)
        self.cell(0, 10, 'Word Search', border=True, ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')


def create_grid(words, x, y):
    grid = [['' for _ in range(x)] for _ in range(y)]
    directions = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1)]

    def can_place(word, row, col, dir_x, dir_y):
        """Check if the word can be placed starting at (row, col) in the specified direction."""
        for i in range(len(word)):
            new_row = row + dir_y * i
            new_col = col + dir_x * i
            if new_row < 0 or new_row >= y or new_col < 0 or new_col >= x or (
                grid[new_row][new_col] != '' and grid[new_row][new_col] != word[i]
            ):
                return False
        return True

    def place_word(word):
        """Attempt to place the word in the grid."""
        placed = False
        while not placed:
            dir_x, dir_y = random.choice(directions)
            start_row = random.randint(0, y - 1)
            start_col = random.randint(0, x - 1)
            if can_place(word, start_row, start_col, dir_x, dir_y):
                for i in range(len(word)):
                    new_row = start_row + dir_y * i
                    new_col = start_col + dir_x * i
                    grid[new_row][new_col] = word[i]
                placed = True

    for word in words:
        place_word(word)

    # Fill empty cells with random letters
    for row in range(y):
        for col in range(x):
            if grid[row][col] == '':
                grid[row][col] = random.choice(string.ascii_uppercase)

    return grid


def create_pdf(grid, words):
    """Generate a PDF with the word search grid and the word list."""
    pdf = PDF('P', 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.add_page()

    cell_width = 200 / len(grid[0])
    cell_height = 10

    # Create the grid in the PDF
    pdf.set_font('helvetica', '', 12)
    for row in grid:
        for letter in row:
            pdf.cell(cell_width, cell_height, letter, border=1, align='C')
        pdf.ln(cell_height)

    # Add the word list to the PDF
    pdf.ln(10)
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, 'Words to Find:', ln=True)
    pdf.set_font('times', '', 12)
    for word in words:
        pdf.cell(0, 10, word, ln=True)  # Ensure each word is treated as a single string

    pdf.output('generated_pdfs/word_search.pdf')



if __name__ == "__main__":
    input_data = json.loads(sys.argv[1])
    words = input_data.get("words", [])
    x = input_data.get("width", 15)
    y = input_data.get("height", 15)

    grid = create_grid(words, x, y)
    create_pdf(grid, words)
