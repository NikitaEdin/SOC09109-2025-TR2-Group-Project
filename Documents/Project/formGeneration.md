# Form Generation
The form generation system is constructed of 4 main pillars, which can be highly customised and expanded upon.

## How It Works
The 4 pillars of the form generations are:
- "Form base" layout.
- - Responsible for the consistent and structural page layout of every form.
- The form macros.
- - Generates the correct input based on the json field type and attributes.
- The JSON template.
- - The provided predefined form structure.
- The automated backend (verification and update).
- - Handles the form verification and database CRUD operation of updating the records.

### Form_Base
The form base layout (`form_main.html`) contains all the necessary dependencies for the form to be fully generated, including basic navigation and error messsages in case something goes wrong.


### Form Macros
The form macros (`form_macros.html`) file is responsible for converting the given field (such as a checkbox or a textfield) into a fully functioning input type, along with the correct ID and name attributes.

Additionally, the macro displays any field errors in case of a failed form submission.

### Adding New Types
Adding new types is easily done by adding another `else-if` statement with the name of the type.

```py
{% elif field.type == 'checkbox' %}
...
```
Followed by the visual representation of the object.

> [!NOTE]  
> More field specific attributes can be added via the JSON template, and won't cause conflicts/issues with existing form generation logic.

### JSON Templates
The JSON templates can be found in `app/forms/jsons`.

A simple example of a basic JSON is `preFlightTemplate.py`, which contains only checkboxes, categorised into multiple sections, each containing a text header.

A more complex example of a JSON template is `siteEvaluationTemplate.py`, which contains multiple field types, number of sections, along with optional items such as tooltips.

The mandatory attributes for each field are:
- `id` - The unique id (lowercase without spaces or digits).
- `name` - The displayed name in the form.
- `value` - The actual value of this field (keep it empty, used for saving/loading data).
- `type` - The type which determines how it's rendered.
- - Available types: `textarea`, `date`, `checkbox`, `text`.

The optional attributes for each field are:
- `required` - True or False
- `tooltip` - Brief description for the user.

> [!IMPORTANT]  
> For more information on the json templates, visit [JsonTemplates Documentation](/Documents/Project/jsonTemplates.md).


### Automated Backend

The backend logic for the generated form is all handled in the `handle_json_form_submission` method in `routes_forms.py`.

The method handles the form submission and updates the records in the database.

```py
# Util method to dynamically handle json form submission.
# And update corresponding attribute and db record.
def handle_json_form_submission(project, form_attr_name):
    form_data = getattr(project, form_attr_name)

    # Process  request
    if request.method == 'POST':
        for section in form_data[0]['form']['sections']:
            for field in section['fields']:
                field_id = field['id']
                field_value = request.form.get(field_id)
                field['value'] = field_value

        # Save changes
        setattr(project, form_attr_name, form_data)
        flag_modified(project, form_attr_name)
        db.session.add(project)
        db.session.commit()
        return True 
    return False  
```

<hr>

## Examples
A great example of the form generation system can be highlighted with how the `pre-flight` form is done.

The frontend (`pre_flight.html`) only contains the following:
```jinja
{% extends "base.html" %}
<!-- Utilise form macro for auto populating fields -->
{% import "forms/form_macros.html" as macros %}

{% block content %}
    <!-- For any errors -->
    {% include "shared/flash-message.html" %}

    <!-- Pass the used attribute(json) and auto-generate form -->
    {% set form_data=project.preFlight[0] %}
    {% include "forms/form_main.html" %}
       
{% endblock %}
```

The correct json template is simply passed into the form generation html, which handles all the front-end heavy-lifting logic.

And the backend route contains the following:
```py
@app.route("/project/<int:project_id>/pre-flight", methods=['GET', 'POST'])
@login_required
def pre_flight(project_id):
    project = Project.query.get_or_404(project_id)
    security(project)

    # Handle form submit (json from auto-gen form)
    if handle_json_form_submission(project, "preFlight"):
        flash('Changes saved successfully!', 'success')
        return redirect(url_for('project', project_id=project.id))

    return render_template('forms/pre_flight.html', title='Pre-Flight Actions', project=project)
```

This ensures the route code has the cleanest code and the easiest structure to understand and expand upon.