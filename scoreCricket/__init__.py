import os

from flask import Flask


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'cricket_score.sqlite'),
  )
  
  if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
  else:
    # load the teat config if passed in
    app.config.from_mapping(test_config)
    
  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass
  
  # a simple page
  @app.route('/love')
  def love():
    return "I don't like cricket, I love it."
  
  from . import db
  db.init_app(app)
  
  from . import auth
  app.register_blueprint(auth.bp)
  
  from . import match_info
  app.register_blueprint(match_info.bp)
  app.add_url_rule('/', endpoint='index')
  
  return app


@route('/')
def index():
  db = get_db
  matches = db.execute(
    'SELECT p.id, venue, team_a, team_b, date, scorer_id'
    ' FROM match_info p JOIN user u ON p.scorer_id = u.id'
    ' ORDER BY date DESC'
  ).fetchall()
  return render_template('match_info/index.html', matches=matches)
