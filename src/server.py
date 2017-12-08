import cherrypy
import json



@cherrypy.expose
class MusicWebService(object):
    exposed = True

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

def start_service():
    music = MusicWebService()
    optionsController = Options()
    dispatcher = cherrypy.dispatch.RoutesDispatcher()

    dispatcher.connect('music_get', '/',controller=music,action = 'GET',conditions=dict(method=['GET']))
    dispatcher.connect('title_get', '/song',controller=music,action = 'GET',conditions=dict(method=['GET']))
    dispatcher.connect('music_put','/',controller=music,action = 'PUT',conditions=dict(method=['PUT']))
    dispatcher.connect('title_put','/song',controller=music,action = 'PUT',conditions=dict(method=['PUT']))

    dispatcher.connect('options_music', '/', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('options_title', '/song', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))

    conf = {'global': {'server.socket_host': '127.0.0.1', 'server.socket_port': 8080},'/' : {'request.dispatch':dispatcher,'tools.CORS.on':True,}}

    #Update configuration and start the server
    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)

if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    start_service()

