from flask import render_template, abort, current_app

from servicex.decorators import oauth_required
from servicex.models import TransformRequest


@oauth_required
def transformation_request(id_: str):
    current_app.logger.info(f"Got transformation request: {id_}")
    if id_.isnumeric():
        req = TransformRequest.query.get(id_)
    else:
        req = TransformRequest.query.filter_by(request_id=id_).one()
    if not req:
        abort(404)
    return render_template('transformation_request.html', req=req)
