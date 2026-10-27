from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

tasks = []
next_id = 1

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager v1</title>
    <style>
        body {
            font-family: Arial;
            max-width: 650px;
            margin: 50px auto;
            background: #f4f6f9;
            padding: 20px;
        }
        h1 { color: #234; }
        form, li {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
        }
        input {
            padding: 10px;
            width: 70%;
        }
        button {
            padding: 10px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Task Manager v1</h1>
    <p>Add and view your tasks.</p>

    <form method="POST" action="/add">
        <input name="title" placeholder="Enter task name"
               required maxlength="120">
        <button type="submit">Add Task</button>
    </form>

    <h2>My Tasks</h2>
    <ul>
    {% for task in tasks %}
        <li>{{ task.id }}. {{ task.title }}</li>
    {% else %}
        <p>No tasks yet. Add your first task!</p>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    global next_id
    title = request.form.get("title", "").strip()

    if not title or len(title) > 120:
        return "Invalid task title", 400

    tasks.append({"id": next_id, "title": title})
    next_id += 1

    return redirect("/")

@app.route("/health")
def health():
    return {"status": "healthy", "version": "v1"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
