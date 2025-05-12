from fpdf import FPDF
import random, os

def generate_biology_matching_worksheet(include_answer_key=False):
    class PDF(FPDF):
        def header(self):
            script_dir = os.path.dirname(__file__)
            image_path = os.path.join(script_dir, 'math.png')

            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")

            self.image(image_path, 10, 8, 25)
            self.set_font('helvetica', 'B', 20)
            self.cell(80)
            self.cell(30, 10, 'Basic Binomial Worksheet', align='C')
            self.ln(20)

        def footer(self):
            self.set_y(-15)
            self.set_font('helvetica', 'I', 10)
            self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    # Words and Definitions
    biology_words = [
        "Mitochondria",
        "Photosynthesis",
        "Osmosis",
        "Chlorophyll",
        "Homeostasis",
        "Nucleus",
        "Enzyme",
        "Cell membrane",
        "DNA",
        "Ecosystem"
    ]

    definitions = [
        "Powerhouse of the cell, produces energy",
        "Process by which plants make food using sunlight",
        "Movement of water across a semi-permeable membrane",
        "Green pigment responsible for photosynthesis",
        "Maintaining a stable internal environment",
        "Control center of the cell containing genetic material",
        "Protein that speeds up chemical reactions",
        "Structure that controls what enters and exits the cell",
        "Genetic material carrying instructions for life",
        "Community of organisms interacting with their environment"
    ]

    # Create a mapping of words to definitions
    word_definition_mapping = dict(zip(biology_words, definitions))

    # Randomize the order of definitions
    randomized_indices = list(range(len(definitions)))
    random.shuffle(randomized_indices)
    randomized_definitions = [definitions[i] for i in randomized_indices]

    # Create a reverse mapping for the answer key
    answer_key_mapping = {i: randomized_indices.index(i) for i in range(len(definitions))}

    # Create PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('helvetica', '', 12)

    # Add instructions
    pdf.ln(8)
    pdf.multi_cell(0, 0, "Match the biology terms in Column A with their correct definitions in Column B.")
    pdf.ln(10)

    # Add Columns with wrapping
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(95, 10, "Column A: Biology Words", border=1, align='C')
    pdf.cell(95, 10, "Column B: Definitions", border=1, align='C')
    pdf.ln(15)
    pdf.set_font('times', '', 16)

    for i in range(10):
        pdf.cell(10, 10, f"{i + 1}.", border=0)
        pdf.cell(85, 10, biology_words[i], border=0)
        pdf.multi_cell(95, 10, f"{chr(65 + i)}. {randomized_definitions[i]}", border=0, align='L')
        pdf.ln(1)

    # Add Answer Key if requested
    if include_answer_key:
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 20)
        pdf.cell(0, -10, 'Answer Key', 0, 1, 'C')
        pdf.set_font('times', '', 16)
        pdf.ln(20)

        for i, word in enumerate(biology_words):
            correct_letter = chr(65 + answer_key_mapping[i])
            pdf.cell(0, 10, f"{i + 1}. {word} -> {correct_letter}", ln=True)

    # Save the PDF 
    output_dir = os.path.join(os.path.dirname(__file__), '../generated_pdfs')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, 'biology_matching.pdf')
    pdf.output(pdf_path)

# To generate a PDF
generate_biology_matching_worksheet(include_answer_key=True)