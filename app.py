import bottle
from bottle import route, run, template, BaseTemplate, static_file, request
from beaker.middleware import SessionMiddleware
import numpy_financial as npf


app = bottle.default_app()
BaseTemplate.defaults['get_url'] = app.get_url  # reference to function

session_opts = {
	'session.type': 'file',
	'session.cookie_expires': 300,
	'session.data_dir': './data',
	'session.auto': True
}

app  = SessionMiddleware(app, session_opts)


# ----------- system functions ----------------
@route('/')
def index():
	return template('index.html')

@route('/static/<filename:path>', name='static')
def serve_static(filename):
    return static_file(filename, root='static')

@route('/startover', method='POST')
def startover():
	return template('index.html')

# --------------- view #1 ----------------------
@route('/investment', method='POST')
def ppt_selector():

	initial_ivst = request.forms.investment

	# we use session(s) to pass over parameters between views

	sess = bottle.request.environ.get('beaker.session')
	if 'init_i' not in sess:
		sess['init_i'] = sess.get('init_i',initial_ivst)
	else:
		sess['init_i'] = initial_ivst
	sess.save()

	return template('computed.html', i_ivst = initial_ivst)

# --------------- view #2 ----------------------
@route('/cash-flow', method='POST')
def compute():

	y1 = request.forms.year1
	y2 = request.forms.year2
	y3 = request.forms.year3
	y4 = request.forms.year4
	y5 = request.forms.year5

	# get parameters from your own session

	sess = bottle.request.environ.get('beaker.session')
	if 'init_i' in sess:
		i_ivst = sess['init_i']
	else:
		i_ivst = 0
	sess.delete()

	# finaly we calculate the IRR value from the array

	r = npf.irr([float(y1) - float(i_ivst), float(y2), float(y3), float(y4), float(y5)])
	computed_irr = round(r * 100.0, 3)

	return template('outputsheet.html', irr_1 = str(computed_irr))

# --------------- Bottle ----------------------
# bottle.run(app=app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
bottle.run(app=app)



