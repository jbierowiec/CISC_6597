from fpdf import FPDF
import os
import random

class PDF(FPDF):
    def header(self):
        script_dir = os.path.dirname(__file__)  
        image_path = os.path.join(script_dir, 'math.png')

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        self.image(image_path, 10, 8, 25)
        self.set_font('helvetica', 'B', 20)
        self.cell(80)
        self.cell(30, 10, 'Basic Division Worksheet', align='C')
        self.ln(30)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def generate_random_problems(num_problems, min_value=1, max_value=20):
    """Generates random division problems and their solutions."""
    problems = []
    solutions = []

    for _ in range(num_problems):
        b = random.randint(min_value, max_value)  # Choose a non-zero divisor
        quotient = random.randint(min_value, max_value)  # Choose a random quotient
        a = b * quotient  # Calculate the dividend as a multiple of the divisor

        while b == 0:  # Ensure 'b' is not zero
            b = random.randint(min_value, max_value)
        problems.append(f"{a} ÷ {b} =")
        # solutions.append(a / b)
        solutions.append(quotient)
    
    return problems, solutions

def generate_division_worksheet(num_problems=10, include_answer_key=False, output_path="basic_division.pdf"):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('times', '', 16)

    num_columns = 2  # Number of columns
    col_width = pdf.w / num_columns - 10
    row_height = 10
    rows_per_page = 23

    # Generate random problems and solutions
    problems, solutions = generate_random_problems(num_problems)

    # Layout problems in columns
    for idx, problem in enumerate(problems):
        '''
        x = (idx % num_columns) * col_width + 10
        y = (idx // num_columns) * row_height + 40
        pdf.set_xy(x, y)
        pdf.cell(10, 10, f"{idx + 1}.", align='R', ln=0)
        pdf.cell(col_width, row_height, problem, 0, 0, 'L')
        '''
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
            '''
            x = (idx % num_columns) * col_width + 10
            y = (idx // num_columns) * row_height + 40
            pdf.ln(10)
            pdf.set_xy(x, y)
            pdf.cell(10, 10, f"{idx + 1}.", align='R', ln=0)
            pdf.cell(col_width, row_height, str(solution), 0, 0, 'L')
            '''
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
    pdf_path = os.path.join(output_dir, 'basic_division.pdf')
    #pdf.output(pdf_path)
    pdf.output(output_path)

# To generate a PDF
generate_division_worksheet(include_answer_key=True)