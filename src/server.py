#!/usr/bin/python3

import json
import tornado.ioloop
import tornado.web
import traceback

import manager

### Config ###
PORT = 8888
### ###

class MainHandler(tornado.web.RequestHandler):
	cache = {}
	def stuff(self):
		try:
			print("CACHE: ", self.cache)
			username = self.get_argument("username");
			data = tornado.escape.json_decode(self.request.body)

			languages = data['languages']
			filters = data['filters']

			if username in self.cache:
				rank = self.cache[username]['rank-cache']
				user_info = self.cache[username]['info-cache']
			else:
				if len(self.cache) > 128: # simple way to clean the cache and don't fill the memory forever
					self.cache = {}
				man = manager.Manager(username)

				print("== languages ==")
				for l in languages:
					print(l)
					man.add_tech(l)

				print("== filters ==")
				for f in filters:
					print(f)
					man.add_filter(f['weight'], f['filter'])
				rank = man.rank()
				user_info = man.get_user_info()
				######CACHE DISABLED###self.cache[username]={'rank-cache':rank, 'info-cache':user_info}
			print("CACHE after response: ", self.cache)
			self.write({'rank': rank, 'details' : user_info})
		except tornado.web.MissingArgumentError as e:
			traceback.print_exc()
			self.write("missing argument(s): username")

	def get(self):
		return self.stuff()
	def post(self):
		return self.stuff()

def make_app():
	return tornado.web.Application([

		# Raking Endpoint
		(r"/api/rankuser", MainHandler),

		# Serve index.html on /
		(r"/()",tornado.web.StaticFileHandler, {"path": "./src/static/index.html"},),

		# Serve everthing inside static/ on /
		(r"/(.*)",tornado.web.StaticFileHandler, {"path": "./src/static"},),
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(PORT)
	print("Web Server running on port", PORT);
	tornado.ioloop.IOLoop.current().start()


