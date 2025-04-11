# Installation/Deployment Documentation
A quick documentation on how to deploy the project locally and on a dedicated server (AWS EC2 as an example).

> [!NOTE]  
> This readme file won't cover instructions for gunicorn and nginx.

## Local (Visual Studio Code)
> [!IMPORTANT]  
> Prerequisite: Python 3 installed on the system.

- Clone the repo and open the folder in Visual Studio Code.

Execute the following commands in the VS terminal:
- `python -m venv venv`
- `venv\Scripts\activate`

> [!TIP]  
> If you're getting an error "running scripts is disabled on this system", execute this command:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

- `pip install flask`
- `pip install -r requirements.txt`
- `python create_env.py`
- `python create_db.py`
- `python run.py`

Now the app should be available locally on `http://127.0.0.1:5000`


## AWS EC2 and Docker
Execute the following commands in the given order

### Preparing the VM
- `sudo yum update -y`
- `sudo yum install docker -y`
- `sudo yum install git -y`

### Docker
- `sudo services docker start`
- `sudo usermod -a -G docker ec2-user`

### Repo
- `mkdir downloads`
- `cd downloads`
- `git clone http://github.com/NikitaEdin/SOC09109-2025-TR2-Group-Project.git .` _(with the dot at the end)_

### Dockerfile
- `sudo docker build -t ec2-drone:1.0 -f dockerfile .` _(with the dot at the end)_
- `sudo docker run -d -p 80:5000 ec-drone:1.0`

And now the instance should be running accessible via the EC2 public IP.

<hr>

### Other Notes
Check running dockers:
- `sudo docker ps`

Removing dockers:
- `sudo docker stop $(docker ps -q)`
- `sudo docker rm $(docker ps -a -q)`
- `sudo docker ps`


<hr>

## FAQ
Q: What are the default login credentials? <br>
A: They're listed in `create_db.py` script.

Q: Getting an error `Flask module is not recognised` - what do I do?<br>
A: Make sure you run `pip install flask` while in `venv`.

Q: How do I activate the virtual environment on the server?<br>
A: Run source `venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows).

Q: Getting `"ModuleNotFoundError"` after deployment - what do I do?<br>
A: Ensure all required packages are installed using `pip install -r requirements.txt`.

Q: Can I change the host port from `5000`? <br>
A: Yes, in `run.py` and in server deployment steps (if any).

Q: How can I transfer project files to EC2/VM server? <br>
A: Using the Git clone command or a third party software like [FileZilla](https://filezilla-project.org/). 

Q: What's the best way to serve Flask in production? <br>
A: Use `gunicorn` or `uWSGI` behind a reverse proxy like `Nginx` (beyond the scope of this project).

