import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os, random
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
        self.cell(30, 10, 'Rectangular Prism Volume Worksheet', align='C')
        self.ln(30)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def generate_prism_image(width, length, height, filename):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    vertices = [
        [0, 0, 0], [width, 0, 0], [width, length, 0], [0, length, 0],
        [0, 0, height], [width, 0, height], [width, length, height], [0, length, height]
    ]
    
    faces = [
        [vertices[j] for j in [0, 1, 5, 4]],
        [vertices[j] for j in [1, 2, 6, 5]],
        [vertices[j] for j in [2, 3, 7, 6]],
        [vertices[j] for j in [3, 0, 4, 7]],
        [vertices[j] for j in [0, 1, 2, 3]],
        [vertices[j] for j in [4, 5, 6, 7]]
    ]
    
    ax.add_collection3d(Poly3DCollection(faces, alpha=0.25, linewidths=1, edgecolors='k'))
    ax.set_xlim([0, max(width, length)])
    ax.set_ylim([0, max(width, length)])
    ax.set_zlim([0, height])

    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    plt.axis('off')
    
    plt.savefig(filename)
    plt.close()

def generate_rectangular_prism_volume_worksheet(num_problems=20, include_answer_key=False):
    pdf = PDF()
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

        width, length, height = random.randint(2, 10), random.randint(2, 10), random.randint(2, 10)
        volume = width * length * height
        surface_area = 2 * (width * length + width * height + length * height)

        problems.append((width, length, height, volume, surface_area))

        filename = f'prism_{i}.png'
        generate_prism_image(width, length, height, filename)
        image_files.append(filename)

        pdf.cell(0, 10, f"{i+1}.", ln=True)
        pdf.image(filename, x=60, y=pdf.get_y(), w=90)
        pdf.ln(50)
        pdf.set_font('helvetica', '', 16)
        pdf.cell(0, 10, f'Width: {width} units', ln=True)
        pdf.cell(0, 10, f'Length: {length} units', ln=True)
        pdf.cell(0, 10, f'Height: {height} units', ln=True)
        pdf.ln(10)

    if include_answer_key:
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 20)
        pdf.set_y(20)
        pdf.cell(0, 10, 'Answer Key', align='C', ln=True)
        pdf.set_font('times', '', 16)
        pdf.ln(5)

        for i, (width, length, height, volume, surface_area) in enumerate(problems, 1):
            pdf.ln(5)
            pdf.cell(0, 10, f'Problem {i}.', ln=True)
            pdf.cell(0, 10, f'Volume = {volume} cubic units', ln=True)
            pdf.cell(0, 10, f'Surface Area = {surface_area} square units', ln=True)
            pdf.ln(10)

    for file in image_files:
        if os.path.exists(file):
            os.remove(file)

    output_dir = os.path.join(os.path.dirname(__file__), '../generated_pdfs')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, 'rectangular_prism_volume.pdf')
    pdf.output(pdf_path)

generate_rectangular_prism_volume_worksheet(include_answer_key=True)