from flask import render_template
import humanize

from servicex.models import TransformRequest, db


def active_requests():
    reqs = db.session.query(TransformRequest)\
        .filter(TransformRequest.status.in_({"Submitted", "Running"}))\
        .all()
    return render_template(
        "requests_table.html", transformation_requests=reqs, humanize=humanize
    )
