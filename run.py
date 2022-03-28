from application import app, app_SECRET_KEY

app.config['SECRET_KEY'] = app_SECRET_KEY

if __name__ == '__main__':
    app.run(debug=True)
