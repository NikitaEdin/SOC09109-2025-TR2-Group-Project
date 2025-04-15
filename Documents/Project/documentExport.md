# Documentation Export

This file documents how the 'export document' functionality works on the site, and includes advisories should it be extended.

There are 2 key files as part of this feature:
- [templates/forms/export.html](../../app/templates/forms/export.html) - This file includes the printable template for exporting a json object
- [routes_forms.py](../../app/routes_forms.py) - This file includes the routes for exporting a document. You can ctrl-f to find all endpoints that end with '/export'. Currently that is these ones:
  - [Viability study endpoint](../../app/routes_forms.py#L73-L82)
  - [Site evaluation endpoint](../../app/routes_forms.py#L132-L142)

> [!NOTE]  
>  We didn't get time to add everything, but it is easy to add the rest. See the [creating an export endpoint](#creating-an-export-endpoint) section below on how to add more.

## Export logic

There are two ways for a user to trigger an export:

The first is by navigating directly to the url and pressing 'Save Document', e.g. if the user bookmarked the link in the field.

The second is by clicking the export button for a specific document on the project page. Doing it the second way will auto prompt the browser's save page dialog.

Both of these users end in selecting 'Save to PDF' in the save dialog and downloading the page.

## Export template

The [export template](../../app/templates/forms/export.html) is very similar to the form template, but is readonly and has styles to be printed. It includes a navbar and other control buttons that are hidden to the print menu via the `no-print` and `print-only` CSS classes.

Currently, it supports only a few field types, but it may be necessary to add more in the future. These are:
- `text`
- `textarea`
- `date`

It may be wise to implement things like `checkbox` or even simplify it to render all unknown types like a regular `text` field. To add more, add a new `elif` statement on [line 73](../../app/templates/forms/export.html#L73) of export.html

The export template has JavaScript at the bottom of the file that facilitates user interaction. It reacts to clicking the 'Save Document' button by showing the browser print dialog. It also checks to see if there is a `auto_open` query parameter, and if so, opens the print dialog immediately. Setting this to `false` will not prevent the print dialog from opening on load, the parameter must be omitted entirely.

`auto_open` is set in every export link in the project page, so make sure to include it in any new export links you add.

## Creating an export endpoint

To add a new form export endpoint, edit the following code to match the form name for the endoint and add it to [routes_forms.py](../../app/routes_forms.py):

```py
@app.route("/project/<int:project_id>/formname/export", methods=["GET"])
@login_required
def export_viability_study(project_id):
    project = Project.query.get_or_404(project_id)
    security(project)

    creator = project.get_author()
    allowed_users = project.allowed_users

    return render_template("/forms/export.html", form_data=project.form_name, title="Form Name", creator=creator, allowedUsers=allowed_users)
```

The `form_data` variable should be passed a JSON object that follows the structure outlined in the [JSON templates](./jsonTemplates.md) document.
