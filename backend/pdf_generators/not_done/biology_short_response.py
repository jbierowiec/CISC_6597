from fpdf import FPDF
import os

def generate_short_response_worksheet(output_file):
    class PDFWorksheet(FPDF):
        def header(self):
            script_dir = os.path.dirname(__file__)
            image_path = os.path.join(script_dir, 'math.png')

            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")

            self.image(image_path, 10, 8, 25)
            self.set_font('helvetica', 'B', 20)
            self.cell(80)
            self.cell(30, 10, 'Basic Binomial Worksheet', align='C')
            self.ln(30)

        def footer(self):
            self.set_y(-15)
            self.set_font('helvetica', 'I', 10)
            self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

        def add_question(self, question, question_number):
            pdf.set_font('times', '', 16)
            self.multi_cell(0, 10, f"{question_number}. {question}")
            self.ln(2)
            self.cell(0, 35, '', border=1)  # Adjusted height for the answer box
            self.ln(35)

    # Biology questions for the worksheet
    questions = [
        "Explain the process of photosynthesis and its importance to plants.",
        "Describe the structure and function of a cell membrane.",
        "What is DNA, and why is it important for inheritance?",
        "How do environmental factors affect the rate of enzyme activity?",
        "What are the differences between mitosis and meiosis?"
    ]

    pdf = PDFWorksheet()
    pdf.add_page()

    # Add questions to the PDF
    for i, question in enumerate(questions, start=1):
        pdf.add_question(question, i)

    # Save the PDF
    output_dir = os.path.join(os.path.dirname(__file__), '../generated_pdfs')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, 'biology_short_response.pdf')
    pdf.output(pdf_path)

# Generate the PDF worksheet
generate_short_response_worksheet("biology_word_problems.pdf")