# FinalYearProject Malay NLP Application

## Description
A web application designed for normalizing Malay text, translating it to English, and performing sentiment analysis.

## Model
This project uses the following Models:

1. **Noisy Translation Small T5**: 
   - Citation: [mesolitica/translation-t5-small-standard-bahasa-cased-v2](https://huggingface.co/mesolitica/translation-t5-small-standard-bahasa-cased-v2)

2. **Sentiment Analysis Small Nanot5**: 
   - Citation: [mesolitica/sentiment-analysis-nanot5-small-malaysian-cased](https://huggingface.co/mesolitica/sentiment-analysis-nanot5-small-malaysian-cased)

## Installation

1. Clone the Repository:
        git clone <https://github.com/mxteng03/FinalYearProjectNLP>
        cd FinalYearProject

2. Set Up the Virtual Environment:
        python3 -m venv venv
        Windows: venv\Scripts\activate

3. Install Required Packages:
        pip install -r requirements.txt

## Features
- Text Normalization
- Translation 
- Sentiment Analysis

## Usage
1. Normalize Text: Enter a Malay text into the input box and click "Submit." The application will normalize the text.
2. Translate Text: The normalized text will be automatically translated to English.
3. Sentiment Analysis: The sentiment of the translated text will be analyzed, and the result will be displayed as an emoji.
