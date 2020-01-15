from unittest.mock import MagicMock
from test.integrationtests.skills.skill_tester import SkillTest

def test_runner(skill, example, emitter, loader):
	# get the skill class instance
	_skillobj = next(s for s in loader.skills if s and s.root_dir == skill)

	# setup mock data
	_list_projects = [
		{
			'id': 1,
			'name': 'Target',
			'parent_id': _skillobj.parent_project_id
		},
		{
			'id': 2,
			'name': 'Giant Eagle',
			'parent_id': _skillobj.parent_project_id
		}
	]

	# replace the Todoist API with a mock
	_skillobj.todoist_api = MagicMock(state={'projects': _list_projects})

	return SkillTest(skill, example, emitter).run(loader)