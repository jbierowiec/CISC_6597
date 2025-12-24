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
        self.cell(30, 10, 'Indefinite Integration Worksheet', align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def format_polynomial_latex(coefficients, degree, var='x'):
    terms = []
    x = var

    for coeff, deg in zip(coefficients, range(degree, -1, -1)):
        if coeff == 0:
            continue

        # sign handling
        sign = "+" if coeff > 0 else "-"
        abs_c = abs(coeff)

        # term body
        if deg == 0:
            body = f"{abs_c}"
        elif deg == 1:
            body = f"{'' if abs_c == 1 else abs_c}{x}"
        else:
            body = f"{'' if abs_c == 1 else abs_c}{x}^{deg}"

        terms.append((sign, body))

    if not terms:
        return "0"

    # first term: keep its sign only if negative
    first_sign, first_body = terms[0]
    poly = (f"-{first_body}" if first_sign == "-" else f"{first_body}")

    # remaining terms: always include +/- with spacing
    for sign, body in terms[1:]:
        poly += f" {sign} {body}"

    return poly

def sympy_to_latex_clean(expr):
    """
    Convert sympy expression to latex and remove \\left/\\right bloat.
    """
    s = sp.latex(expr)
    s = s.replace(r"\left", "").replace(r"\right", "")
    return s

def generate_indefinite_integral_problems(num_problems):
    problems = []
    solutions = []

    x = sp.Symbol('x')

    for _ in range(num_problems):
        degree = random.randint(1, 3)
        coefficients = [random.randint(-10, 10) for _ in range(degree + 1)]

        if all(c == 0 for c in coefficients):
            coefficients[random.randint(0, degree)] = random.randint(1, 10)

        polynomial = sum(coeff * x**deg for coeff, deg in zip(coefficients, range(degree, -1, -1)))
        antiderivative = sp.integrate(polynomial, x)
        poly_latex = format_polynomial_latex(coefficients, degree, var='x')

        problems.append(rf"\int ({poly_latex})\,dx")

        sol_latex = sympy_to_latex_clean(antiderivative) + r" + C"
        solutions.append(sol_latex)

    return problems, solutions

def render_latex_to_image(latex_code):
    """Renders a LaTeX expression to an image file and returns it as a BytesIO object."""
    fig, ax = plt.subplots(figsize=(4, 1))
    ax.text(0.5, 0.5, f"${latex_code}$",
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=12)
    ax.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

def generate_indefinite_integral_worksheet(num_problems=10, include_answer_key=False, output_path="indefinite_integration.pdf"):
    pdf = PDF('P', 'mm', 'Letter')
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=False, margin=15)
    pdf.add_page()
    pdf.set_font('times', '', 16)
    pdf.ln(10)

    problems, solutions = generate_indefinite_integral_problems(num_problems)

    left_x = 10
    right_x = 110
    y_start = 40
    line_height = 20
    max_rows = 11
    questions_per_page = 22

    tmp_files = []

    try:
        for i, problem in enumerate(problems):
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

            image_x = x + 20
            image_y = y - 2

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
                tmp_img.write(image_stream.getvalue())
                tmp_img_path = tmp_img.name
                tmp_files.append(tmp_img_path)

            pdf.image(tmp_img_path, x=image_x, y=image_y, w=80, h=20)

        if include_answer_key:
            pdf.add_page()
            pdf.set_font('helvetica', 'B', 20)
            pdf.cell(0, -10, 'Answer Key', 0, 1, 'C')
            pdf.set_font('times', '', 16)
            pdf.ln(10)

            for i, solution in enumerate(solutions):
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

                image_x = x + 20
                image_y = y - 2

                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
                    tmp_img.write(image_stream.getvalue())
                    tmp_img_path = tmp_img.name
                    tmp_files.append(tmp_img_path)

                pdf.image(tmp_img_path, x=image_x, y=image_y, w=80, h=20)

        # Save the PDF (either to provided output_path or your generated_pdfs folder)
        pdf.output(output_path)

    finally:
        # cleanup temp images
        for f in tmp_files:
            try:
                os.remove(f)
            except OSError:
                pass

# Example usage:
# generate_indefinite_integral_worksheet(include_answer_key=True)
