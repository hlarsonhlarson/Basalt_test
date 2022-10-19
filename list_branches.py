import requests
import json

from environment_variables import url,method
from package_manager import group_by_arch_field, diff_of_packages, show_latest_version


def request_data(branches):
	res = []
	for branch in branches:
		branch_url = f'{url}{method}{branch}'
		tmp = requests.get(branch_url)
		if tmp.status_code == 200:
			res.append((branch,tmp.json()['packages']))
		else:
			res.append(None)
	return res

def assign_output_to_branch(res, branches):
	if res[0][0] == branches[0]:
		sisyph = res[0][1]
		p10 = res[1][1]
	else:
		sisyph = res[1][1]
		p10 = res[0][1]
	return sisyph, p10

def get_list_compare_branches():
	branches = ['sisyphus','p10']
	res = request_data(branches)
	if not res or len(res) != 2 or not res[0] or not res[1]:
		return 'Can\'t get information from API'

	sisyph, p10 = assign_output_to_branch(res, branches)

	sisyph_groups, sisyph_packages_info = group_by_arch_field(sisyph)
	p10_groups, p10_packages_info = group_by_arch_field(p10)

	diff1 = diff_of_packages(sisyph_groups, sisyph_packages_info,
								p10_groups, p10_packages_info)
	diff2 = diff_of_packages(p10_groups, p10_packages_info,
							sisyph_groups,sisyph_packages_info)

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