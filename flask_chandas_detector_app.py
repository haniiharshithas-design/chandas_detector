from flask import Flask, request,render_template_string 
from indic_transliteration import detect, sanscript 
from indic_transliteration.sanscript import transliterate 
import re

app = Flask(__name__)

HTML = """

<!DOCTYPE html><html>
<head>
    <title>Universal Auto Chandas Detector</title>
    <style>
        body {
            font-family: Georgia, serif;
            max-width: 900px;
            margin: 40px auto;
            background: #f8f5ef;
            padding: 20px;
        }
        textarea {
            width: 100%;
            height: 120px;
            font-size: 18px;
            padding: 10px;
        }
        button {
            padding: 10px 20px;
            margin-top: 10px;
            border: none;
            border-radius: 8px;
            background: #8b6f3d;
            color: white;
            font-size: 16px;
        }
        .syllable {
            display: inline-block;
            margin: 5px;
            padding: 8px 12px;
            border-radius: 10px;
            font-weight: bold;
        }
        .L { background: #d4edda; }
        .G { background: #f8d7da; }
    </style>
</head>
<body>
    <h1>Universal Auto Chandas Detector</h1>
    <form method="POST">
        <textarea name="verse" placeholder="Enter Sanskrit in any script"></textarea><br><br>
        <button type="submit">Detect</button>
    </form>{% if result %}
<h3>Detected Chandas: {{ result }}</h3>
<p><b>Detected Script:</b> {{ script }}</p>
<p><b>Normalized:</b> {{ normalized }}</p>
<p><b>Pattern:</b> {{ pattern }}</p>
<p><b>Syllable Count:</b> {{ syllable_count }}</p>

<h3>Syllable Analysis</h3>
{% for syl, lg in syllable_map %}
    <span class="syllable {{ lg }}">{{ syl }} ({{ lg }})</span>
{% endfor %}
{% endif %}

</body>
</html>
"""
def normalize_input(text):
     try:
         scheme = detect.detect(text)
         normalized = transliterate(text, scheme, sanscript.DEVANAGARI)
         return scheme, normalized 
     except Exception:
         return "unknown", text

def split_syllables(text):
    vowels = "अआइईउऊऋॠऌएऐओऔािीुूृॄॢेैोौंः"
    syllables = []
    current = ""

    for char in text:
        if char.isspace() or char == "।":
            if current:
                syllables.append(current)
                current = ""
            continue

        current += char

        # split when vowel sign or vowel appears
        if char in vowels:
            syllables.append(current)
            current = ""

    if current:
        syllables.append(current)

    return [s for s in syllables if s.strip()]

def laghu_guru(syllables):
    result = []
    long_vowels = "आईऊएऐओऔ"

    for syl in syllables:
        if any(v in syl for v in long_vowels) or len(syl) > 2:
            result.append((syl, "G"))
        else:
            result.append((syl, "L"))

    return result
def detect_chandas_by_count(syllables):
    count = len(syllables)

    # Flexible Anushtubh detection
    if 8 <= count <= 10:
        return "Anushtubh (single pada)"
    elif 16 <= count <= 20:
        return "Anushtubh (half shloka)"
    elif 30 <= count <= 34:
        return "Anushtubh"
    elif 11 <= count <= 12:
        return "Indravajra / Upendravajra"
    elif 16 <= count <= 18:
        return "Mandakranta"
    else:
        return "Unknown"
    
@app.route("/", methods=["GET", "POST"]) 
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    script = None
    normalized = None
    syllable_map = []
    pattern = ""
    syllable_count = 0

    if request.method == "POST":
        verse = request.form["verse"]

        script, normalized = normalize_input(verse)

        syllables = split_syllables(normalized)
        syllable_map = laghu_guru(syllables)
        syllable_count = len(syllables)

        pattern = "".join([lg for _, lg in syllable_map])
        result = detect_chandas_by_count(syllables)

    return render_template_string(
        HTML,
        result=result,
        script=script,
        normalized=normalized,
        syllable_map=syllable_map,
        pattern=pattern,
        syllable_count=syllable_count
    )

if __name__ == "__main__":
    app.run(debug=True)