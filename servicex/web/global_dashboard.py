import itertools

from flask import render_template, request
from flask_restful import reqparse
from flask_sqlalchemy import Pagination

from servicex.decorators import admin_required
from servicex.models import TransformRequest


parser = reqparse.RequestParser()
sort_choices = ("start", "finish", "status")
parser.add_argument(
    "sort",
    choices=sort_choices,
    default="finish",
    help=f"Sort must be one of: {', '.join(map(repr, sort_choices))}."
)
order_choices = ("asc", "desc")
parser.add_argument(
    "order",
    choices=order_choices,
    default="desc",
    help="Order must be 'asc' or 'desc'."
)
dropdown_options = list(itertools.product(sort_choices, order_choices))


@admin_required
def global_dashboard():
    page = request.args.get('page', default=1, type=int)
    args = parser.parse_args()
    sort, order = args["sort"], args["order"]
    model_attributes = {
        "finish": TransformRequest.finish_time,
        "start": TransformRequest.submit_time,
        "status": TransformRequest.status
    }
    sort_attr = model_attributes[sort]
    pagination: Pagination = TransformRequest.query \
        .order_by(getattr(sort_attr, order)()) \
        .paginate(page=page, per_page=25, error_out=False)
    return render_template(
        "global_dashboard.html",
        pagination=pagination,
        dropdown_options=dropdown_options,
        active_sort=sort,
        active_order=order
    )
