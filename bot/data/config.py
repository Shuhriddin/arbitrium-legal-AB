from environs import Env
env = Env()
env.read_env()
BOT_TOKEN=env.str('BOT_TOKEN')
DB_TG_CHANNEL=env.str('DB_TG_CHANNEL')
ADMINS=env.list('ADMINS')
