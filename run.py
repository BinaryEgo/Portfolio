from application import app, app_SECRET_KEY
from flask_bootstrap import Bootstrap

app.config['SECRET_KEY'] = app_SECRET_KEY
Bootstrap(app)

if __name__ == '__main__':
    app.run(debug=True)
