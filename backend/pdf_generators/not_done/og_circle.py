import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, random
import numpy as np
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '../../math.png')

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        self.image(image_path, 10, 8, 25)
        self.set_font('helvetica', 'B', 20)
        self.cell(80)
        self.cell(30, 10, 'Basic Circle Worksheet', align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def generate_circle_image(actual_radius, display_radius, filename, max_radius=30):
    fig, ax = plt.subplots(figsize=(4, 4))

    circle = plt.Circle((0, 0), actual_radius, fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(circle)

    ax.plot([0, actual_radius], [0, 0], color='black', linewidth=3)

    ax.text(
        0,
        actual_radius * 0.15,
        f"{display_radius} cm",
        fontsize=12,
        ha='left',
        va='bottom',
        fontweight='bold'
    )

    pad = 2
    ax.set_xlim(-(max_radius + pad), max_radius + pad)
    ax.set_ylim(-(max_radius + pad), max_radius + pad)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.savefig(filename, dpi=300)
    plt.close()


def generate_unique_radii(num_questions, min_radius=10, max_radius=30):
    if num_questions > (max_radius - min_radius + 1):
        raise ValueError("num_questions is too large for unique radii in the given range.")
    return random.sample(range(min_radius, max_radius + 1), num_questions)


# ===============================
# DRAW ONE “CIRCLE BLOCK” AT A FIXED POSITION
# ===============================
def draw_circle_block(pdf: PDF, index: int, actual_radius: int, display_radius: int, img_path: str,
                      block_top_y: float, img_w_mm: float):
    """
    Draws one complete circle question block starting at block_top_y.
    This never splits across pages because we place everything with fixed Y coordinates.
    """

    left_x = 15
    line_h = 8

    # Question number
    pdf.set_xy(left_x, block_top_y)
    pdf.set_font('times', '', 16)
    pdf.cell(0, line_h, f"{index}.", ln=1)

    # Circle image (centered)
    x_center = (pdf.w - img_w_mm) / 2
    img_y = block_top_y + 6
    pdf.image(img_path, x=x_center, y=img_y, w=img_w_mm)

    # Text under image
    text_y = img_y + (img_w_mm * 0.9) + 6  # crude but consistent spacing
    pdf.set_xy(left_x, text_y)
    pdf.cell(0, line_h, "Calculate the following:", ln=1)
    pdf.set_x(left_x)
    pdf.cell(0, line_h, "1. Diameter = __________ cm", ln=1)
    pdf.set_x(left_x)
    pdf.cell(0, line_h, "2. Circumference = __________ cm", ln=1)
    pdf.set_x(left_x)
    pdf.cell(0, line_h, "3. Area = __________ cm²", ln=1)


# ===============================
# MAIN WORKSHEET GENERATION
# ===============================
def generate_circle_worksheet(num_problems=10, include_answer_key=False, output_path="basic_circles.pdf"):
    pdf = PDF('P', 'mm', 'Letter')
    pdf.alias_nb_pages()

    # IMPORTANT: disable auto page breaks so nothing splits mid-block
    pdf.set_auto_page_break(auto=False)

    ACTUAL_MIN = 10
    ACTUAL_MAX = 30
    DISPLAY_MOD = 30

    circles = generate_unique_radii(num_problems, ACTUAL_MIN, ACTUAL_MAX)

    # PDF image width scaling (mm)
    MIN_W = 30
    MAX_W = 80

    # Two blocks per page: top and bottom Y anchors
    TOP_BLOCK_Y = 35
    BOTTOM_BLOCK_Y = 145  # adjust if you want more/less whitespace

    image_files = []

    # Create pages in pairs (2 per page)
    for i in range(0, num_problems, 2):
        pdf.add_page()
        # Top block
        actual_radius = circles[i]
        display_radius = (actual_radius - ACTUAL_MIN) % DISPLAY_MOD + 1

        img_w = MIN_W + (actual_radius - ACTUAL_MIN) * (MAX_W - MIN_W) / (ACTUAL_MAX - ACTUAL_MIN)

        filename = f"circle_{i}.png"
        generate_circle_image(actual_radius, display_radius, filename, max_radius=ACTUAL_MAX)
        image_files.append(filename)

        draw_circle_block(
            pdf=pdf,
            index=i + 1,
            actual_radius=actual_radius,
            display_radius=display_radius,
            img_path=filename,
            block_top_y=TOP_BLOCK_Y,
            img_w_mm=img_w
        )

        # Bottom block (if exists)
        if i + 1 < num_problems:
            actual_radius2 = circles[i + 1]
            display_radius2 = (actual_radius2 - ACTUAL_MIN) % DISPLAY_MOD + 1

            img_w2 = MIN_W + (actual_radius2 - ACTUAL_MIN) * (MAX_W - MIN_W) / (ACTUAL_MAX - ACTUAL_MIN)

            filename2 = f"circle_{i+1}.png"
            generate_circle_image(actual_radius2, display_radius2, filename2, max_radius=ACTUAL_MAX)
            image_files.append(filename2)

            draw_circle_block(
                pdf=pdf,
                index=i + 2,
                actual_radius=actual_radius2,
                display_radius=display_radius2,
                img_path=filename2,
                block_top_y=BOTTOM_BLOCK_Y,
                img_w_mm=img_w2
            )

    # Answer key (optional) — also avoid splitting mid-entry by turning auto-break back on if you want
    if include_answer_key:
        pdf.add_page()

        left_x = 15
        line_h = 7
        bottom_limit = pdf.h - 20

        # Tunable positions (mm)
        ANSWER_TITLE_Y_FIRST = 28      # keep title high on page 6/7
        ANSWER_START_Y_FIRST = 38      # first "Circle 1" starts here (not too low)

        ANSWER_START_Y_SUBSEQUENT = 45 # start lower ONLY on new pages to avoid header/logo

        # --- Title (first answer key page only) ---
        pdf.set_font('helvetica', 'B', 20)
        pdf.set_y(ANSWER_TITLE_Y_FIRST)
        pdf.cell(0, 10, 'Answer Key', ln=True, align='C')

        pdf.set_font('times', '', 14)
        y = ANSWER_START_Y_FIRST

        for i, r in enumerate(circles):
            diameter = 2 * r
            circumference = 2 * np.pi * r
            area = np.pi * (r ** 2)

            needed = 4 * line_h + 3

            # If this entry won't fit, go to next page
            if y + needed > bottom_limit:
                pdf.add_page()
                # IMPORTANT: on subsequent pages, start lower so it NEVER hits the header/logo
                y = ANSWER_START_Y_SUBSEQUENT

            pdf.set_xy(left_x, y)
            pdf.set_font('times', 'B', 14)
            pdf.cell(0, line_h, f"Circle {i+1}:", ln=1)

            pdf.set_font('times', '', 14)
            pdf.set_x(left_x); pdf.cell(0, line_h, f"Diameter = {diameter:.2f} cm", ln=1)
            pdf.set_x(left_x); pdf.cell(0, line_h, f"Circumference = {circumference:.2f} cm", ln=1)
            pdf.set_x(left_x); pdf.cell(0, line_h, f"Area = {area:.2f} cm²", ln=1)

            y = pdf.get_y() + 2

    # Cleanup temp images
    for f in image_files:
        try:
            os.remove(f)
        except OSError:
            pass

    output_dir = os.path.join(os.path.dirname(__file__), '../generated_pdfs')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, 'circles.pdf')
    pdf.output(pdf_path)


# RUN
generate_circle_worksheet(include_answer_key=True)
