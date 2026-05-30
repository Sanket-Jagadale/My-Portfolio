from flask import Flask, render_template, send_from_directory, request, jsonify
from pathlib import Path
from chatbot import get_response

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resume')
def download_resume():
    return send_from_directory(BASE_DIR, 'resume.pdf', as_attachment=True)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'response': "Please say something!"}), 400
    
    response = get_response(user_message)
    return jsonify({'response': response})


@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(BASE_DIR, 'robots.txt')


@app.route('/sitemap.xml')
def sitemap_xml():
    return send_from_directory(BASE_DIR, 'sitemap.xml')


# Serve Google Search Console verification file(s) placed at project root
@app.route('/google8090a1307bb3d0a4.html')
def google_verify():
    return send_from_directory(BASE_DIR, 'google8090a1307bb3d0a4.html')

if __name__ == '__main__':
    app.run(debug=True)
