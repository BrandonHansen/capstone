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

    def CORS():
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
        cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            'tools.CORS.on': True
        }
    }
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    cherrypy.config.update(conf)
    cherrypy.quickstart(MusicWebService(), '/', conf)
    cherrypy.quickstart(MusicWebService(), '/song', conf)

