import json
from flask import Blueprint

bp = Blueprint('filters', __name__)

@bp.app_template_filter('from_json')
def from_json(value):
    """Convert a JSON string to Python object"""
    try:
        return json.loads(value) if value else []
    except:
        return []
