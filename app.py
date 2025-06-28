print("🔥 POLIPITCH LIVE VERSION LOADED")

import openai
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        industry = request.form.get("industry")
        response_text = generate_idea(industry)
        slides = parse_response(response_text)
        return render_template("index.html", slides=slides)
    return render_template("index.html", slides=None)

from flask import make_response
from weasyprint import HTML

from flask import make_response
from weasyprint import HTML

@app.route("/export", methods=["POST"])
def export_pdf():
    slides_html = request.form.get("slides")
    pdf = HTML(string=slides_html).write_pdf()
    
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=pitch_deck.pdf"
    return response





import openai

def generate_idea(industry):
    prompt = f"""
You're a world-class startup founder. Based on the industry: "{industry}", generate the following in this exact format:

<name> ... </name>
<problem> ... </problem>
<solution> ... </solution>
<features> ... </features>
<business_model> ... </business_model>
<pitch_slides> ... </pitch_slides>
<investor_pitch> ... </investor_pitch>
"""


    response = openai.ChatCompletion.create(  # ✅ no OpenAI() object!
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


import re

def parse_response(response_text):
    def extract(tag):
        match = re.search(f"<{tag}>(.*?)</{tag}>", response_text, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    return {
        "name": extract("name"),
        "problem": extract("problem"),
        "solution": extract("solution"),
        "features": extract("features"),
        "business_model": extract("business_model"),
        "pitch_slides": extract("pitch_slides"),
        "investor_pitch": extract("investor_pitch"),
    }



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

#source .venv/bin/activate
#pip install openai==0.28