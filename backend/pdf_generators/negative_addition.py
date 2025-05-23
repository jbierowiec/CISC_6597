from fpdf import FPDF
import os
import random

class PDF(FPDF):
    def header(self):
        script_dir = os.path.dirname(__file__)  
        image_path = os.path.join(script_dir, '../math.png')

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        self.image(image_path, 10, 8, 25)
        self.set_font('helvetica', 'B', 20)
        self.cell(80)
        self.cell(30, 10, 'Negative Addition Worksheet', align='C')
        self.ln(30)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def generate_random_problems(num_problems, min_value=-20, max_value=20):
    """Generates random negative addition problems with positive and negative numbers."""
    problems = []
    solutions = []

    for _ in range(num_problems):
        a = random.randint(min_value, max_value)
        b = random.randint(min_value, max_value)

        # Ensure a mix of positive and negative numbers
        while a == 0:  # Avoid zero for variety
            a = random.randint(min_value, max_value)
        while b == 0:
            b = random.randint(min_value, max_value)

        problems.append(f"{a} + {b} =")
        solutions.append(a + b)
    
    return problems, solutions

def generate_negative_addition_worksheet(num_problems=10, include_answer_key=False, output_path="negative_addition.pdf"):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('helvetica', '', 12)

    num_columns = 2  # Number of columns
    col_width = pdf.w / num_columns - 10
    row_height = 10
    rows_per_page = 23

    # Generate random problems and solutions
    problems, solutions = generate_random_problems(num_problems)

    # Layout problems in columns
    for idx, problem in enumerate(problems):
        local_idx = idx % (rows_per_page * num_columns)
        page_idx = idx // (rows_per_page * num_columns)

        if local_idx == 0 and idx != 0:
            pdf.add_page()

        column = local_idx % num_columns
        row = local_idx // num_columns
        x = column * col_width + 10
        y = row * row_height + 40

        pdf.set_xy(x, y)
        pdf.set_font('times', '', 16)
        pdf.cell(10, 10, f"{idx + 1}.", align='R', ln=0)
        pdf.cell(col_width, row_height, problem, 0, 0, 'L')

    # Include answer key if requested
    if include_answer_key:
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 20)
        pdf.set_y(20)
        pdf.cell(0, 10, 'Answer Key', align='C', ln=True)
        pdf.set_font('times', '', 16)
        pdf.ln(15)

        for idx, solution in enumerate(solutions):
            local_idx = idx % (rows_per_page * num_columns)
            page_idx = idx // (rows_per_page * num_columns)

            if local_idx == 0 and idx != 0:
                pdf.add_page()

            column = local_idx % num_columns
            row = local_idx // num_columns
            x = column * col_width + 10
            y = row * row_height + 40

            pdf.set_xy(x, y)
            pdf.cell(10, 10, f"{idx + 1}.", align='R', ln=0)
            pdf.cell(col_width, row_height, str(solution), 0, 0, 'L')

    # Save the PDF
    output_dir = os.path.join(os.path.dirname(__file__), '../generated_pdfs')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, 'negative_addition.pdf')
    #pdf.output(pdf_path)
    pdf.output(output_path)
        
# To generate a PDF
#generate_negative_addition_worksheet(include_answer_key=True)