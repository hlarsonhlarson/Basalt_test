import requests
import asyncio
import pandas as pd
import json
from time import time


url = 'https://rdb.altlinux.org/api/'
method = 'export/branch_binary_packages/'

'''
async def branch_list(branch_url):
	ans = requests.get(branch_url)
	if ans.status_code == 200:
		return (branch_url.split('/')[-1],ans.json())
	return None
	
async def all_branches_list(branches):
	tasks = []
	for branch in branches:
		branch_url = f'{url}{method}{branch}'
		tasks.append(branch_list(branch_url))
	return asyncio.gather(*tasks)
'''

def simple_run(branches):
	res = []
	for branch in branches:
		branch_url = f'{url}{method}{branch}'
		tmp = requests.get(branch_url)
		if tmp.status_code == 200:
			res.append((branch,tmp.json()['packages']))
		else:
			res.append(None)
	return res

def group_by_arch_field(branch_list):
	groups = dict()
	packages_info = dict()
	for elem in branch_list:
		version = elem['arch']
		if version not in groups:
			groups[version] = []
		groups[version].append(elem['name'])
		packages_info[f"{version}_{elem['name']}"] = elem
	return groups, packages_info

def diff_of_packages(group1, info_group1,group2, info_group2):
	version_diff = dict()
	for version in group1:
		group1_packages = set(group1[version])
		group2_packages = set()
		if version in group2:
			group2_packages = set(group2[version])
		remaining_packages = group1_packages - group2_packages
		version_diff[version] = [info_group1[f'{version}_{x}'] for x in remaining_packages]
	return version_diff

def show_latest_version(group1,info_group1,group2,info_group2):
	latest_package_info = []
	for version in group1:
		group1_packages = set(group1[version])
		group2_packages = set()
		if version in group2:
			group2_packages = set(group2[version])
		common_packages = group1_packages & group2_packages
		for package in common_packages:
			pack1 = info_group1[f'{version}_{package}']
			pack2 = info_group2[f'{version}_{package}']
			if pack1['version']+pack1['release'] > pack2['version']+pack2['release']:
				latest_package_info.append(pack1)
	return latest_package_info

def get_list_compare_branches():
	branches = ['sisyphus','p10']
	#res = asyncio.run(all_branches_list(branches))
	res = simple_run(branches)
	if len(res) != 2 or not res[0] or not res[1]:
		return 'Can\'t get information from API'
	if res[0][0] == branches[0]:
		sisyph = res[0][1]
		p10 = res[1][1]
	else:
		sisyph = res[1][1]
		p10 = res[0][1]
	sisyph_groups, sisyph_packages_info = group_by_arch_field(sisyph)
	p10_groups, p10_packages_info = group_by_arch_field(p10)
	diff1 = diff_of_packages(sisyph_groups, sisyph_packages_info, p10_groups, p10_packages_info)
	diff2 = diff_of_packages(p10_groups, p10_packages_info, sisyph_groups,sisyph_packages_info)
	latest_versions = show_latest_version(sisyph_groups,
						sisyph_packages_info,
						p10_groups,
						p10_packages_info)
	result_dict = {f'Extra packages {branches[0]}': diff1,
			f'Extra packages {branches[1]}': diff2,
			f'Latest packages {branches[0]}': latest_versions
}
	return json.dumps(result_dict,indent=4) 



if __name__ == '__main__':
	print(get_list_compare_branches())
