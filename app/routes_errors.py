from flask import render_template

def error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('/errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('/errors/403.html'), 403

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('/errors/500.html'), 500