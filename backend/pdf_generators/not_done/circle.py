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

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        self.image(image_path, 10, 8, 25)
        self.set_font('helvetica', 'B', 20)
        self.cell(80)
        self.cell(30, 10, 'Basic Circle Worksheet', align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def generate_circle_image(radius, filename):
    fig, ax = plt.subplots(figsize=(max(5, radius / 10), max(5, radius / 10)))
    circle = plt.Circle((0, 0), radius, fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(circle)
    ax.plot([0, radius], [0, 0], color='black', linewidth=3)
    ax.text(0, radius * 0.2, f"{radius} cm", fontsize=15, ha='left', va='bottom', fontweight='bold')
    ax.set_xlim(-radius-2, radius+2)
    ax.set_ylim(-radius-2, radius+2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect(1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()

def generate_unique_radii(num_questions, min_radius=1, max_radius=30):
    return random.sample(range(min_radius, max_radius + 1), num_questions)

def generate_circle_worksheet(num_problems=20, include_answer_key=False):
    pdf = PDF('P', 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('times', '', 16)
    pdf.ln(10)

    circles = generate_unique_radii(num_problems, 1, 30)

    image_files = []

    for i, radius in enumerate(circles):
        if i % 2 == 0 and i > 0:
            pdf.add_page()
            pdf.ln(10)

        filename = f"circle_{i}.png"
        generate_circle_image(radius, filename)
        image_files.append(filename)

        pdf.cell(0, 10, f"{i+1}.", ln=True)
        pdf.image(filename, x=80, w=50)
        pdf.ln(5)
        pdf.cell(0, 10, "Calculate the following:", ln=True)
        pdf.cell(0, 10, "1. Diameter = __________ cm", ln=True)
        pdf.cell(0, 10, "2. Circumference = __________ cm", ln=True)
        pdf.cell(0, 10, "3. Area = __________ cm²", ln=True)
        pdf.ln(5)

    if include_answer_key:
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 20)
        pdf.set_y(20)
        pdf.cell(0, 10, 'Answer Key', align='C', ln=True)
        pdf.set_font('times', '', 16)
        pdf.ln(5)

        for i, radius in enumerate(circles):
            pdf.ln(5)
            diameter = 2 * radius
            circumference = 2 * np.pi * radius
            area = np.pi * (radius ** 2)
            pdf.cell(0, 10, f"Circle {i+1}. ", ln=True)
            pdf.cell(0, 10, f"Diameter = {diameter:.2f} cm", ln=True)
            pdf.cell(0, 10, f"Circumference = {circumference:.2f} cm", ln=True)
            pdf.cell(0, 10, f"Area = {area:.2f} cm²", ln=True)      

    for file in image_files:
        if os.path.exists(file):
            os.remove(file)

    output_dir = os.path.join(os.path.dirname(__file__), '../generated_pdfs')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, 'circles.pdf')
    pdf.output(pdf_path)

generate_circle_worksheet(num_problems=20, include_answer_key=True)