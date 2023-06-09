from logging import FileHandler, StreamHandler, INFO, basicConfig, error as log_error, info as log_info
from os import path as ospath, environ
from subprocess import run as srun
from pymongo import MongoClient
from dotenv import load_dotenv
from subprocess import run as srun

if ospath.exists('botlog.txt'):
    with open('botlog.txt', 'r+') as f:
        f.truncate(0)

basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[FileHandler('log.txt'), StreamHandler()],
                    level=INFO)

load_dotenv('config.env', override=True)

BOT_TOKEN = environ.get('BOT_TOKEN', '')
if len(BOT_TOKEN) == 0:
    log_error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)

bot_id = BOT_TOKEN.split(':', 1)[0]

DATABASE_URL = environ.get('DATABASE_URL', '')
if len(DATABASE_URL) == 0:
    DATABASE_URL = None


UPSTREAM_REPO = environ.get('UPSTREAM_REPO', 'https://github.com/khainee/sam')
if len(UPSTREAM_REPO) == 0:
    UPSTREAM_REPO = None

UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', '')
if len(UPSTREAM_BRANCH) == 0:
    UPSTREAM_BRANCH = 'master'

if UPSTREAM_REPO is not None:
    if ospath.exists('.git'):
        srun(["rm", "-rf", ".git"])

    update = srun([f"git init -q \
            && git config --global user.email sam.agd@outlook.com \
            && git config --global user.name rctb \
            && git add . \
            && git commit -sm update -q \
            && git remote add origin {UPSTREAM_REPO} \
            && git fetch origin -q \
            && git reset --hard origin/{UPSTREAM_BRANCH} -q \
            && rm -rf .git"], shell=True)

    if update.returncode == 0:
        log_info('Successfully updated from UPSTREAM_REPO')
    else:
        log_error('Something went wrong while updating, check UPSTREAM_REPO if valid or not!')
