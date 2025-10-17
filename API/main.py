from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Données en mémoire pour l'exemple
TODOS = [

    {"id": 1, "title": "Acheter du pain", "done": False},

    {"id": 2, "title": "Lire Flask docs", "done": True},
]

# on peut faire un unit test
def find_todo(todo_id):
    return next((t for t in TODOS if t["id"] == todo_id), None)


@app.get("/todos")
def list_todos():
    return jsonify(TODOS), 200


@app.get("/todos/<int:todo_id>")
def get_todo(todo_id):
    todo = find_todo(todo_id)

    if not todo:
        abort(404, description="Todo non trouvé")

    return jsonify(todo), 200


@app.post("/todos")
def create_todo():
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not title:
        abort(400, description="Champ 'title' requis")

    new_id = (max([t["id"] for t in TODOS]) + 1) if TODOS else 1

    todo = {"id": new_id, "title": title, "done": False}
    TODOS.append(todo)

    return jsonify(todo), 201


@app.patch("/todos/<int:todo_id>")
def update_todo(todo_id):
    todo = find_todo(todo_id)

    if not todo:
        abort(404, description="Todo non trouvé")

    data = request.get_json(silent=True) or {}

    if "title" in data: todo["title"] = data["title"]

    if "done" in data: todo["done"] = bool(data["done"])

    return jsonify(todo), 200


@app.delete("/todos/<int:todo_id>")
def delete_todo(todo_id):
    todo = find_todo(todo_id)

    if not todo:
        abort(404, description="Todo non trouvé")

    TODOS.remove(todo)

    return "", 204


# Gestion d'erreurs JSON propre

@app.errorhandler(400)
def handle_bad_request(err):
    return jsonify(error=err.description or str(err)), err.code

@app.errorhandler(404)
def handle_not_found(err):
    return jsonify(error=err.description or str(err)), err.code


if __name__ == "__main__":
    app.run(debug=True)