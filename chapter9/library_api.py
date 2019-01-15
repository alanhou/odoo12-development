from xmlrpc import client

class LibraryAPI():
	def __init__(self, srv, port, db, user, pwd):
		common = client.ServerProxy(
			'http://%s:%d/xmlrpc/2/common' % (srv, port))
		self.api = client.ServerProxy(
			'http://%s:%d/xmlrpc/2/object' % (srv, port))
		self.uid = common.authenticate(db, user, pwd, {})
		self.pwd = pwd
		self.db = db
		self.model = 'library.book'

	def execute(self, method, arg_list, kwarg_dict=None):
		return self.api.execute_kw(
			self.db, self.uid, self.pwd, self.model,
			method, arg_list, kwarg_dict or {})

	def search_read(self, text=None):
		domain = [('name', 'ilike', text)] if text else []
		fields = ['id', 'name']
		return self.execute('search_read', [domain, fields])

	def create(self, title):
		vals = {'name': title}
		return self.execute('create', [vals])

	def write(self, title, id):
		vals = {'name': title}
		return self.execute('write', [[id], vals])

	def unlink(self, id):
		return self.execute('unlink', [[id]])

if __name__ == '__main__':
	# 测试配置
	srv, db, port = '192.168.16.161', 'dev12', 8069
	user, pwd = 'admin', 'admin'
	api = LibraryAPI(srv, port, db, user, pwd)
	from pprint import pprint
	pprint(api.search_read())