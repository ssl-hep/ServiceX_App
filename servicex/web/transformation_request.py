from datetime import timedelta

from flask import render_template, abort
import humanize

from servicex.models import TransformRequest


def transformation_request(id_):
    req = TransformRequest.query.get(id_)
    if not req:
        abort(404)
    return render_template(
        'transformation_request.html', req=req, humanize=humanize, timedelta=timedelta
    )
