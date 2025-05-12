import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, random
import numpy as np
import sympy as sp
from fpdf import FPDF
from io import BytesIO

class PDF(FPDF):
    def header(self):
        script_dir = os.path.dirname(__file__)  
        image_path = os.path.join(script_dir, 'math.png')

        if os.path.exists(image_path):
            self.image(image_path, 10, 8, 25)
        
        self.set_font('helvetica', 'B', 20)
        self.cell(80)
        self.cell(30, 10, 'Right Triangle Worksheet', align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def generate_pythagorean_triple():
    triples = [(3, 4, 5), (5, 12, 13), (7, 24, 25), (8, 15, 17), (9, 40, 41), (11, 60, 61),
               (12, 35, 37), (13, 84, 85), (16, 63, 65), (20, 21, 29)]
    k = random.randint(1, 5)  # Scaling factor
    a, b, c = random.choice(triples)
    return k * a, k * b, k * c

def generate_triangle_image(a, b, c, missing, filename):
    fig, ax = plt.subplots()
    ax.set_xlim(0, max(a, b) + 2)
    ax.set_ylim(0, max(a, b) + 2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    ax.plot([0, 0, a, 0], [0, b, 0, 0], 'k-', linewidth=2)
    
    labels = { 'a': f'{a} cm', 'b': f'{b} cm', 'c': f'{c:.2f} cm' }
    labels[missing] = 'x'
    
    ax.text(a/2, -0.5, labels['a'], fontsize=18, ha='center')
    ax.text(-0.5, b/2, labels['b'], fontsize=18, va='center')
    ax.text(a/2, b/2, labels['c'], fontsize=18, ha='center', va='bottom')
    
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()

def generate_unique_triangles(num_questions):
    triangles = []
    for _ in range(num_questions):
        a, b, c = generate_pythagorean_triple()
        missing = random.choice(['a', 'b', 'c'])
        triangles.append((a, b, c, missing))
    return triangles

def generate_triangle_worksheet(num_problems=20, include_answer_key=False):
    pdf = PDF('P', 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('times', '', 16)
    pdf.ln(10)

    triangles = generate_unique_triangles(num_problems)
    image_files = []

    for i, (a, b, c, missing) in enumerate(triangles):
        if i % 2 == 0 and i > 0:
            pdf.add_page()
            pdf.ln(10)
        
        filename = f"triangle_{i}.png"
        generate_triangle_image(a, b, c, missing, filename)
        image_files.append(filename)
        
        pdf.cell(0, 10, f"{i+1}.", ln=True)
        pdf.image(filename, x=80, w=50)
        pdf.ln(5)
        pdf.cell(0, 10, "Find the missing value x:", ln=True)
        pdf.ln(5)

    if include_answer_key:
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 20)
        pdf.set_y(20)
        pdf.cell(0, 10, 'Answer Key', align='C', ln=True)
        pdf.set_font('times', '', 16)
        pdf.ln(5)
        
        for i, (a, b, c, missing) in enumerate(triangles):
            pdf.ln(5)
            answer = {'a': a, 'b': b, 'c': c}[missing]
            pdf.cell(0, 10, f"Triangle {i+1}: x = {answer} cm", ln=True)
    
    for file in image_files:
        if os.path.exists(file):
            os.remove(file)
    
    output_dir = os.path.join(os.path.dirname(__file__), '../generated_pdfs')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, 'triangles.pdf')
    pdf.output(pdf_path)

generate_triangle_worksheet(num_problems=20, include_answer_key=True)