from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from gtts import gTTS

app = Flask(__name__)

# Diretórios especificados pelo usuário
TEXT_DIRS = {
    'dom_casmurro': 'C:/Users/SAMSUNG/Desktop/Projetos Futuros/Machado_Assis_Surdos/Dom_Casmurro/Textos',
    'memorias_postumas': 'C:/Users/SAMSUNG/Desktop/Projetos Futuros/Machado_Assis_Surdos/Memorias_Postumas/Textos'
}
AUDIO_DIRS = {
    'dom_casmurro': 'C:/Users/SAMSUNG/Desktop/Projetos Futuros/Machado_Assis_Surdos/Dom_Casmurro/Audios',
    'memorias_postumas': 'C:/Users/SAMSUNG/Desktop/Projetos Futuros/Machado_Assis_Surdos/Memorias_Postumas/Audios'
}
VIDEO_DIRS = {
    'dom_casmurro': 'C:/Users/SAMSUNG/Desktop/Projetos Futuros/Machado_Assis_Surdos/Dom_Casmurro/Videos',
    'memorias_postumas': 'C:/Users/SAMSUNG/Desktop/Projetos Futuros/Machado_Assis_Surdos/Memorias_Postumas/Videos'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/textos/<int:capitulo_num>')
def buscar_texto(capitulo_num):
    obra = request.args.get('obra')
    if obra in TEXT_DIRS:
        capitulo_texto = os.path.join(TEXT_DIRS[obra], f'capitulo_{capitulo_num}.txt')
        try:
            with open(capitulo_texto, 'r', encoding='utf-8') as file:
                texto = file.read()
            return jsonify({'text': texto})
        except FileNotFoundError:
            return jsonify({'error': 'Capítulo não encontrado'})
    else:
        return jsonify({'error': 'Obra não localizada por enquanto'})

@app.route('/audios/<int:capitulo_num>')
def buscar_audio(capitulo_num):
    obra = request.args.get('obra')
    if obra in AUDIO_DIRS:
        audio_filename = os.path.join(AUDIO_DIRS[obra], f'capitulo_{capitulo_num}.mp3')
        if os.path.exists(audio_filename):
            return send_from_directory(AUDIO_DIRS[obra], f'capitulo_{capitulo_num}.mp3')
        else:
            return jsonify({'error': 'Áudio não encontrado'})
    else:
        return jsonify({'error': 'Obra não localizada por enquanto'})

@app.route('/convert_text_to_audio', methods=['POST'])
def convert_text_to_audio():
    dados = request.json
    obra = dados.get('obra')
    capitulo = dados.get('capitulo')
    if obra in TEXT_DIRS:
        capitulo_texto = os.path.join(TEXT_DIRS[obra], f'capitulo_{capitulo}.txt')
        try:
            with open(capitulo_texto, 'r', encoding='utf-8') as file:
                texto = file.read()
        except FileNotFoundError:
            return jsonify({'error': 'Arquivo de texto não encontrado'})

        tts = gTTS(texto, lang='pt-br')
        audio_filename = os.path.join(AUDIO_DIRS[obra], f'capitulo_{capitulo}.mp3')
        tts.save(audio_filename)

        return jsonify({'message': f'Áudio salvo em {audio_filename}', 'audio': audio_filename})
    else:
        return jsonify({'error': 'Obra não localizada por enquanto'})

@app.route('/video/<path:filename>')
def video(filename):
    obra = request.args.get('obra')
    if obra in VIDEO_DIRS:
        return send_from_directory(VIDEO_DIRS[obra], filename)
    else:
        return jsonify({'error': 'Obra não localizada por enquanto'})

if __name__ == '__main__':
    app.run(debug=True)
