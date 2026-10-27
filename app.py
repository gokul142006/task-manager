import os
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

tasks = []
next_id = 1

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager v2</title>
    <style>
        body {
            font-family: Arial;
            max-width: 650px;
            margin: 50px auto;
            background: #f4f6f9;
            padding: 20px;
        }

        h1 {
            color: #234;
        }

        form, li {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
        }

        input {
            padding: 10px;
            width: 65%;
            box-sizing: border-box;
        }

        button {
            padding: 10px;
            cursor: pointer;
        }

        .completed {
            color: green;
            font-weight: bold;
        }

        .pending {
            color: #b45309;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Task Manager v2</h1>
    <p>Add, view and update your tasks.</p>

    <form method="POST" action="/add">
        <input name="title"
               placeholder="Enter task name"
               required maxlength="120">
        <button type="submit">Add Task</button>
    </form>

    <h2>My Tasks</h2>
    <ul>
    {% for task in tasks %}
        <li>
            {{ task.id }}. {{ task.title }}
            <br><br>

            Status:
            <span class="{{ task.status.lower() }}">
                {{ task.status }}
            </span>

            <form method="POST"
                  action="/update/{{ task.id }}">
                <button type="submit">
                    {% if task.status == "Pending" %}
                        Mark Completed
                    {% else %}
                        Mark Pending
                    {% endif %}
                </button>
            </form>
        </li>
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
                "Completed"
                if task["status"] == "Pending"
                else "Pending"
            )
            break

    return redirect("/")


@app.route("/health")
def health():
    return {"status": "healthy", "version": "v2"}


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5001)),
        debug=False
    )