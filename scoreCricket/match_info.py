from flask import (
  Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from scoreCricket.auth import login_required
from scoreCricket.db import get_db

bp = Blueprint('match_info', __name__)


@bp.route('/')
def index():
  db = get_db()
  matches = db.execute(
    'SELECT p.id, venue, team_a, team_b, date, scorer_id'
    ' FROM match_info p JOIN user u ON p.scorer_id = u.username'
    ' ORDER BY date DESC'
  ).fetchall()
  return render_template('match_info/index.html', matches=matches)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
  if request.method =='POST':
    venue = request.form['venue']
    team_a = request.form['team_a']
    team_b = request.form['team_b']
    team_a_runs = request.form['team_a_runs']
    team_b_runs = request.form['team_b_runs']
    error = None

    if not team_a or not team_b:
      error = "Please enter two teams"

    if not team_a_runs or not team_b_runs:
      error = "Please enter a score for each team"
      
    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
        'INSERT INTO match_info (venue, team_a, team_b, team_a_runs, team_b_runs, scorer_id)'
        ' VALUES (?, ?, ?, ?, ?, ?)',
        (venue, team_a, team_b, team_a_runs, team_b_runs, g.user['username'])
      )
      db.commit()
      return redirect(url_for('match_info.index'))
    
  return render_template('match_info/create.html')

def get_match_details(id, check_author=True):
  match = get_db().execute(
    'SELECT p.id, scorer_id, date, venue, team_a, team_b, team_a_runs, team_b_runs'
    ' FROM match_info p JOIN user u ON p.scorer_id = u.username'
    ' WHERE p.id = ?',
    (id,)
  ).fetchone()
  
  if match is None:
    abort(404, f"Match id {id} doesn't exist.")
    
  if check_author and match['scorer_id'] != g.user['username']:
    abort(403)
    
  return match
