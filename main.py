from flask import Flask, request, redirect
from werkzeug.routing import Rule

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app called `app` in `main.py`.
app = Flask(__name__)
app.url_map.add(Rule('/', endpoint='index'))
app.url_map.add(Rule('/204', endpoint='no_content'))
app.url_map.add(Rule('/301', endpoint='redirect301'))
app.url_map.add(Rule('/302', endpoint='redirect302'))
app.url_map.add(Rule('/<path:ignore>', endpoint='index'))


@app.endpoint('redirect301')
def redir301():
	return redirect('/destination', 301)


@app.endpoint('redirect302')
def redir301():
	return redirect('/destination', 302)


@app.endpoint('no_content')
def no_content():
	return '', 204


@app.endpoint('index')
def hello(ignore=''):
	status = request.args.get('status', None)

	for header in request.headers:
		print(f"{header}")

	return {
		'body': make_body(), # must be before it gets processed
		'url': request.url,
		'method': request.method,
		'path': request.path,
		'query': request.query_string.decode(),
		'queryParams': request.args,
		'queryParamsAll': request.args.to_dict(flat=False),
		'formParams': request.form,
		'formParamsAll': request.form.to_dict(flat=False),
		'headers': dict(request.headers),
	}, status


def make_body():
	if request.content_type == 'application/json':
		return request.json
	else:
		return request.get_data().decode()


if __name__ == '__main__':
	# This is used when running locally only. When deploying to Google App
	# Engine, a webserver process such as Gunicorn will serve the app. This
	# can be configured by adding an `entrypoint` to app.yaml.
	app.run(host='127.0.0.1', port=8088, debug=True)