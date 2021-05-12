import os
import signal
import subprocess
import sys
import time
from jinja2 import Environment, FileSystemLoader, select_autoescape
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

###############
# JINJA BUILD #
###############

def ls(path, ignore=[]):
    names = subprocess.run(
        ["ls", path],
        capture_output=True
    ).stdout.decode('utf-8').split('\n')
    return [n for n in names if n != "" and n not in ignore]

def render_page(env, page):
    html = env.get_template(page).render()
    f = open("dist/"+page, "w")
    f.write(html)
    f.close()

def jinja():
    env = Environment(
        loader=FileSystemLoader(
            ["src/", "theme/templates/"]),
        autoescape=select_autoescape(["html", "xml"]),
        auto_reload=True
    )
    pages = ls("src/")
    for page in pages:
        render_page(env, page)
    print("Jinja Built")

# Copy Files and Images
def files_and_images():
    os.system("cp -r assets/img dist/assets/img")
    os.system("cp assets/img/favicon.ico dist/")
    os.system("cp assets/img/favicon.png dist/")

# Prod Assets
def assets_prod():
    if os.path.exists("dist/assets"):
        os.system("rm -r dist/assets/*")
    else:
        os.makedirs("dist/assets")
    files_and_images()
    os.system(
        "npx sass --load-path=node_modules assets/style.scss dist/assets/style.css")
    os.system("npx sass --load-path=node_modules assets/scss:dist/assets/css")
    os.system("npx postcss -u autoprefixer -r dist/assets/**/*.css")
    os.system("cp -r assets/js dist/assets/js")
    os.system("cp assets/script.js dist/assets/script.js")
    os.system("npx browserify -p tinyify assets/bundle.js -o dist/assets/bundle.js")
    # If I need a single-page import, make bundle-page.js in assets/js to go with page.js
    #scripts = ls("assets/js")
    #for s in scripts:
    #    os.system("npx browserify assets/js/{} -o dist/assets/js/{}".format(s, s))
    print("Assets Copied\n")

# Faster Dev Assets
def assets_dev():
    if os.path.exists("dist/assets"):
        os.system("rm -r dist/assets/*")
    else:
        os.makedirs("dist/assets")
    files_and_images()
    os.system(
        "sass --load-path=node_modules assets/style.scss dist/assets/style.css")
    os.system("sass --load-path=node_modules assets/scss:dist/assets/css")
    os.system("npx postcss -u autoprefixer -r dist/assets/**/*.css")
    os.system("cp -r assets/js dist/assets/js")
    os.system("cp assets/script.js dist/assets/script.js")
    os.system("npx browserify assets/bundle.js -o dist/assets/bundle.js")
    print("Assets Copied\n")

def clean_dist():
    if os.path.exists("dist"):
        os.system("rm -r dist/*")
    else:
        os.makedirs("dist")

###############
# LIVE RELOAD #
###############

class Watcher:

    def __init__(self, directory=".", handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self):
        self.observer.schedule(
            self.handler, self.directory, recursive=True)
        self.observer.start()
        print("Watcher Running in {}/".format(self.directory))
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated")


class PKCHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        if event.is_directory or "/dist/" in event.src_path:
            return None
        elif "/assets/" in event.src_path:
            assets_dev()
        else:
            jinja()


##################
# NETLIFY DEPLOY #
##################

def build_site(prod):
    clean_dist()
    jinja()
    if prod:
        assets_prod()
    else:
        assets_dev()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: `python build.py --dev` or `python build.py --prod`")
        exit
    elif sys.argv[1] == "--prod":
        build_site(prod=True)
        print("pkandc.com Built")
    elif sys.argv[1] == "--dev":
        print("Initializing pkandc.com")
        src_watcher = Watcher(".", PKCHandler())
        build_site(prod=False)
        server_proc = subprocess.Popen(["netlify", "dev"])
        src_watcher.run()
        if server_proc.pid:
            os.kill(server_proc.pid, signal.SIGTERM)
    else:
        print("Usage: `python build.py --dev` or `python build.py --prod`")
        exit
