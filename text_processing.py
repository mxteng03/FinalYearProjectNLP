from flask import Blueprint, request, jsonify
from malaya.normalizer.rules import Normalizer, Tokenizer
from transformers import T5ForConditionalGeneration, AutoTokenizer
from huggingface import load
from malaya.torch_model.huggingface import Classification
import logging

logging.basicConfig(level=logging.WARNING)

text_processing = Blueprint('text_processing', __name__)

tokenizer = AutoTokenizer.from_pretrained(
    'mesolitica/translation-t5-small-standard-bahasa-cased-v2',
    use_fast=False
)

translator_model = T5ForConditionalGeneration.from_pretrained(
    'mesolitica/translation-t5-small-standard-bahasa-cased-v2'
)

sentiment_model = load(
    model='mesolitica/sentiment-analysis-nanot5-small-malaysian-cased',
    class_model=Classification,
    available_huggingface={
        'mesolitica/sentiment-analysis-nanot5-small-malaysian-cased': {
            'Size (MB)': 167,
            'macro precision': 0.67602,
            'macro recall': 0.67120,
            'macro f1-score': 0.67339,
        }
    },
)

emoji_mapping = {
    'negative': '☹️',
    'neutral': '😐',
    'positive': '🙂'
}

def translator_to_ms(text):
    input_ids = tokenizer.encode(f'terjemah ke Melayu: {text}', return_tensors='pt')
    outputs = translator_model.generate(input_ids, max_length=1000)
    all_special_ids = [0, 1, 2]
    outputs = [i for i in outputs[0] if i not in all_special_ids]
    return tokenizer.decode(outputs, spaces_between_special_tokens=False)

def translator_to_en(text):
    input_ids = tokenizer.encode(f'terjemah ke English: {text}', return_tensors='pt')
    outputs = translator_model.generate(input_ids, max_length=1000)
    all_special_ids = [0, 1, 2]
    outputs = [i for i in outputs[0] if i not in all_special_ids]
    return tokenizer.decode(outputs, spaces_between_special_tokens=False)

malaya_tokenizer = Tokenizer().tokenize

normalizer = Normalizer(tokenizer=malaya_tokenizer)

@text_processing.route('/normalize', methods=['POST'])
def normalize_text():
   try:
    data = request.get_json()
    original_text = data.get('text', '') 

    preprocessed_text = original_text.capitalize()           
    normalized_result = normalizer.normalize(preprocessed_text)
    
    translation = translator_to_ms(normalized_result['normalize'])

    return jsonify({
        'original_text': original_text,
        'preprocessed_text': preprocessed_text,
        'normalized_text': translation
    })
   except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
   except Exception as e:
        logging.error(f"Error occurred during normalize: {str(e)}")
        return jsonify({'error': str(e)}), 500

@text_processing.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text = data.get('text', '')

        translation = translator_to_en(text)

        return jsonify({
            'original_input': text,
            'translation': translation
        })
    except Exception as e:
        logging.error(f"Error occurred during translation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@text_processing.route('/sentiment', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()
        text = data.get('text', '')

        sentiment_result = sentiment_model.predict([text])[0]
        sentiment_emoji = emoji_mapping.get(sentiment_result, '😐')  # Default to neutral if not found

        return jsonify({
            'text': text,
            'sentiment': sentiment_emoji
        })
    except Exception as e:
        logging.error(f"Error occurred during sentiment analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500
