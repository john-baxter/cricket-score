from flask import (
  Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from scoreCricket.auth import login_required
from scoreCricket.db import get_db

bp = Blueprint('match_info', __name__)


# @bp.route('/create', methods=('GET', 'POST'))
# @login_required
# def create():
#   if request.method == 'POST':
#     # date_and_time
#     venue = request.form['venue']
#     team_a = request.form['team_a']
#     team_b = request.form['team_b']
#     error = None
    
#     if not venue:
#       error = 'Venue is required.'
    
#     if not team_a:
#       error = 'Team A is required.'
    
#     if not team_b:
#       error = 'Team B is required.'
      
#     if error is not None:
#       flash(error)
#     else:
#       db = get_db()
#       db.execute(
#         'INSERT INTO match_info (scorer_id, venue, team_a, team_b'
#         ' VALUES (?, ?, ?, ?)',
#         (g.user['id'], venue, team_a, team_b)
#       )
#       db.commit()
#       return redirect(url_for(
#         # TODO
#         # template says `blog.index` but need to figure out what to put here
#         'match_info.index'
#       ))
      
#   return render_template(
#     # TODO
#     # template says `blog/create.html`
#     'match_info/create.html'
#   )
  
  
@bp.route('/')
def index():
  db = get_db()
  matches = db.execute(
    'SELECT p.id, venue, team_a, team_b, date, scorer_id'
    ' FROM match_info p JOIN user u ON p.scorer_id = u.id'
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
        (venue, team_a, team_b, team_a_runs, team_b_runs, g.user['id'])
      )
      db.commit()
      return redirect(url_for('match_info.index'))
    
  return render_template('match_info/create.html')
