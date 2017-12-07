import cherrypy


@cherrypy.expose
class MusicWebService(object):

    @cherrypy.tools.accept(media='text/plain')

    def GET(self):
        return cherrypy.session['currentLine']

    def POST(self):
        some_string = 'Initial'
        cherrypy.session['currentLine'] = some_string
        return some_string

    def PUT(self, another_string):
        cherrypy.session['currentLine'] = another_string

    def DELETE(self):
        cherrypy.session.pop('currentLine', None)


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