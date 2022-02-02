from flask import (
  Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from scoreCricket.auth import login_required
from scoreCricket.db import get_db

bp = Blueprint('match_info', __name__)


