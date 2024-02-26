from django.test.client import Client
from django.urls import reverse

# creating a variable called test_rules triggers pytest to run it as a test! annoying!
from phac_aspc.rules import patch_rules
from phac_aspc.rules import test_rule as my_test_rule

from proj.models import User

from my_app.model_factories import ProjectFactory
from my_app.services import (
    set_project_contributor,
    set_project_leader,
    set_project_spectator,
)


def test_admin_has_all_access(admin_user):
    assert my_test_rule("is_admin", admin_user)

    p = ProjectFactory()
    assert my_test_rule("can_view_project", admin_user, p.id)
    assert my_test_rule("can_modify_project", admin_user, p.id)


def test_leader_role():
    leader = User.objects.create()
    proj = ProjectFactory()
    other_proj = ProjectFactory()
    set_project_leader(proj, leader)

    assert not my_test_rule("is_admin", leader)
    assert my_test_rule("is_project_leader", leader, proj.id)
    assert not my_test_rule("is_project_leader", leader, other_proj.id)
    assert my_test_rule("can_view_project", leader, proj.id)
    assert my_test_rule("can_modify_project", leader, proj.id)
    assert not my_test_rule("can_view_project", leader, other_proj.id)
    assert not my_test_rule("can_modify_project", leader, other_proj.id)


def test_contributor_role():
    u = User.objects.create()
    proj = ProjectFactory()
    other_proj = ProjectFactory()
    set_project_contributor(proj, u)

    assert not my_test_rule("is_admin", u)
    assert not my_test_rule("is_project_leader", u, proj.id)
    assert my_test_rule("is_project_contributor", u, proj.id)
    assert not my_test_rule("is_project_contributor", u, other_proj.id)
    assert my_test_rule("can_view_project", u, proj.id)
    assert my_test_rule("can_modify_project_tasks", u, proj.id)
    assert not my_test_rule("can_modify_project_tasks", u, other_proj.id)
    assert not my_test_rule("can_view_project", u, other_proj.id)


def test_spectator_role():
    u = User.objects.create()
    proj = ProjectFactory()
    other_proj = ProjectFactory()
    set_project_spectator(proj, u)

    assert not my_test_rule("is_admin", u)
    assert not my_test_rule("is_project_leader", u, proj.id)
    assert not my_test_rule("is_project_contributor", u, proj.id)
    assert my_test_rule("is_project_spectator", u, proj.id)
    assert not my_test_rule("is_project_spectator", u, other_proj.id)
    assert my_test_rule("can_view_project", u, proj.id)
    assert not my_test_rule("can_modify_project_tasks", u, proj.id)


def check_user_has_preview_access(user, project_id):
    client = Client()
    client.force_login(user)
    resp = client.get(reverse("preview_project_modal", args=[project_id]))
    return resp.status_code == 200


def check_user_can_use_modify_view(user, project_id):
    client = Client()
    client.force_login(user)
    resp = client.get(reverse("edit_project", args=[project_id]))
    return resp.status_code == 200


def test_views_use_rules_via_mocks():
    u = User.objects.create()
    proj = ProjectFactory()

    with patch_rules(can_modify_project=True):
        assert check_user_can_use_modify_view(u, proj.id)

    with patch_rules(can_modify_project=False):
        assert not check_user_can_use_modify_view(u, proj.id)

    with patch_rules(can_view_project=True):
        assert check_user_has_preview_access(u, proj.id)

    with patch_rules(can_view_project=False):
        assert not check_user_has_preview_access(u, proj.id)
