#!/usr/bin/python3

import tornado.ioloop
import tornado.web
import traceback

from manager import *

### Config ###
PORT = 8888
### ###

class MainHandler(tornado.web.RequestHandler):
	def stuff(self):
		try:
			username = self.get_argument("username");
			man = Manager(username)
			# TODO: add filters & stuff
			self.write(man.rank())
		except tornado.web.MissingArgumentError as e:
			traceback.print_exc()
			self.write("missing argument(s): username")

	def get(self):
		return self.stuff()
	def post(self):
		return self.stuff()

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("static/index.html")

def make_app():
	return tornado.web.Application([

		# Raking Endpoint
		(r"/api/rankuser", MainHandler),

		# Serve index.html on /
		(r"/", IndexHandler),

		# Serve everthing inside static/ on /
		(r"/(.*)",tornado.web.StaticFileHandler, {"path": "./static"},),
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(PORT)
	print("Web Server running on port", PORT);
	tornado.ioloop.IOLoop.current().start()


