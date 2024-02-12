from flask import Flask, jsonify, request, render_template, redirect
import logging

log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("api/setimage", methods=["POST"])
def set_image():
    json = request.get_json(force=True)

    jsonify({}), 201

if __name__ == "__main__":
    print("Started Rest API")
    app.run(host="0.0.0.0", port=80, debug=False)