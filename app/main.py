from flask import Flask, request, render_template
from prometheus_client import Counter, generate_latest, REGISTRY
import os

app = Flask(__name__)

# Prometheus counter for request metrics
request_counter = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint'])

@app.route('/api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
    # Increment request count
    request_counter.labels(method=request.method, endpoint='/api').inc()

    # Extract headers and method
    headers = dict(request.headers)
    method = request.method

    # Parse request body safely
    body = None
    try:
        body = request.get_json(silent=True)
    except Exception:
        body = None

    if not body:
        body = request.form.to_dict() or request.data.decode('utf-8') or {}

    return render_template('response.html', headers=headers, method=method, body=body)

@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain; version=0.0.4'}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
