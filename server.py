import sys
import Queue

sys.path.append('tubes')
try:
    import tubes
except ImportError:
    print "you need tubes to make it work"
    print "http://github.com/marianoguerra/tubes"
    sys.exit(-1)

import webless

handler = tubes.Handler()
handler.register_static_path('/css', 'css/')
handler.register_static_path('/js', 'js/')

counter = 0
scripts = {}

def run_script(url, script):
    result = Queue.Queue()

    browser = webless.Browserless(url)
    def inject_fun(view, frame):
        browser.inject_file('js/jquery.js')
        browser.inject_file('js/json2.js')
        browser.inject_script(script)
        code = browser.get_code()
        result.put(code)

    browser.view.connect('load-finished', inject_fun)

    while True:
        webless.process_events()
        try:
            return result.get(True, 1.0)
        except Queue.Empty:
            pass

def run_script1(url, script):
    result = run_script(url, script)

    if result is None:
        return tubes.Response('timeout', 408)

    return result

@handler.get('^/?$', produces=tubes.HTML)
@handler.get('^/index.html$', produces=tubes.HTML)
def get_main(request):
    return file('index.html')

@handler.get('^/(.*)/?$', produces=tubes.HTML)
def get_script(request, sid):
    global scripts
    if sid in scripts:
        return run_script1(*scripts[sid])

    return tubes.Response('not found', 404)

@handler.post('^/?$', produces=tubes.HTML, accepts=tubes.JSON)
def new_script(request, body):
    global scripts, counter
    if 'url' not in body or 'code' not in body:
        return tubes.Response('Invalid request', 500)

    scripts[str(counter)] = (body['url'], body['code'])
    counter += 1

    return '<a href="/%d">test your script</a>' % (counter - 1,)

@handler.post('^/test/?$', produces=tubes.HTML, accepts=tubes.JSON)
def test_script(request, body):
    if 'url' not in body or 'code' not in body:
        return tubes.Response('Invalid request', 500)

    return run_script1(body['url'], body['code'])

if __name__ == '__main__':
    tubes.run(handler)
