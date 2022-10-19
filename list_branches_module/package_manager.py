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
