import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, random
import sympy as sp
from fpdf import FPDF
from io import BytesIO
import tempfile

class PDF(FPDF):
    def header(self):
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '../math.png')

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        self.image(image_path, 10, 8, 25)
        self.set_font('helvetica', 'B', 20)
        self.cell(80)
        self.cell(30, 10, 'Basic Derivation Worksheet', align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def generate_derivative_problems(num_problems):
    problems = []
    solutions = []

    x = sp.Symbol('x')

    for _ in range(num_problems):
        degree = random.randint(1, 4)
        coefficients = [random.randint(1, 10) for _ in range(degree + 1)]
        polynomial = sum(coeff * x**deg for coeff, deg in zip(coefficients, range(degree, -1, -1)))

        derivative = sp.diff(polynomial, x)

        problems.append(rf"\frac{{d}}{{dx}}\left({sp.latex(polynomial)}\right)")
        solutions.append(sp.latex(derivative))

    return problems, solutions

def render_latex_to_image(latex_code):
    """Renders a LaTeX expression to an image file and returns it as a BytesIO object."""
    fig, ax = plt.subplots(figsize=(4, 1))
    ax.text(0.5, 0.5, f"${latex_code}$", horizontalalignment='center', verticalalignment='center', fontsize=12)
    ax.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

def generate_derivation_worksheet(num_problems=10, include_answer_key=False, output_path="basic_derivation.pdf"):
    pdf = PDF('P', 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=False, margin=15)
    pdf.add_page()
    pdf.set_font('times', '', 16)
    pdf.ln(10)

    problems, solutions = generate_derivative_problems(num_problems)

    left_x = 10
    right_x = 110
    y_start = 40
    line_height = 20  
    max_rows = 11
    questions_per_page = 22

    for i, problem in enumerate(problems):
        page_index = i // questions_per_page
        local_index = i % questions_per_page
        column = local_index // max_rows  
        row = local_index % max_rows

        if local_index == 0 and i != 0:
            pdf.add_page()

        y = y_start + (row * line_height)
        x = left_x if column == 0 else right_x

        image_stream = render_latex_to_image(problem)

        pdf.set_xy(x, y)
        pdf.cell(20, 10, f"{i + 1}.", align='L', ln=0)

        # Always place image a fixed distance right of the number
        image_x = x + 20  
        image_y = y - 2  

        # Save the image_stream to a temporary PNG file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
            tmp_img.write(image_stream.getvalue())
            tmp_img_path = tmp_img.name

        pdf.image(tmp_img_path, x=image_x, y=image_y, w=80, h=20)
        pdf.ln(15)

    if include_answer_key:
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 20)
        pdf.cell(0, -10, 'Answer Key', 0, 1, 'C')
        pdf.set_font('times', '', 16)
        pdf.ln(10)

        y_start = 40

        for i, solution in enumerate(solutions):
            page_index = i // questions_per_page
            local_index = i % questions_per_page
            column = local_index // max_rows
            row = local_index % max_rows

            if local_index == 0 and i != 0:
                pdf.add_page()

            y = y_start + (row * line_height)
            x = left_x if column == 0 else right_x

            image_stream = render_latex_to_image(solution)

            pdf.set_xy(x, y)
            pdf.cell(20, 10, f"{i + 1}.", align='L', ln=0)

            # Always place image a fixed distance right of the number
            image_x = x + 20  
            image_y = y - 2   
            
            # Save the image_stream to a temporary PNG file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
                tmp_img.write(image_stream.getvalue())
                tmp_img_path = tmp_img.name
            
            pdf.image(tmp_img_path, x=image_x, y=image_y, w=80, h=20)
            pdf.ln(15)

    # Save the PDF
    output_dir = os.path.join(os.path.dirname(__file__), '../generated_pdfs')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, 'basic_derivation.pdf')
    pdf.output(output_path)
    
# To generate a PDF
#generate_derivation_worksheet(include_answer_key=True)