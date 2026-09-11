from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Tarea 1", "description": "Ejemplo"}
]

@app.get('/health')
def health():
    return jsonify(status='healthy')

@app.get('/tasks')
def list_tasks():
    return jsonify(tasks)

@app.get('/tasks/<int:task_id>')
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    return (jsonify(task), 200) if task else (jsonify(error='No encontrada'), 404)

@app.post('/tasks')
def create_task():
    data = request.get_json() or {}
    task = {
        "id": len(tasks) + 1,
        "title": data.get('title', 'Sin título'),
        "description": data.get('description', '')
    }
    tasks.append(task)
    return jsonify(task), 201

@app.put('/tasks/<int:task_id>')
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify(error='No encontrada'), 404
    task.update(request.get_json() or {})
    return jsonify(task)

@app.delete('/tasks/<int:task_id>')
def delete_task(task_id):
    global tasks
    old = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]
    return ('', 204) if len(tasks) < old else (jsonify(error='No encontrada'), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)