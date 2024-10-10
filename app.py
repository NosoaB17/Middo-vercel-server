from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from googletrans import Translator, LANGUAGES
import requests
import io
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)

translator = Translator()

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text')
    source = data.get('source', 'auto')
    target = data.get('target', 'en')

    if not text:
        return jsonify({'error': 'No text provided'}), 400
        
    try:
        # Translate to target language
        result = translator.translate(text, src=source, dest=target)
        
        # Translate to English (ESL) if source is not English
        esl_source = text if source == 'en' else translator.translate(text, src=source, dest='en').text
        
        # Translate target back to English (ESL) if target is not English
        esl_target = result.text if target == 'en' else translator.translate(result.text, src=target, dest='en').text
        
        return jsonify({
            'translatedText': result.text,
            'detectedLanguage': result.src,
            'eslSource': esl_source,
            'eslTarget': esl_target
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/languages', methods=['GET'])
def get_languages():
    return jsonify(LANGUAGES)

@app.route('/tts', methods=['GET'])
def text_to_speech():
    text = request.args.get('text', '')
    lang = request.args.get('lang', '')

    if not text or not lang:
        return jsonify({'error': 'Missing parameters'}), 400

    # Decode the URL-encoded text
    decoded_text = unquote(text)

    try:
        response = requests.get(
            'https://translate.google.com/translate_tts',
            params={
                'ie': 'UTF-8',
                'q': decoded_text,
                'tl': lang,
                'client': 'tw-ob'
            },
            stream=True
        )
        response.raise_for_status()
        
        return send_file(
            io.BytesIO(response.content),
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='tts_audio.mp3'
        )
    except Exception as e:
        return jsonify({'error': f'Error fetching TTS: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)