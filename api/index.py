from flask import Flask, request, render_template_string
from lxml import etree
import os

app = Flask(__name__)

with open('flag.txt', 'w') as f:
    f.write('CTF{xxe_p4rs3r_m4g1c}')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Auror Recruitment Portal</title>
    <style>
        body { background: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 40px; }
        .container { border: 1px solid #30363d; padding: 20px; background: #161b22; max-width: 600px; }
        h1 { color: #d4af37; }
        textarea { width: 100%; background: #050505; color: #58a6ff; border: 1px solid #30363d; padding: 10px; }
        input[type="submit"] { margin-top: 10px; background: #d4af37; color: #000; border: none; padding: 10px 20px; cursor: pointer; font-weight: bold; }
        .response { margin-top: 20px; color: #3fb950; white-space: pre-wrap; word-wrap: break-word; }
        .error { margin-top: 20px; color: #f85149; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Auror XML Resume Parser</h1>
        <p>Submit your details using our standardized XML format.</p>
        
        <form method="POST" action="/">
            <textarea name="resume" rows="10">
<resume>
    <name>Harry Potter</name>
    <skills>Defense Against the Dark Arts</skills>
</resume>
            </textarea><br>
            <input type="submit" value="Submit Application">
        </form>

        {% if message %}
            <div class="response"><strong>System Response:</strong><br>{{ message }}</div>
        {% endif %}
        {% if error %}
            <div class="error"><strong>Parser Error:</strong><br>{{ error }}</div>
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
                msg = f"Application received for: \n{applicant_name}\n\nWe will contact you via owl soon."
                return render_template_string(HTML_TEMPLATE, message=msg)
            else:
                return render_template_string(HTML_TEMPLATE, error="Invalid format. <name> tag missing.")
                
        except etree.XMLSyntaxError as e:
            return render_template_string(HTML_TEMPLATE, error=str(e))
            
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)