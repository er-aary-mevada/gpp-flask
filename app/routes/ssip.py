from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('ssip', __name__)

@bp.route('/ssip')
@login_required
def index():
    return render_template('ssip/index.html')
