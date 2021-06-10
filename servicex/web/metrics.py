from flask import render_template


def metrics():
    return render_template('metrics.html')
