📜 Universal Auto Chandas Detector

A Flask-based Sanskrit Chandas detection system that automatically analyzes Sanskrit verses and predicts their metrical family using akshara segmentation, Laghu–Guru visualization, and syllable-count heuristics.

✨ Features

- 🌍 Automatic script normalization
- 📜 Devanagari Sanskrit support
- 🟢 Laghu/Guru syllable visualization
- 🔢 Syllable count based meter detection
- 📖 Supports Anushtubh, Indravajra, Mandakranta
- 🌐 Flask web interface
- 🚀 Python 3.14 compatible

🧠 Tech Stack

- Python
- Flask
- Regex / NLP heuristics
- Indic Transliteration

▶️ Run Locally

python -m pip install flask indic-transliteration
python flask_chandas_detector_app.py

Open:

http://127.0.0.1:5000

🧪 Example Input

कर्मण्येवाधिकारस्ते मा फलेषु कदाचन ।

🎯 Output

Detected Chandas: Anushtubh (single pada)
Markdown
##project screenshot
<img width="1082" height="430" alt="image" src="https://github.com/user-attachments/assets/b58e9d7a-175c-4fa9-9391-c61aaf8eed02" />


