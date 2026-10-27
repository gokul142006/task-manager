
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

tasks = []
next_id = 1

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager v3</title>
    <style>
        body {
            font-family: Arial;
            background: #f3f5f9;
            max-width: 750px;
            margin: 70px auto;
        }
        form, .task {
            background: white;
            padding: 20px;
            margin: 12px 0;
            border-radius: 10px;
        }
        input { padding: 12px; width: 65%; }
        button { padding: 10px; cursor: pointer; margin: 4px; }
        .completed { color: green; }
        .pending { color: #c65d00; }
    </style>
</head>
<body>
    <h1>Task Manager v3</h1>
    <p>Add, view, update and delete your tasks.</p>

    <form action="/add" method="POST">
        <input name="title" placeholder="Enter task name"
               required maxlength="120">
        <button type="submit">Add Task</button>
    </form>

    <h2>My Tasks</h2>
    {% if tasks %}
        {% for task in tasks %}
        <div class="task">
            <h3>{{ task.title }}</h3>
            <p>Status:
                <strong class="{{ task.status.lower() }}">
                    {{ task.status }}
                </strong>
            </p>

            <form action="/update/{{ task.id }}" method="POST">
                <button type="submit">
                    {% if task.status == "Pending" %}
                        Mark Completed
                    {% else %}
                        Mark Pending
                    {% endif %}
                </button>
            </form>

            <form action="/delete/{{ task.id }}" method="POST"
                  onsubmit="return confirm('Delete this task?')">
                <button type="submit">Delete Task</button>
            </form>
        </div>
        {% endfor %}
    {% else %}
        <p>No tasks yet. Add your first task!</p>
    {% endif %}
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

    tasks.append({
        "id": next_id,
        "title": title,
        "status": "Pending"
    })

    next_id += 1
    return redirect("/")

@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = (
                "Completed" if task["status"] == "Pending"
                else "Pending"
            )
            break

    return redirect("/")

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect("/")

@app.route("/health")
def health():
    return {"status": "healthy", "version": "v3"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=False)
