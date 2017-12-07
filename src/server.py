import cherrypy
import json


@cherrypy.expose
class MusicWebService(object):

    @cherrypy.tools.accept(media='text/plain')
    
    def __init__(self):
        self.dict = {'currentLine' : 0}

    def GET(self):
        print "GET REQUEST"
        for key in self.dict:
            print "Key: " + key + ", Value: " + self.dict[key]
        return self.dict['currentLine']

    def POST(self):
        some_string = 'Initial'
        self.dict['currentLine'] = some_string
        return some_string

    def PUT(self):
        data = cherrypy.request.body.read()
        print "Data from server" + str(data)
        self.dict['currentLine'] = str(data)
        for key in self.dict:
            print "Key: " + key + ", Value: " + self.dict[key]

    def DELETE(self):
        self.dict.pop('currentLine', None)


if __name__ == '__main__':
    
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.quickstart(MusicWebService(), '/', conf)
