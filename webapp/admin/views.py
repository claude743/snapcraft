# Packages
import json
import flask
from canonicalwebteam.store_api.exceptions import (
    StoreApiError,
    StoreApiResponseErrorList,
)
from canonicalwebteam.store_api.stores.snapstore import SnapStoreAdmin
from webapp.api.exceptions import ApiError
from webapp.decorators import login_required

# Local
from webapp.helpers import api_publisher_session
from webapp.publisher.views import _handle_error, _handle_error_list

admin_api = SnapStoreAdmin(api_publisher_session)

admin = flask.Blueprint(
    "admin", __name__, template_folder="/templates", static_folder="/static"
)


@admin.route("/admin")
@login_required
def get_stores():
    """
    In this view we get all the stores the user is an admin or we show a 403
    """
    try:
        stores = admin_api.get_stores(flask.session)
    except StoreApiResponseErrorList as api_response_error_list:
        return _handle_error_list(api_response_error_list.errors)
    except (StoreApiError, ApiError) as api_error:
        return _handle_error(api_error)

    if not stores:
        flask.abort(403)

    # We redirect to the first store snap list
    return flask.redirect(
        flask.url_for(".get_store_snaps", store_id=stores[0]["id"])
    )


@admin.route("/admin/<store_id>/snaps")
@login_required
def get_store_snaps(store_id):
    try:
        stores = admin_api.get_stores(flask.session)
        store = admin_api.get_store(flask.session, store_id)
        snaps = admin_api.get_store_snaps(flask.session, store_id)
    except StoreApiResponseErrorList as api_response_error_list:
        return _handle_error_list(api_response_error_list.errors)
    except (StoreApiError, ApiError) as api_error:
        return _handle_error(api_error)

    return flask.render_template(
        "admin/snaps.html", stores=stores, store=store, snaps=snaps
    )


@admin.route("/admin/<store_id>/members")
@login_required
def get_members(store_id):
    try:
        stores = admin_api.get_stores(flask.session)
        store = admin_api.get_store(flask.session, store_id)
        members = admin_api.get_store_members(flask.session, store_id)
    except StoreApiResponseErrorList as api_response_error_list:
        return _handle_error_list(api_response_error_list.errors)
    except (StoreApiError, ApiError) as api_error:
        return _handle_error(api_error)

    return flask.render_template(
        "admin/members.html", stores=stores, store=store, members=members
    )


@admin.route("/admin/<store_id>/members/manage")
@login_required
def get_manage_members(store_id):
    try:
        stores = admin_api.get_stores(flask.session)
        store = admin_api.get_store(flask.session, store_id)
        members = admin_api.get_store_members(flask.session, store_id)
    except StoreApiResponseErrorList as api_response_error_list:
        return _handle_error_list(api_response_error_list.errors)
    except (StoreApiError, ApiError) as api_error:
        return _handle_error(api_error)

    return flask.render_template(
        "admin/manage_members.html",
        stores=stores,
        store=store,
        members=members,
    )


@admin.route("/admin/<store_id>/members/manage", methods=["POST"])
@login_required
def post_manage_members(store_id):
    members = json.loads(flask.request.form.get("members"))

    try:
        admin_api.update_store_members(flask.session, store_id, members)
        flask.flash("Changes saved", "positive")
    except StoreApiResponseErrorList as api_response_error_list:
        msgs = [
            f"{error.get('message', 'An error occurred')}"
            for error in api_response_error_list.errors
        ]

        for msg in msgs:
            flask.flash(msg, "negative")
    except (StoreApiError, ApiError) as api_error:
        return _handle_error(api_error)

    return flask.redirect(
        flask.url_for(".get_manage_members", store_id=store_id)
    )


@admin.route("/admin/<store_id>/members/invite", methods=["POST"])
@login_required
def post_invite_members(store_id):
    members = json.loads(flask.request.form.get("members"))

    try:
        admin_api.invite_store_members(flask.session, store_id, members)
        flask.flash("Changes saved", "positive")
    except StoreApiResponseErrorList as api_response_error_list:
        msgs = [
            f"{error.get('message', 'An error occurred')}"
            for error in api_response_error_list.errors
        ]

        for msg in msgs:
            flask.flash(msg, "negative")
    except (StoreApiError, ApiError) as api_error:
        return _handle_error(api_error)

    return flask.redirect(
        flask.url_for(".get_manage_members", store_id=store_id)
    )


@admin.route("/admin/<store_id>/settings")
@login_required
def get_settings(store_id):
    try:
        stores = admin_api.get_stores(flask.session)
        store = admin_api.get_store(flask.session, store_id)
    except StoreApiResponseErrorList as api_response_error_list:
        return _handle_error_list(api_response_error_list.errors)
    except (StoreApiError, ApiError) as api_error:
        return _handle_error(api_error)

    return flask.render_template(
        "admin/settings.html", stores=stores, store=store
    )


@admin.route("/admin/<store_id>/settings", methods=["POST"])
@login_required
def post_settings(store_id):
    settings = {}
    settings["private"] = not flask.request.form.get("is_public")
    settings["manual-review-policy"] = flask.request.form.get(
        "manual-review-policy"
    )

    try:
        admin_api.change_store_settings(flask.session, store_id, settings)
        flask.flash("Changes saved", "positive")
    except StoreApiResponseErrorList as api_response_error_list:
        msgs = [
            f"{error.get('message', 'An error occurred')}"
            for error in api_response_error_list.errors
        ]

        for msg in msgs:
            flask.flash(msg, "negative")
    except (StoreApiError, ApiError) as api_error:
        return _handle_error(api_error)

    return flask.redirect(flask.url_for(".get_settings", store_id=store_id))


@admin.route("/admin/<store_id>/models")
@login_required
def get_models(store_id):
    try:
        stores = admin_api.get_stores(flask.session)
        store = admin_api.get_store(flask.session, store_id)
    except StoreApiResponseErrorList as api_response_error_list:
        return _handle_error_list(api_response_error_list.errors)
    except (StoreApiError, ApiError) as api_error:
        return _handle_error(api_error)

    return flask.render_template(
        "admin/models.html",
        stores=stores,
        store=store,
        models=[],
    )
