import matplotlib
matplotlib.use('Agg')
import random
from fpdf import FPDF
import matplotlib.pyplot as plt
import os

class PDF(FPDF):
    def header(self):
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '../math.png')

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        self.image(image_path, 10, 8, 25)
        self.set_font('helvetica', 'B', 20)
        self.cell(80)
        self.cell(30, 10, 'Fraction Division Worksheet', align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def generate_fraction_problems(num_problems, min_value=1, max_value=20):
    from fractions import Fraction

    problems = []
    solutions = []

    for _ in range(num_problems):
        numerator1 = random.randint(min_value, max_value)
        denominator1 = random.randint(min_value, max_value)
        numerator2 = random.randint(min_value, max_value)
        denominator2 = random.randint(min_value, max_value)
        
        problem = rf"\frac{{{numerator1}}}{{{denominator1}}} ÷ \frac{{{numerator2}}}{{{denominator2}}}"
        problems.append(problem)
        
        fraction1 = Fraction(numerator1, denominator1)
        fraction2 = Fraction(numerator2, denominator2)
        solution = fraction1 / fraction2
        solutions.append(solution)

    return problems, solutions

def render_latex_to_image(latex_code, filename):
    plt.figure(figsize=(3, 1.5))
    plt.text(0.5, 0.5, f"${latex_code}$", horizontalalignment='center', verticalalignment='center', fontsize=16)
    plt.axis('off')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

def generate_fraction_division_worksheet(num_problems=10, include_answer_key=False, output_path="fraction_division.pdf"):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('times', '', 16)
    pdf.ln(10)

    problems, solutions = generate_fraction_problems(num_problems)

    left_x = 10
    right_x = 110
    y_start = 40
    line_height = 20  # Increased line height for better spacing
    max_rows = 12
    per_page = max_rows * 2  # 2 columns

    for i, problem in enumerate(problems):
        if i % per_page == 0 and i != 0:
            pdf.add_page()

        local_idx = i % per_page
        col = local_idx // max_rows
        row = local_idx % max_rows
        x = left_x if col == 0 else right_x
        y = y_start + row * line_height

        image_filename = f'fraction_{i + 1}.png'
        render_latex_to_image(problem, image_filename)

        pdf.set_xy(x, y)
        pdf.cell(10, 10, f"{i + 1}.", align='L')
        pdf.image(image_filename, x=x + 12, y=y - 5, w=50, h=20)
        os.remove(image_filename)

    if include_answer_key:
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 20)
        pdf.cell(0, -10, 'Answer Key', 0, 1, 'C')
        pdf.set_font('times', '', 16)
        pdf.ln(10)

        y = 40

        for i, solution in enumerate(solutions):
            if i % per_page == 0 and i != 0:
                pdf.add_page()

            local_idx = i % per_page
            col = local_idx // max_rows
            row = local_idx % max_rows
            x = left_x if col == 0 else right_x
            y = y_start + row * line_height

            image_filename = f'solution_{i + 1}.png'
            latex_solution = rf"\frac{{{solution.numerator}}}{{{solution.denominator}}}"
            render_latex_to_image(latex_solution, image_filename)

            pdf.set_xy(x, y)
            pdf.cell(10, 10, f"{i + 1}.", align='L')
            pdf.image(image_filename, x=x + 12, y=y - 5, w=50, h=20)
            os.remove(image_filename)

    # Save the PDF
    output_dir = os.path.join(os.path.dirname(__file__), '../generated_pdfs')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, 'fraction_division.pdf')
    #pdf.output(pdf_path)
    pdf.output(output_path)
    
# To generate a PDF
#generate_fraction_division_worksheet(include_answer_key=True)