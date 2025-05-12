import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, random
import numpy as np
from fpdf import FPDF

def generate_isosceles_triangle():
    vertex_angle = random.randint(20, 100)  # Random vertex angle
    base_angle = (180 - vertex_angle) / 2  # Equal base angles
    return round(vertex_angle, 2), round(base_angle, 2)

def generate_triangle_image(vertex_angle, base_angle, given, filename):
    height = 10  # Set a fixed height for visualization
    base_width = 2 * height * np.tan(np.radians(base_angle))  # Proportional base width
    
    fig, ax = plt.subplots()
    ax.set_xlim(-base_width / 2 - 1, base_width / 2 + 1)
    ax.set_ylim(0, height + 2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    # Triangle vertices
    left_base = (-base_width / 2, 0)
    right_base = (base_width / 2, 0)
    top_vertex = (0, height)
    
    ax.plot([left_base[0], right_base[0], top_vertex[0], left_base[0]],
            [left_base[1], right_base[1], top_vertex[1], left_base[1]], 'k-', linewidth=2)
    
    labels = {'vertex': f'{vertex_angle}°', 'base': 'x°', 'base2': 'y°'}
    labels[given] = f'{round(vertex_angle if given == "vertex" else base_angle, 2)}°'
    
    ax.text(left_base[0] - 1, 1, labels['base'], fontsize=18, ha='center')
    ax.text(right_base[0] + 1, 1, labels['base2'], fontsize=18, ha='center')
    ax.text(top_vertex[0], top_vertex[1] + 0.5, labels['vertex'], fontsize=18, ha='center', va='bottom')
    
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()

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

    for i, (vertex_angle, base_angle, given) in enumerate(triangles):
        if i % 2 == 0 and i > 0:
            pdf.add_page()
            pdf.ln(10)
        
        filename = f"triangle_{i}.png"
        generate_triangle_image(vertex_angle, base_angle, given, filename)
        image_files.append(filename)
        
        pdf.cell(0, 10, f"{i+1}.", ln=True)
        pdf.image(filename, x=80, w=50)
        pdf.ln(5)
        pdf.cell(0, 10, "Find the missing angles x and y:", ln=True)
        pdf.ln(5)

    if include_answer_key:
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 20)
        pdf.set_y(20)
        pdf.cell(0, 10, 'Answer Key', align='C', ln=True)
        pdf.set_font('times', '', 16)
        pdf.ln(5)
        
        for i, (vertex_angle, base_angle, given) in enumerate(triangles):
            pdf.ln(5)
            x, y = base_angle, base_angle if given == 'vertex' else (vertex_angle, base_angle)
            pdf.cell(0, 10, f"Triangle {i+1}: x = {x}°, y = {y}°", ln=True)
    
    for file in image_files:
        if os.path.exists(file):
            os.remove(file)
    
    output_dir = os.path.join(os.path.dirname(__file__), '../generated_pdfs')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, 'isosceles_triangles_angles.pdf')
    pdf.output(pdf_path)

generate_triangle_worksheet(num_problems=20, include_answer_key=True)
