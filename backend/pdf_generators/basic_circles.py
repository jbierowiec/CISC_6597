import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os, random
import numpy as np
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "../math.png")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        self.image(image_path, 10, 8, 25)
        self.set_font("helvetica", "B", 20)
        self.cell(80)
        self.cell(30, 10, "Basic Circle Worksheet", align="C")
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 10)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def generate_circle_image(actual_radius: int, display_radius: int, filename: str, max_radius: int = 30):
    fig, ax = plt.subplots(figsize=(4, 4))

    circle = plt.Circle((0, 0), actual_radius, fill=False, edgecolor="black", linewidth=2)
    ax.add_patch(circle)

    # radius line
    ax.plot([0, actual_radius], [0, 0], color="black", linewidth=3)

    # label: what students see
    ax.text(
        0,
        actual_radius * 0.15,
        f"{display_radius} cm",
        fontsize=12,
        ha="left",
        va="bottom",
        fontweight="bold",
    )

    # fixed axis limits so images are comparable across radii
    pad = 2
    ax.set_xlim(-(max_radius + pad), (max_radius + pad))
    ax.set_ylim(-(max_radius + pad), (max_radius + pad))
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.savefig(filename, dpi=300)
    plt.close()


def generate_unique_radii(num_questions: int, min_radius: int = 10, max_radius: int = 30):
    if num_questions > (max_radius - min_radius + 1):
        raise ValueError("num_questions is too large for unique radii in the given range.")
    return random.sample(range(min_radius, max_radius + 1), num_questions)


def draw_circle_block(
    pdf: PDF,
    index: int,
    img_path: str,
    block_top_y: float,
    img_w_mm: float,
):
    left_x = 15
    line_h = 8

    # Question number
    pdf.set_xy(left_x, block_top_y)
    pdf.set_font("times", "", 16)
    pdf.cell(0, line_h, f"{index}.", ln=1)

    # Image centered
    x_center = (pdf.w - img_w_mm) / 2
    img_y = block_top_y + 6
    pdf.image(img_path, x=x_center, y=img_y, w=img_w_mm)

    # Text under image
    text_y = img_y + (img_w_mm * 0.75) + 10
    pdf.set_xy(left_x, text_y)
    pdf.cell(0, line_h, "Calculate the following:", ln=1)
    pdf.set_x(left_x)
    pdf.cell(0, line_h, "1. Diameter = __________ cm", ln=1)
    pdf.set_x(left_x)
    pdf.cell(0, line_h, "2. Circumference = __________ cm", ln=1)
    pdf.set_x(left_x)
    pdf.cell(0, line_h, "3. Area = __________ cm²", ln=1)


def generate_basic_circles_worksheet(num_problems=10, include_answer_key=False, output_path="basic_circles.pdf"):
    pdf = PDF("P", "mm", "Letter")
    pdf.alias_nb_pages()

    # IMPORTANT: disable auto page breaks so question blocks never split
    pdf.set_auto_page_break(auto=False)

    # ---- Radius rules ----
    ACTUAL_MIN = 10
    ACTUAL_MAX = 30
    DISPLAY_MOD = 30

    # Create circle records so answer key matches what students see
    actual_radii = generate_unique_radii(num_problems, ACTUAL_MIN, ACTUAL_MAX)
    circles = []
    for r_actual in actual_radii:
        r_display = (r_actual - ACTUAL_MIN) % DISPLAY_MOD + 1
        circles.append({"actual": r_actual, "display": r_display})

    # ---- PDF image scaling (by ACTUAL radius; visual size reflects actual) ----
    MIN_W = 30
    MAX_W = 80

    # Two blocks per page Y anchors (Letter)
    TOP_BLOCK_Y = 35
    BOTTOM_BLOCK_Y = 145

    image_files = []

    # ---- Questions: exactly 2 per page ----
    for i in range(0, num_problems, 2):
        pdf.add_page()

        # Top question
        c1 = circles[i]
        r_actual_1, r_display_1 = c1["actual"], c1["display"]
        img_w_1 = MIN_W + (r_actual_1 - ACTUAL_MIN) * (MAX_W - MIN_W) / (ACTUAL_MAX - ACTUAL_MIN)

        f1 = f"circle_{i}.png"
        generate_circle_image(r_actual_1, r_display_1, f1, max_radius=ACTUAL_MAX)
        image_files.append(f1)

        draw_circle_block(pdf, index=i + 1, img_path=f1, block_top_y=TOP_BLOCK_Y, img_w_mm=img_w_1)

        # Bottom question (if exists)
        if i + 1 < num_problems:
            c2 = circles[i + 1]
            r_actual_2, r_display_2 = c2["actual"], c2["display"]
            img_w_2 = MIN_W + (r_actual_2 - ACTUAL_MIN) * (MAX_W - MIN_W) / (ACTUAL_MAX - ACTUAL_MIN)

            f2 = f"circle_{i+1}.png"
            generate_circle_image(r_actual_2, r_display_2, f2, max_radius=ACTUAL_MAX)
            image_files.append(f2)

            draw_circle_block(pdf, index=i + 2, img_path=f2, block_top_y=BOTTOM_BLOCK_Y, img_w_mm=img_w_2)

    # ---- Answer key ----
    if include_answer_key:
        left_x = 15
        line_h = 7
        bottom_limit = pdf.h - 20

        # Start circles at the same height from the logo on EVERY answer key page
        CIRCLE_START_Y = 42

        def start_answer_key_page(show_title: bool):
            pdf.add_page()
            if show_title:
                # Put Answer Key right under the header (tight)
                pdf.set_font("helvetica", "B", 20)
                pdf.set_y(pdf.get_y() + 1)
                pdf.cell(0, -15, "Answer Key", ln=True, align="C")
            pdf.set_font("times", "", 14)
            return CIRCLE_START_Y

        y = start_answer_key_page(show_title=True)

        for i, c in enumerate(circles):
            # Use DISPLAY radius so answers match what students see on the image label
            r = c["display"]

            diameter = 2 * r
            circumference = 2 * np.pi * r
            area = np.pi * (r ** 2)

            needed = 4 * line_h + 3
            if y + needed > bottom_limit:
                # New page: no title, but SAME start height
                y = start_answer_key_page(show_title=False)

            pdf.set_xy(left_x, y)
            pdf.set_font("times", "B", 14)
            pdf.cell(0, line_h, f"Circle {i+1}:", ln=1)

            pdf.set_font("times", "", 14)
            pdf.set_x(left_x)
            pdf.cell(0, line_h, f"Diameter = {diameter:.2f} cm", ln=1)
            pdf.set_x(left_x)
            pdf.cell(0, line_h, f"Circumference = {circumference:.2f} cm", ln=1)
            pdf.set_x(left_x)
            pdf.cell(0, line_h, f"Area = {area:.2f} cm²", ln=1)

            y = pdf.get_y() + 2

    # Cleanup temp images
    for f in image_files:
        try:
            os.remove(f)
        except OSError:
            pass

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    pdf.output(output_path)

# Example local run:
#generate_basic_circles_worksheet(include_answer_key=True)