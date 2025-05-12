from fpdf import FPDF
import random, os

def generate_cpp_code_tracing_worksheet(include_answer_key=False):
    class PDF(FPDF):
        def header(self):
            script_dir = os.path.dirname(__file__)
            image_path = os.path.join(script_dir, 'math.png')

            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")

            self.image(image_path, 10, 8, 25)
            self.set_font('helvetica', 'B', 20)
            self.cell(80)
            self.cell(30, 10, 'Basic C++ Code Tracing Worksheet', align='C')
            self.ln(20)

        def footer(self):
            self.set_y(-15)
            self.set_font('helvetica', 'I', 10)
            self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    # Words and Definitions
    cpp_programs = [
'''// Program 1
#include <iostream>
using namespace std;

int main() {
    int a = 3, b = 10, sum = 0;

    while (a < b) {
        sum += a * b;
        a += 2;
        b -= 1;

        cout << "a: " << a << ", b: " << b << ", sum: " << sum << endl;
    }

    return 0;
}
''',

    '''// Program 2
#include <iostream>
using namespace std;

int main() {
    int x = 1, count = 0;

    while (x < 50) {
        x = x * 2;
        count++;

        cout << "x: " << x << ", count: " << count << endl;
    }

    return 0;
}
''',

    '''// Program 3
#include <iostream>
using namespace std;

int main() {
    int n = 5;
    int factorial = 1;

    while (n > 0) {
        factorial *= n;
        n--;

        cout << "n: " << n << ", factorial: " << factorial << endl;
    }

    return 0;
}
''',

    '''// Program 4
#include <iostream>
using namespace std;

int main() {
    int a = 1, b = 1, total = 0;

    while (a <= 10) {
        total += b;
        b += 2;
        a++;

        cout << "a: " << a << ", b: " << b << ", total: " << total << endl;
    }

    return 0;
}
''',

    '''// Program 5
#include <iostream>
using namespace std;

int main() {
    int num = 15;

    while (num > 0) {
        if (num % 3 == 0) {
            cout << num << " is divisible by 3" << endl;
        } else {
            cout << num << " is not divisible by 3" << endl;
        }

        num -= 2;
    }

    return 0;
}
''',

    '''// Program 6
#include <iostream>
using namespace std;

int main() {
    int i = 0, j = 10;

    while (i <= 5) {
        cout << "i: " << i << ", j: " << j << endl;
        i++;
        j -= 2;
    }

    return 0;
}
''',

    '''// Program 7
#include <iostream>
using namespace std;

int main() {
    int x = 10;
    int y = 1;

    while (x > 0) {
        y = y * 2;
        x -= 2;

        cout << "x: " << x << ", y: " << y << endl;
    }

    return 0;
}
''',

    '''// Program 8
#include <iostream>
using namespace std;

int main() {
    int counter = 0, limit = 5;

    while (counter < limit) {
        cout << "counter: " << counter << endl;
        counter++;
    }

    cout << "Loop ended" << endl;

    return 0;
}
''',

    '''// Program 9
#include <iostream>
using namespace std;

int main() {
    int i = 0;
    int sum = 0;

    while (i < 10) {
        sum += i;
        i += 3;

        cout << "i: " << i << ", sum: " << sum << endl;
    }

    return 0;
}
''',

    '''// Program 10
#include <iostream>
using namespace std;

int main() {
    int i = 6, j = 2;

    while (i >= 0) {
        int result = i * j;
        cout << "i: " << i << ", j: " << j << ", result: " << result << endl;
        i--;
        j++;
    }

    return 0;
}
'''
    ]

    # Randomly select 4 programs
    selected_programs = random.sample(cpp_programs, 4)




    # Create a mapping of words to definitions
    #word_definition_mapping = dict(zip(biology_words, definitions))

    # Randomize the order of definitions
    #randomized_indices = list(range(len(definitions)))
    #random.shuffle(randomized_indices)
    #randomized_definitions = [definitions[i] for i in randomized_indices]

    # Create a reverse mapping for the answer key
    #answer_key_mapping = {i: randomized_indices.index(i) for i in range(len(definitions))}

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

    with open("cpp_code_tracing_worksheet.txt", "w") as f:
        for i, program in enumerate(selected_programs, start=1):
            f.write(f"Program {i}:\n")
            f.write(program)
            f.write("\n" + "-" * 30 + "\n\n")

    '''
    for i in range(10):
        pdf.cell(10, 10, f"{i + 1}.", border=0)
        pdf.cell(85, 10, biology_words[i], border=0)
        pdf.multi_cell(95, 10, f"{chr(65 + i)}. {randomized_definitions[i]}", border=0, align='L')
        pdf.ln(1)
    '''

    '''
    # Add Answer Key if requested
    if include_answer_key:
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 20)
        pdf.cell(0, -10, 'Answer Key', 0, 1, 'C')
        pdf.set_font('times', '', 16)
        pdf.ln(20)

        for i, word in enumerate(biology_words):
            correct_letter = chr(65 + answer_key_mapping[i])
            pdf.cell(0, 10, f"{i + 1}. {word} -> {correct_letter}", ln=True)'
    '''

    # Save the PDF 
    output_dir = os.path.join(os.path.dirname(__file__), '../generated_pdfs')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, 'cpp_code_tracing.pdf')
    pdf.output(pdf_path)

# To generate a PDF
generate_cpp_code_tracing_worksheet(include_answer_key=True)