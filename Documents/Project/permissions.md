# Permissions and Decorators
This documentation file highlights how user permissions work within the Flight Project system, and how "Flask decorators" are used to enforce access control and authorisation.

## Permissions
Within the Flight Project system, access to projects is managed through a structured permissions model based on user roles and ownership.

### Project Creators
Users who create a Flight Project are automatically granted full read/write permissions, as they fully own the project.

This includes the ability to:
 - Edit project details, forms, checklist.
 - Upload and delete files.
 - Manage access for other pilots/users for that project.

### Admin Users
Users with Admin privileges have unrestricted access across the platform. <br>
This includes full read/write access to all projects created by other users.

Admins may:
- View and modify other users' projects.
- Override permission settings where necessary.

### Shared Project Users
Project authors/creators can share their projects with other users, such projects are called "shared projects" with those users.

Shared users are granted:
- Read-only access to the project.
- No permission to:
- - Upload files.
- - Edit project details, forms, checklist.
- - Manage project access.

<hr>

## Decorators
To enforce an additional layer of permissions and user authentication in the backend of the Flask routes, decorators are utilised.

### 'login_required' Decorator
A decorator provided by Flask, the `login_required` ensures that the user is authenticated before they can access a given route.

> [!TIP]  
> The default login view can be adjusted in `__init__.py` at this line: `login_manager.login_view = 'login'`.

This is commonly used for any route that needs the user to be authenticated, for example (in `routes_dashboard.py`): 
```python
# The main/home page of the dashboard.
@app.route("/dashboard")
@login_required
def dashboard():
    # User projects
    projects = current_user.get_projects()
```

> [!IMPORTANT]  
> If the user attempts to access such a route while being unauthenticated - they will be redirected to the login page.



### 'admin_required' Decorator
This is a custom decorator (`decorators.py`) used to protect admin-only routes, such as the admin dashboard.<br>
This additional layer of security simplifies the two constant checks of both authenticated and authorised as admin role. <br>

Commonly used for configuration and system-level management, for example:
```python
@app.route("/admin/users/delete/<int:user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    ...
```


> [!IMPORTANT]  
> If the user attempts to access such route while being unauthorised for admin permissions - they will receive the 403 error (access denied).

<hr>

## Custom Decorators Example
Custom decorators can be easily added in order to improve the efficiency of the routes, reducing repeating checks, and adding an extra layer of security.

For example, `project_owner_required` decorator:
```python
def project_owner_required(f):
    @wraps(f)
    def decorated_function(project_id, *args, **kwargs):
        project = get_project_by_id(project_id)
        if not project.is_owner(current_user):
            flash("You do not have permission to access this project.", "danger")
            return redirect(url_for('projects'))
        return f(project_id, *args, **kwargs)
    return decorated_function
```

Which can be added to the edit_project route:
```python
@app.route("/project/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
@project_owner_required
def edit_project(project_id):
    # Fetch project by ID
    project = Project.query.get_or_404(project_id)
```