import flask
from webapp.api.github import GitHub
from webapp.decorators import login_required
from werkzeug.exceptions import Unauthorized

publisher_github = flask.Blueprint(
    "github", __name__, template_folder="/templates", static_folder="/static"
)


@publisher_github.route("/publisher/github/get-repos", methods=["GET"])
@login_required
def get_repos():
    github = GitHub(flask.session.get("github_auth_secret"))
    org = flask.request.args.get("org")

    try:
        if org:
            repos = github.get_org_repositories(org)
        else:
            repos = github.get_user_repositories()
    except Unauthorized:
        return (
            flask.jsonify({"error": "You need to be authenticated on GitHub"}),
            401,
        )

    return flask.jsonify(repos)
