from django.db.models import Q


def user_can_edit_chants_in_source(user, source):
    """
    Checks if the user can edit Chants in a given Source.
    Used in ChantDetail, ChantList, ChantCreate, ChantDelete, ChantEdit,
    ChantEditSyllabification, and SourceDetail views.
    """
    if user.is_anonymous or (source is None):
        return False

    source_id = source.id
    user_is_assigned_to_source = user.sources_user_can_edit.filter(id=source_id)

    user_is_project_manager = user.groups.filter(name="project manager").exists()
    user_is_editor = user.groups.filter(name="editor").exists()
    user_is_contributor = user.groups.filter(name="contributor").exists()

    return (
        (user_is_project_manager)
        or (user_is_editor and user_is_assigned_to_source)
        or (user_is_editor and source.created_by == user)
        or (user_is_contributor and user_is_assigned_to_source)
        or (user_is_contributor and source.created_by == user)
    )


def user_is_proofreader(user):
    """
    Checks if the user is a proofreader.
    Used in UserSourceListView.
    """
    if user.groups.filter(Q(name="project manager") | Q(name="editor")).exists():
        return True
    return False


def user_can_proofread_chants_in_source(user, source_id):
    """
    Checks if the user can access the proofreading page of a given Source.
    Used in ChantProofreadView.
    """
    if user.is_anonymous:
        return False
    assigned_to_source = user.sources_user_can_edit.filter(id=source_id)

    is_project_manager = user.groups.filter(name="project manager").exists()
    is_editor = user.groups.filter(name="editor").exists()

    if (is_project_manager) or (is_editor and assigned_to_source):
        return True
    return False


def user_can_view_unpublished_source(user, source):
    """
    Checks if the user can view unpublished Sources or Chants/Sequences belonging
    to unpublished sources on the site.
    Used in ChantDetail, SequenceDetail, and SourceDetail views.
    """
    display_unpublished = user.is_authenticated
    if (
        (source is not None)
        and (source.published is False)
        and (not display_unpublished)
    ):
        return False
    return True


def user_can_edit_sequence(user):
    """
    Checks if the user has permission to edit a Sequence object.
    Used in SequenceDetail and SequenceEdit views.
    """
    is_project_manager = user.groups.filter(name="project manager").exists()

    if is_project_manager:
        return True
    return False


def user_can_create_source(user):
    """
    Checks if the user has permission to create a Source object.
    Used in SourceCreateView.
    """

    is_authorized = user.groups.filter(
        Q(name="project manager") | Q(name="editor") | Q(name="contributor")
    ).exists()

    if is_authorized:
        return True
    return False


def user_can_edit_source(user, source):
    """
    Checks if the user has permission to edit a Source object.
    Used in SourceDetail, SourceEdit, and SourceDelete views.
    """
    if user.is_anonymous:
        return False
    source_id = source.id
    assigned_to_source = user.sources_user_can_edit.filter(id=source_id)

    is_project_manager = user.groups.filter(name="project manager").exists()
    is_editor = user.groups.filter(name="editor").exists()
    is_contributor = user.groups.filter(name="contributor").exists()

    if (
        (is_project_manager)
        or (is_editor and assigned_to_source)
        or (is_editor and source.created_by == user)
        or (is_contributor and source.created_by == user)
    ):
        return True
    return False


def user_can_view_user_detail(viewing_user, user):
    """
    Checks if the user can view the user detail pages of regular users in the database or just indexers.
    Used in UserDetailView.
    """
    if viewing_user.is_authenticated or user.is_indexer:
        return True
    return False


def user_can_manage_source_editors(user):
    """
    Checks if the user has permission to change the editors assigned to a Source.
    Used in SourceDetailView.
    """
    if user.is_staff or user.groups.filter(name="project manager").exists():
        return True
    return False
