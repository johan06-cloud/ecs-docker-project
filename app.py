from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    mock_results = []
    if query:
        mock_results = [
            {
                'title': f'{query} - Getting Started Guide',
                'snippet': f'Learn everything about {query} with our comprehensive guide covering the basics and advanced topics.'
            },
            {
                'title': f'Understanding {query} in 2026',
                'snippet': f'A deep dive into {query}, including best practices and common pitfalls to avoid.'
            },
            {
                'title': f'{query} vs Alternatives - Comparison',
                'snippet': f'See how {query} stacks up against similar solutions in the market today.'
            },
        ]
    return render_template('index.html', query=query, results=mock_results)

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)