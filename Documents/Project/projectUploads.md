# Project File Upload & Management
This documentation explains how file uploads work on the platform.<br>
Allowing users to upload and manage files within each project.


## Customisation
The file uploading system can be customised allowing the developer to adjust the number of allowed files per project, allowed file extensions, along with the maximum size per file.

All of the backend for the file uploading is located in `routes_new_project.py`, where the developer can adjust the following settings to suit their corresponding system and client needs.

```py
UPLOAD_FOLDER = 'uploads/'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'csv', 'ppt', 'pptx', 'txt', 'png', 'jpg', 'jpeg'}
MAX_FILES_PER_PROJECT = 10
```

> [!IMPORTANT]  
> The current code limits the system to 100MB per project in order to save space, but this can be easier adjusted.

## Database Metadata
Once a new file is uploaded to the server, its metadata is stored in `ProjectFile` table, which you can read more about in the [database diagram](/Documents/Database%20Design/Database%20Design.pdf).

Each file record in the database contains the following information:
- `id`: unique indentification number for each file.
- `original_filename`: the original filename upon upload.
- `filename`: the new filename used for server-side storage.
- `filepath`: full path to the file on the server.
- `size`: size of the file in bytes.
- `uploaded_at`: date of which the file was uploaded/modified.
- `project_id`: reference to the associated project.

> [!IMPORTANT]  
> A file with the same name (in the same project) will overwrite with the existing file and record - by design.

## File Storage
The uploaded files are stored on the server with a unique pattern to prevent potential file overlapping instances across multiple projects in case the same named file is uploaded across multiple projects.

The naming scheme as follows:

`<ProjectID>_<UUID>_<filename>`

- `ProjectID`: represents the associated project numeric id.
- `UUID`: unique identifier (128-bit) in hexademical form.
- `filename`: the original filename.

Code snippet:
```py
unique_filename = f"{project_id}_{uuid.uuid4().hex}_{original_filename}"
```

### Example
If the original filename is `myImage.jpg` is uploaded to a project id `123`, the new and unique filename is `123_9c56f5e8f36f47509f4d8e6f340bcd52_myImage.jpg`.

> [!TIP]
> This is done for security reasons to prevent unauthorised users from brute forcing attacks.