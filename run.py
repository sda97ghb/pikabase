import subprocess


def run_sync(command):
    subprocess.run(command.split())


def run_async(command):
    subprocess.Popen(command.split())


def main():
    run_async("python manage.py rundramatiq")
    run_sync("gunicorn -b 0.0.0.0:8080 project.wsgi")


if __name__ == '__main__':
    main()
