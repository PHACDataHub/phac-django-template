import random

from django.contrib.auth.models import Group
from django.db import transaction

from proj.models import User

from my_app.constants import ADMIN_USER_GROUP
from my_app.model_factories import ProjectFactory, ProjectTaskFactory
from my_app.models import Project


@transaction.atomic
def run():
    admin_group = Group.objects.get_or_create(name=ADMIN_USER_GROUP)[0]

    admin = User.objects.create_superuser(
        username="admin",
        password="admin",
    )
    admin.groups.add(admin_group)

    u1 = User.objects.create_user(
        username="billy.bob",
        password="billy.bob",
    )
    u2 = User.objects.create_user(
        username="rilly.rob",
        password="rilly.rob",
    )
    u3 = User.objects.create_user(
        username="silly.sob",
        password="silly.sob",
    )
    u4 = User.objects.create_user(
        username="dilly.dob",
        password="dilly.dob",
    )
    users = {u1, u2, u3, u4}

    for _x in range(1, 10):
        proj = ProjectFactory()

        leader = random.choice(users)
        proj.add_user(leader, Project.LEADER_ROLE)

        contributor = random.choice(users - {leader})
        proj.add_user(contributor, Project.CONTRIBUTOR_ROLE)

        spectator = random.choice(users - {leader, contributor})
        proj.add_user(spectator, Project.SPECTATOR_ROLE)

        for x in range(1, random.randint(0, 4)):
            ProjectTaskFactory(project=proj)
