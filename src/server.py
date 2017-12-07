import cherrypy
import json



@cherrypy.expose
class MusicWebService(object):

    @cherrypy.tools.accept(media='text/plain')
    
    def __init__(self):
        self.dict = {'currentLine' : 0}

    def GET(self):
        return self.dict['currentLine']

    def POST(self):
        some_string = 'Initial'
        self.dict['currentLine'] = some_string
        return some_string

    def PUT(self):
        data = cherrypy.request.body.read()
        self.dict['currentLine'] = str(data)

    def DELETE(self):
        self.dict.pop('currentLine', None)

class Options:
    def OPTIONS(self, *args, **kwargs):
            return ""

def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    music = MusicWebService()
    optionsController = Options()
    dispatcher = cherrypy.dispatch.RoutesDispatcher()

    #GET
    dispatcher.connect('get_vals', '/',controller=music,action = 'GET',conditions=dict(method=['GET']))
    dispatcher.connect('get_song', '/song/',controller=music,action = 'GET',conditions=dict(method=['GET']))

    #PUT
    dispatcher.connect('put_vals','/',controller=music,action = 'PUT',conditions=dict(method=['PUT']))
    dispatcher.connect('put_song','/song/',controller=music,action = 'PUT',conditions=dict(method=['PUT']))


    ###### OPTIONS #####
    dispatcher.connect('options_root', '/', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('options_song', '/song/', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            'tools.CORS.on': True
        }
    }
    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)