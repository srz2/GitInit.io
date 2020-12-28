import os
import requests
import configparser
from flask import Flask, session, request, make_response, render_template, redirect, send_from_directory

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = config['DEFAULT']['session_secret']

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/authorize')
def authorize():
    client_id = config['DEFAULT']['client_id']
    auth_url = f'http://github.com/login/oauth/authorize?client_id={client_id}&scope=user%20public_repo'
    print(auth_url)
    return redirect(auth_url)

@app.route('/connected')
def connected():
    code = request.args.get('code')
    token = request.args.get('access_token')
    print('Check Code:', code)
    print('Check token:', token)
    if not code is None:
        print('Retrieved Code:', code)

        r = requests.post('https://github.com/login/oauth/access_token', {
            'client_id': config['DEFAULT']['client_id'],
            'client_secret': config['DEFAULT']['client_secret'],
            'code': code,
            'redirect_uri': 'http://localhost:5000/connected'
        })
        print(str(r.text))
        return redirect('/connected?' + str(r.text))

    elif not token is None:
        print('Retrieved Authorization Code', token)
        resp = redirect('/')
        resp.set_cookie('authorization', token)
        return resp
    else:
        error_code = request.args.get('error')
        error_desc = request.args.get('error_description')
        error_uri = request.args.get('error_uri')
        print(f'Error Occured: {error_code}\n{error_desc}\n{error_uri}')
        return render_template('oauth_error.html')

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.run(debug=True)
