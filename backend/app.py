from flask import Flask, send_from_directory, request, jsonify, session, send_file, json
from flask_cors import CORS
from fpdf import FPDF
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()  

from pdf_generators.basic_addition import generate_addition_worksheet
from pdf_generators.basic_subtraction import generate_subtraction_worksheet
from pdf_generators.basic_multiplication import generate_multiplication_worksheet
from pdf_generators.basic_division import generate_division_worksheet

from pdf_generators.negative_addition import generate_negative_addition_worksheet
from pdf_generators.negative_subtraction import generate_negative_subtraction_worksheet
from pdf_generators.negative_multiplication import generate_negative_multiplication_worksheet
from pdf_generators.negative_division import generate_negative_division_worksheet

from pdf_generators.fraction_addition import generate_fraction_addition_worksheet
from pdf_generators.fraction_subtraction import generate_fraction_subtraction_worksheet
from pdf_generators.fraction_multiplication import generate_fraction_multiplication_worksheet
from pdf_generators.fraction_division import generate_fraction_division_worksheet

from pdf_generators.distributive_property import generate_distributive_property_worksheet
from pdf_generators.quadratic_formula import generate_quadratic_formula_worksheet

from pdf_generators.basic_derivation import generate_derivation_worksheet
from pdf_generators.basic_integration import generate_integral_worksheet


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_pdfs")
#OUTPUT_DIR = os.path.join(os.getcwd(), "generated_pdfs") 
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-fallback-secret")
CORS(app, resources={r"/*": {"origins": "*"}})


def log_worksheet_generation(topic, subtopic, subsubtopic, worksheet_type, question_count, include_answer_key):
    log_path = "worksheet_log.json"
    log_entry = {
        "user": session.get("name", "Anonymous"),
        "email": session.get("email"),
        "topic": topic,
        "subtopic": subtopic,
        "subsubtopic": subsubtopic,
        "worksheet_type": worksheet_type,
        "question_count": question_count,
        "include_answer_key": include_answer_key,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_entry)

    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2)


@app.route("/")
def index():
    return "Backend Running"

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route("/downloads/<path:filename>")
def downloads(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


@app.route('/generate-basic-addition', methods=['POST'])
def generate_addition():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"basic_addition_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_addition_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)

        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Arithmetic",
            subsubtopic="Basic Addition",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )

        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-basic-subtraction', methods=['POST'])
def generate_subtraction():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"basic_subtraction_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_subtraction_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)

        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Arithmetic",
            subsubtopic="Basic Subtraction",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )

        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/generate-basic-multiplication', methods=['POST'])
def generate_multiplication():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"basic_multiplication_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_multiplication_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)
        
        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Arithmetic",
            subsubtopic="Basic Multiplication",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )

        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/generate-basic-division', methods=['POST'])
def generate_division():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"basic_division_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_division_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)
        
        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Arithmetic",
            subsubtopic="Basic Division",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )
        
        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
   

@app.route('/generate-negative-addition', methods=['POST'])
def generate_negative_addition():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"negative_addition_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_negative_addition_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)
        
        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Arithmetic",
            subsubtopic="Negative Addition",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )

        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/generate-negative-subtraction', methods=['POST'])
def generate_negative_subtraction():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"negative_subtraction_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_negative_subtraction_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)
        
        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Arithmetic",
            subsubtopic="Negative Subtraction",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )

        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/generate-negative-multiplication', methods=['POST'])
def generate_negative_multiplication():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"negative_multiplication_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_negative_multiplication_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)
        
        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Arithmetic",
            subsubtopic="Negative Multiplication",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )

        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-negative-division', methods=['POST'])
def generate_negative_division():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"negative_division_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_negative_division_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)
        
        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Arithmetic",
            subsubtopic="Negative Division",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )

        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/generate-fraction-addition', methods=['POST'])
def generate_fraction_addition():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"fraction_addition_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_fraction_addition_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)
        
        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Arithmetic",
            subsubtopic="Fraction Addition",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )
        
        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-fraction-subtraction', methods=['POST'])
def generate_fraction_subtraction():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"fraction_subtraction_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_fraction_subtraction_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)
        
        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Arithmetic",
            subsubtopic="Fraction Subtraction",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )

        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/generate-fraction-multiplication', methods=['POST'])
def generate_fraction_multiplication():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"fraction_multiplication_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_fraction_multiplication_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)
        
        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Arithmetic",
            subsubtopic="Fraction Multiplication",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )
        
        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/generate-fraction-division', methods=['POST'])
def generate_fraction_division():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"fraction_division_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_fraction_division_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)
        
        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Arithmetic",
            subsubtopic="Fraction Division",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )
        
        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate-distributive-property', methods=['POST'])
def generate_distributive_property():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"distributive_property_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_distributive_property_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)
        
        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Arithmetic",
            subsubtopic="Distributive Property",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )
        
        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/generate-quadratic-formula', methods=['POST'])
def generate_quadratic_formula():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"quadratic_formula_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_quadratic_formula_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)
        
        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Arithmetic",
            subsubtopic="Quadratic Formula",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )
        
        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate-integrals', methods=['POST'])
def generate_integrals():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"basic_integration_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_integral_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)
        
        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Calculus I",
            subsubtopic="Basic Integration",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )
        
        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-derivatives', methods=['POST'])
def generate_derivatives():
    data = request.json
    include_answer_key = data.get('includeAnswerKey', False)
    num_problems = data.get("questionCount", 10)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"basic_derivation_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        generate_derivation_worksheet(num_problems, include_answer_key=include_answer_key, output_path=filepath)
        
        log_worksheet_generation(
            topic="Mathematics",
            subtopic="Calculus I",
            subsubtopic="Basic Derivation",
            worksheet_type="Practice",
            question_count=num_problems,
            include_answer_key=include_answer_key
        )

        return jsonify({
            "message": f"Worksheet with {num_problems} questions generated successfully.",
            "downloadUrl": f"/downloads/{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/download/<worksheet_type>')
def download(worksheet_type):
    file_mapping = {
        "basic_addition": "generated_pdfs/basic_addition.pdf",
        "basic_subtraction": "generated_pdfs/basic_subtraction.pdf",
        "basic_multiplication": "generated_pdfs/basic_multiplication.pdf",
        "basic_division": "generated_pdfs/basic_division.pdf",
        "negative_addition": "generated_pdfs/negative_addition.pdf",
        "negative_subtraction": "generated_pdfs/negative_subtraction.pdf",
        "negative_multiplication": "generated_pdfs/negative_multiplication.pdf",
        "negative_division": "generated_pdfs/negative_division.pdf",
        "basic_integration": "generated_pdfs/basic_integration.pdf",
        "basic_derivation": "generated_pdfs/basic_derivation.pdf",
        "fraction_addition": "generated_pdfs/fraction_addition.pdf",
        "fraction_subtraction": "generated_pdfs/fraction_subtraction.pdf",
        "fraction_multiplication": "generated_pdfs/fraction_multiplication.pdf",
        "fraction_division": "generated_pdfs/fraction_division.pdf",
        "distributive_property": "generated_pdfs/distributive_property.pdf",
        "quadratic_formula": "generated_pdfs/quadratic_formula.pdf",
    }

    file_path = file_mapping.get(worksheet_type)
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404


if __name__ == "__main__":
    app.run(debug=True)
