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

'''
def generate_isosceles_triangle():
    base = random.randint(4, 20)
    equal_side = random.randint(base, base + 15)
    height = np.sqrt(equal_side**2 - (base/2)**2)
    return base, equal_side, round(height, 2)
'''

def generate_isosceles_triangle():
    vertex_angle = random.randint(20, 100)  # Random vertex angle
    base_angle = (180 - vertex_angle) / 2  # Equal base angles
    return round(vertex_angle, 2), round(base_angle, 2)

'''
def generate_triangle_image(base, equal_side, height, missing, filename):
    fig, ax = plt.subplots()
    ax.set_xlim(0, base + 2)
    ax.set_ylim(0, equal_side + 2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    ax.plot([0, base, base/2, 0], [0, 0, height, 0], 'k-', linewidth=2)
    
    labels = {'base': f'{base} cm', 'side': f'{equal_side} cm', 'height': f'{height:.2f} cm'}
    labels[missing] = 'x'
    
    ax.text(base/2, -1, labels['base'], fontsize=18, ha='center')
    ax.text(-1, equal_side/2, labels['side'], fontsize=18, va='center')
    ax.text(base/2, height/2, labels['height'], fontsize=18, ha='center', va='bottom')
    
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()
'''

def generate_triangle_image(vertex_angle, base_angle, given, filename):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    ax.plot([2, 8, 5, 2], [2, 2, 8, 2], 'k-', linewidth=2)
    
    labels = {'vertex': f'{vertex_angle}°', 'base': 'x°', 'base2': 'y°'}
    labels[given] = f'{round(vertex_angle if given == "vertex" else base_angle, 2)}°'
    
    ax.text(5, 1, labels['base'], fontsize=18, ha='center')
    ax.text(1.5, 5, labels['base2'], fontsize=18, va='center')
    ax.text(5, 7, labels['vertex'], fontsize=18, ha='center', va='bottom')
    
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()

'''
def generate_unique_triangles(num_questions):
    triangles = []
    for _ in range(num_questions):
        base, equal_side, height = generate_isosceles_triangle()
        missing = random.choice(['base', 'side', 'height'])
        triangles.append((base, equal_side, height, missing))
    return triangles
'''

def generate_unique_triangles(num_questions):
    triangles = []
    for _ in range(num_questions):
        vertex_angle, base_angle = generate_isosceles_triangle()
        given = random.choice(['vertex', 'base'])
        triangles.append((vertex_angle, base_angle, given))
    return triangles

def generate_triangle_worksheet(num_problems=20, include_answer_key=False):
    pdf = FPDF('P', 'mm', 'Letter')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('times', '', 16)
    pdf.ln(10)

    triangles = generate_unique_triangles(num_problems)
    image_files = []

    '''
    for i, (base, equal_side, height, missing) in enumerate(triangles):
        if i % 2 == 0 and i > 0:
            pdf.add_page()
            pdf.ln(10)
    '''
    for i, (vertex_angle, base_angle, given) in enumerate(triangles):
        if i % 2 == 0 and i > 0:
            pdf.add_page()
            pdf.ln(10)
        
        filename = f"triangle_{i}.png"
        #generate_triangle_image(base, equal_side, height, missing, filename)
        generate_triangle_image(vertex_angle, base_angle, given, filename)
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
        
        '''
        for i, (base, equal_side, height, missing) in enumerate(triangles):
            pdf.ln(5)
            answer = {'base': base, 'side': equal_side, 'height': height}[missing]
            pdf.cell(0, 10, f"Triangle {i+1}: x = {answer} cm", ln=True)
        '''
        for i, (vertex_angle, base_angle, given) in enumerate(triangles):
            pdf.ln(5)
            if given == 'vertex':
                x, y = base_angle, base_angle
            else:
                x, y = vertex_angle, base_angle
            pdf.cell(0, 10, f"Triangle {i+1}: x = {x}°, y = {y}°", ln=True)
    
    for file in image_files:
        if os.path.exists(file):
            os.remove(file)
    
    output_dir = os.path.join(os.path.dirname(__file__), '../generated_pdfs')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, 'isosceles_triangles.pdf')
    pdf.output(pdf_path)

generate_triangle_worksheet(num_problems=20, include_answer_key=True)
