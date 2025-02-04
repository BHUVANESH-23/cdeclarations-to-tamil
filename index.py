import subprocess
import os
from functools import lru_cache
from flask import Flask, request, render_template, jsonify # type: ignore
from translation.tam_trans import to_Tamil # type: ignore

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query: str | None = request.form.get("query")
        if query:
            if query == "help":
                return jsonify({"output": "சின்டாக்ஸ் பிழை"})  # Change help response to Tamil
            return jsonify({"output": translate(query.strip())})
        return jsonify({"error": "பிழை"})  # Change error response to Tamil
    return render_template("index.html")

SYNTAX_ERROR = "syntax error"

current_directory: str = os.getcwd()
command: list[str] = [os.path.join(current_directory, "cdecl")]

@lru_cache(None)
def translate(query: str) -> str:
    print(f"translate : {translate.cache_info()}")
    storage_classes: list[str] = ["auto", "extern", "static", "register"]
    q_l: list[str] = query.split()
    if q_l[0] in ("declare", "cast"):
        return to_Tamil(SYNTAX_ERROR)  # Change to Tamil translation
    if len(q_l) < 3 and q_l[0] in storage_classes:
        query = f"{q_l[0]} int {q_l[1]}"
    queries: list[str] = [query, f"explain {query};", f"declare {query};"]

    translated_text = None
    with subprocess.Popen(
        command, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    ) as process:
        output, _ = process.communicate(input="\n".join(queries).encode())
        for line in output.splitlines():
            line = line.decode()
            if line and line != SYNTAX_ERROR:
                print(line)
                translated_text = to_Tamil(line)  # Change to Tamil translation
                break

    return translated_text or to_Tamil(SYNTAX_ERROR)  # Change to Tamil translation

if __name__ == "__main__":
    from waitress import serve  # type: ignore # Production WSGI server
    serve(app, host="0.0.0.0", port=5000)
