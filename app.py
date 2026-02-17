from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

app = Flask(__name__)

if not os.path.exists("static"):
    os.makedirs("static")


@app.route("/")
def home():
    return render_template("index.html")


# -------- TEXT TRANSLATION ONLY --------
@app.route("/translate_text", methods=["POST"])
def translate_text():
    try:
        bengali_text = request.form.get("text", "")

        if bengali_text.strip() == "":
            return jsonify({"error": "No text provided"})

        # Translate Bengali → English
        english_text = GoogleTranslator(
            source='bn', target='en'
        ).translate(bengali_text)

        # Bengali voice
        bn_tts = gTTS(text=bengali_text, lang='bn')
        bn_tts.save("static/bn.mp3")

        # English voice
        en_tts = gTTS(text=english_text, lang='en', tld='co.in')
        en_tts.save("static/en.mp3")

        return jsonify({
            "bengali": bengali_text,
            "english": english_text,
            "bn_audio": "/static/bn.mp3",
            "en_audio": "/static/en.mp3"
        })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
