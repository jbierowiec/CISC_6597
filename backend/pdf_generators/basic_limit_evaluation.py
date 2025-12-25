from fpdf import FPDF
import os
import random
import sympy as sp
import tempfile
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO

plt.rcParams.update({
    "mathtext.fontset": "stix",      
    "font.family": "STIXGeneral",    
    "mathtext.default": "regular",   
})

class PDF(FPDF):
    def header(self):
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "../math.png")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        self.image(image_path, 10, 8, 25)
        self.set_font("helvetica", "B", 20)
        self.cell(80)
        self.cell(30, 10, "Basic Limit Evaluation Worksheet", align="C")
        self.ln(30)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 10)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

def sympy_latex_clean(expr) -> str:
    s = sp.latex(expr)
    # Cleaner for matplotlib mathtext
    return s.replace(r"\left", "").replace(r"\right", "")

def render_math_to_png(math_latex: str, fontsize: int = 15) -> BytesIO:
    """
    Render LaTeX-style math to a clean PNG using STIX fonts.
    Fixed-size canvas to prevent glyph overlap.
    """
    fig, ax = plt.subplots(figsize=(3.6, 0.6))
    fig.patch.set_alpha(0.0)
    ax.axis("off")

    ax.text(
        0,
        0.5,
        f"${math_latex}$",
        fontsize=fontsize,
        va="center",
        ha="left"
    )

    buf = BytesIO()
    plt.savefig(
        buf,
        format="png",
        dpi=300,
        transparent=True,
        bbox_inches="tight",
        pad_inches=0.05,
    )
    plt.close(fig)
    buf.seek(0)
    return buf

def _nonzero_int(lo, hi):
    while True:
        v = random.randint(lo, hi)
        if v != 0:
            return v

def make_problem_substitution(x):
    a = random.randint(-5, 5)
    b = random.randint(-9, 9)
    c = random.randint(-5, 5)
    d = random.randint(-9, 9)
    p = random.randint(-5, 5)

    if c * p + d == 0:
        d += 1

    expr = (a * x + b) / (c * x + d)
    return expr, p

def make_problem_factor_cancel(x):
    a = _nonzero_int(-8, 8)
    expr = (x**2 - a**2) / (x - a)
    return expr, a

def make_problem_cancel_common(x):
    p = _nonzero_int(-8, 8)
    m = _nonzero_int(1, 8)
    b = random.randint(-8, 8)
    expr = (m * (x - p) * (x + p) + b * (x - p)) / (x - p)
    return expr, p

def make_problem_rationalize(x):
    k = random.randint(0, 12)
    p = random.randint(0, 12)
    expr = (sp.sqrt(x + k) - sp.sqrt(p + k)) / (x - p)
    return expr, p

def make_problem_trig_sinx_over_x(x):
    k = _nonzero_int(1, 10)
    expr = sp.sin(k * x) / x
    return expr, 0

def make_problem_trig_one_minus_cos(x):
    k = _nonzero_int(1, 10)
    expr = (1 - sp.cos(k * x)) / (x**2)
    return expr, 0

PROBLEM_FACTORIES = [
    make_problem_substitution,
    make_problem_factor_cancel,
    make_problem_cancel_common,
    make_problem_rationalize,
    make_problem_trig_sinx_over_x,
    make_problem_trig_one_minus_cos,
]

def generate_random_limit_problems(num_problems):
    x = sp.Symbol("x", real=True)

    problems_latex = []
    solutions_latex = []

    for _ in range(num_problems):
        maker = random.choice(PROBLEM_FACTORIES)
        expr, p = maker(x)

        lim_val = sp.limit(expr, x, p)

        expr_ltx = sympy_latex_clean(expr)
        p_ltx = sympy_latex_clean(sp.Integer(p))
        lim_ltx = sympy_latex_clean(lim_val)

        # LaTeX-style problem:  \lim_{x\to p} (expr) =
        prob_ltx = rf"\lim_{{x\to {p_ltx}}}\left({expr_ltx}\right)="

        problems_latex.append(prob_ltx)
        solutions_latex.append(lim_ltx)

    return problems_latex, solutions_latex

def generate_basic_limit_evaluation_worksheet(
    num_problems=30,
    include_answer_key=False,
    output_path="basic_limit_evaluation.pdf",
):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("times", "", 16)

    num_columns = 2
    col_width = pdf.w / num_columns - 10
    row_height = 16
    rows_per_page = 16

    problems, solutions = generate_random_limit_problems(num_problems)

    tmp_files = []

    try:
        # Problems in columns
        for idx, problem_ltx in enumerate(problems):
            local_idx = idx % (rows_per_page * num_columns)

            if local_idx == 0 and idx != 0:
                pdf.add_page()

            column = local_idx % num_columns
            row = local_idx // num_columns

            x = column * col_width + 10
            y = row * row_height + 40

            # Number (text)
            pdf.set_xy(x, y)
            pdf.cell(10, 10, f"{idx + 1}.", align="R", ln=0)

            # Render LaTeX-style math to image
            img_buf = render_math_to_png(problem_ltx, fontsize=16)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(img_buf.getvalue())
                tmp_path = tmp.name
                tmp_files.append(tmp_path)

            # Place image where the problem text would go
            pdf.image(tmp_path, x=x + 12, y=y + 1, w=col_width - 20)

        # Answer key
        if include_answer_key:
            pdf.add_page()
            pdf.set_font("helvetica", "B", 20)
            pdf.set_y(20)
            pdf.cell(0, 10, "Answer Key", align="C", ln=True)
            pdf.set_font("times", "", 16)
            pdf.ln(15)

            for idx, sol_ltx in enumerate(solutions):
                local_idx = idx % (rows_per_page * num_columns)

                if local_idx == 0 and idx != 0:
                    pdf.add_page()

                column = local_idx % num_columns
                row = local_idx // num_columns

                x = column * col_width + 10
                y = row * row_height + 40

                pdf.set_xy(x, y)
                pdf.cell(10, 10, f"{idx + 1}.", align="R", ln=0)

                # Render solution as LaTeX math image
                img_buf = render_math_to_png(sol_ltx, fontsize=16)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                    tmp.write(img_buf.getvalue())
                    tmp_path = tmp.name
                    tmp_files.append(tmp_path)

                pdf.image(tmp_path, x=x + 12, y=y + 1, w=col_width - 20)

        # Save to ../generated_pdfs like your other script
        output_dir = os.path.join(os.path.dirname(__file__), "../generated_pdfs")
        os.makedirs(output_dir, exist_ok=True)

        if not os.path.isabs(output_path):
            output_path = os.path.join(output_dir, output_path)

        pdf.output(output_path)
        return output_path

    finally:
        # Always cleanup temp images
        for f in tmp_files:
            try:
                os.remove(f)
            except OSError:
                pass

# To generate a PDF
#generate_basic_limit_evaluation_worksheet(include_answer_key=True)