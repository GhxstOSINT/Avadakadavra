from flask import Flask, request, render_template_string
from lxml import etree
import os

app = Flask(__name__)

try:
    with open('/tmp/flag.txt', 'w') as f:
        f.write('Cruxhunt{xxe_p4rs3r_m4g1c}')
except Exception as e:
    print(f"Could not write flag: {e}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auror XML Parser</title>
    <style>
        * { box-sizing: border-box; }
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-color: #faf0e6;
            font-family: 'Times New Roman', Times, serif;
            color: #333333;
        }
        .parser-card {
            background-color: #fff8dc;
            padding: 40px;
            border-radius: 12px;
            border: 1px solid #e0d0b0;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            max-width: 600px;
            width: 95%;
            text-align: center;
        }
        h1 {
            font-size: 2.8em;
            margin-bottom: 20px;
            color: #b8860b;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-family: Georgia, 'Times New Roman', Times, serif;
        }
        p {
            font-size: 1.2em;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        .code-block {
            background-color: #2c2c2c;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 30px;
            text-align: left;
        }
        textarea.xml-input {
            width: 100%;
            height: 250px;
            padding: 20px;
            background: transparent;
            border: none;
            color: #ffffff;
            font-family: 'Courier New', Courier, monospace;
            font-size: 1em;
            line-height: 1.5;
            resize: vertical;
            outline: none;
        }
        button.submit-btn {
            background-color: #ffd700;
            color: #333333;
            border: none;
            padding: 15px 30px;
            font-size: 1.3em;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.1s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-family: Georgia, 'Times New Roman', Times, serif;
            width: 100%;
        }
        button.submit-btn:hover {
            background-color: #e6c200;
        }
        button.submit-btn:active {
            transform: scale(0.98);
        }
        .response-box {
            margin-top: 25px;
            background-color: #2c2c2c;
            color: #4CAF50;
            padding: 20px;
            border-radius: 8px;
            border-left: 5px solid #4CAF50;
            text-align: left;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'Courier New', Courier, monospace;
        }
        .error-box {
            margin-top: 25px;
            background-color: #2c2c2c;
            color: #f44336;
            padding: 20px;
            border-radius: 8px;
            border-left: 5px solid #f44336;
            text-align: left;
            font-family: 'Courier New', Courier, monospace;
        }
    </style>
</head>
<body>
    <div class="parser-card">
        <h1>Auror XML Resume Parser</h1>
        <p>Submit your details using our standardized XML format.</p>
        
        <form method="POST" action="/">
            <div class="code-block">
                <textarea name="resume" class="xml-input" spellcheck="false">&lt;resume&gt;
  &lt;name&gt;Harry Potter&lt;/name&gt;
  &lt;skills&gt;Defense Against the Dark Arts&lt;/skills&gt;
&lt;/resume&gt;</textarea>
            </div>
            <button type="submit" class="submit-btn">Submit Application</button>
        </form>

        {% if message %}
            <div class="response-box"><strong>System Response:</strong><br><br>{{ message }}</div>
        {% endif %}
        
        {% if error %}
            <div class="error-box"><strong>Parser Error:</strong><br><br>{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        xml_data = request.form.get('resume', '')
        
        try:
            parser = etree.XMLParser(resolve_entities=True, no_network=False)
            root = etree.fromstring(xml_data.encode('utf-8'), parser)
            applicant_name = root.findtext('name')
            
            if applicant_name:
                msg = f"Application received for:\n{applicant_name}\n\nWe will contact you via owl soon."
                return render_template_string(HTML_TEMPLATE, message=msg)
            else:
                return render_template_string(HTML_TEMPLATE, error="Invalid format. <name> tag missing.")
                
        except etree.XMLSyntaxError as e:
            return render_template_string(HTML_TEMPLATE, error=str(e))
            
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
