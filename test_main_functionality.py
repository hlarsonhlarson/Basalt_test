import unittest
from list_branches import group_by_arch_field, diff_of_packages, show_latest_version

class Test(unittest.TestCase):
	def test_comparing(self):
		inp1 = [
			{'name': 'first_package', 'version': '2.0.0', 'release': 'alt', 'arch': 'qwe'},
			{'name': 'second_package', 'version': '3.0.0', 'release': 'alt1', 'arch': 'qwe'},
			{'name': 'third_package', 'version': '4.0.0', 'release': 'alt2', 'arch': 'qwe2'},
			{'name': 'fith_package', 'version': '4.0.0', 'release': 'alt2', 'arch': 'qwe2'},
			{'name': 'first_package', 'version': '4.0.0', 'release': 'alt2', 'arch': 'qwe3'}
			]
		inp2 = [
			{'name': 'first_package', 'version': '3.0.0', 'release': 'alt', 'arch': 'qwe'},
			{'name': 'second_package', 'version': '3.0.1', 'release': 'alt1', 'arch': 'qwe'},
			{'name': 'third_package', 'version': '4.0.0', 'release': 'alt2', 'arch': 'qwe2'},
			{'name': 'sixth_package', 'version': '4.0.0', 'release': 'alt2', 'arch': 'qwe2'},
			]
		names1,info1 = group_by_arch_field(inp1)
		names2,info2 = group_by_arch_field(inp2)
		tmp_res = {
			'qwe2': [{'name': 'fith_package', 'version': '4.0.0', 'release': 'alt2', 'arch': 'qwe2'}],
			'qwe': [],
			'qwe3': [{'name': 'first_package', 'version': '4.0.0', 'release': 'alt2', 'arch': 'qwe3'}
			]}
		self.assertEquals(diff_of_packages(names1,info1,names2,info2),tmp_res)
		tmp_res = {'qwe': [],
			   'qwe2': [{'name': 'sixth_package', 'version': '4.0.0', 'release': 'alt2', 'arch': 'qwe2'}]
			  }

		self.assertEquals(diff_of_packages(names2,info2,names1,info1),tmp_res)
	def test_latest(self):
		inp1 = [
			{'name': 'first_package', 'version': '2.0.0', 'release': 'alt', 'arch': 'qwe'},
			{'name': 'second_package', 'version': '3.0.1', 'release': 'alt1', 'arch': 'qwe'},
			{'name': 'third_package', 'version': '4.0.0', 'release': 'alt2', 'arch': 'qwe2'},
			{'name': 'fith_package', 'version': '4.0.0', 'release': 'alt2', 'arch': 'qwe2'},
			{'name': 'first_package', 'version': '4.0.0', 'release': 'alt2', 'arch': 'qwe3'}
			]
		inp2 = [
			{'name': 'first_package', 'version': '3.0.0', 'release': 'alt', 'arch': 'qwe'},
			{'name': 'second_package', 'version': '3.0.0', 'release': 'alt1', 'arch': 'qwe'},
			{'name': 'third_package', 'version': '4.0.0', 'release': 'alt2', 'arch': 'qwe2'},
			{'name': 'sixth_package', 'version': '4.0.0', 'release': 'alt2', 'arch': 'qwe2'},
			]
		names1,info1 = group_by_arch_field(inp1)
		names2,info2 = group_by_arch_field(inp2)
		tmp_res = [{'name': 'second_package', 'version': '3.0.1', 'release': 'alt1', 'arch': 'qwe'}]
		self.assertEquals(show_latest_version(names1,info1,names2,info2),tmp_res)
