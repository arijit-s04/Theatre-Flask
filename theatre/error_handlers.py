from flask.templating import render_template
from theatre import app

@app.errorhandler(404)
def error_404(e):
    return render_template('error_404.html', title="404"), 404


@app.errorhandler(403)
def error_403(e):
    return render_template('error_403.html', title="403"), 403


@app.errorhandler(500)
def error_500(e):
    return render_template('error_500.html', title="500"), 500
