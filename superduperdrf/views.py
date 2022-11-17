import re

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.static import serve


@login_required
def protected_serve(
    request, path, document_root=None, show_indexes=False, *args, **kwargs
):
    # _user = request.user
    # # Eg: http://.../media/attachements/1001/_-name.ext
    # _search = re.search(r"([\d\.-]+)", path)

    # # Eg: http://.../media/attachements/team/{team_id}/_.ext
    # _team_url = re.search(r"\bteams\b", path)

    # # Eg: http://.../media/images/_.ext
    # _profile_url = re.search(r"\bimages\b", path)
    # if _team_url:
    #     return serve(request, path, document_root, show_indexes)
    # elif _profile_url:
    #     return serve(request, path, document_root, show_indexes)
    # elif _search:
    #     try:
    #         # ! if there's anything that `re` got wrong
    #         _project_id = int(_search.group())
    #         _project = Project.objects.select_related("team").get(pk=_project_id)
    #         if (
    #             not _project.team.organization.is_approver_in_any_team(_user)
    #             or _project.status == "N"
    #         ):
    #             raise Exception
            return serve(request, path, document_root, show_indexes)
        # except (ValueError, Project.DoesNotExist, Exception):
            # raise Http404
    # else:
        # raise Http404
