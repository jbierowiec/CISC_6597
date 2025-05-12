import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os, random
import numpy as np
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        script_dir = os.path.dirname(__file__)  
        image_path = os.path.join(script_dir, 'math.png')

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        self.image(image_path, 10, 8, 25)
        self.set_font('helvetica', 'B', 20)
        self.cell(80)
        self.cell(30, 10, 'Sphere Volume Worksheet', align='C')
        self.ln(30)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def generate_sphere_image(radius, filename):
    fig = plt.figure(figsize=(radius, radius))
    ax = fig.add_subplot(111, projection='3d')
    u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
    x = radius * np.cos(u) * np.sin(v)
    y = radius * np.sin(u) * np.sin(v)
    z = radius * np.cos(v)
    ax.plot_surface(x, y, z, color='lightblue', alpha=0.6)
    ax.set_xlim([-radius, radius])
    ax.set_ylim([-radius, radius])
    ax.set_zlim([-radius, radius])
    plt.axis('off')
    plt.savefig(filename)
    plt.close()

def generate_sphere_volume_worksheet(num_problems=20, include_answer_key=False):
    pdf = PDF('P', 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('times', '', 16)
    pdf.ln(10)

    problems = []
    image_files = []

    for i in range(num_problems):
        if i % 2 == 0 and i > 0:
            pdf.add_page()
            pdf.ln(10)

        radius = random.randint(2, 10)
        surface_area = 4 * np.pi * radius**2
        volume = (4/3) * np.pi * radius**3

        problems.append((radius, volume, surface_area))

        filename = f'sphere_{i}.png'
        generate_sphere_image(radius, filename)
        image_files.append(filename)

        pdf.cell(0, 10, f"{i+1}.", ln=True)
        pdf.image(filename, x=60, y=pdf.get_y(), w=90)
        pdf.ln(50)
        pdf.set_font('helvetica', '', 16)
        pdf.cell(0, 10, f'Radius: {radius} units', ln=True)
        pdf.ln(10)

    if include_answer_key:
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 20)
        pdf.set_y(20)
        pdf.cell(0, 10, 'Answer Key', align='C', ln=True)
        pdf.set_font('times', '', 16)
        pdf.ln(5)

        for i, (radius, volume, surface_area) in enumerate(problems, 1):
            pdf.ln(5)
            pdf.cell(0, 10, f'Problem {i}.', ln=True)
            pdf.cell(0, 10, f'Volume = {volume:.2f} cubic units', ln=True)
            pdf.cell(0, 10, f'Surface Area = {surface_area:.2f} square units', ln=True)
            pdf.ln(10)

    for file in image_files:
        if os.path.exists(file):
            os.remove(file)

    output_dir = os.path.join(os.path.dirname(__file__), '../generated_pdfs')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, 'sphere_volume.pdf')
    pdf.output(pdf_path)

generate_sphere_volume_worksheet(include_answer_key=True)