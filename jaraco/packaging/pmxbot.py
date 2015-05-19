import pmxbot

from . import cheese

@pmxbot.core.command('upload-package')
def upload(client, event, channel, nick, rest):
	repo = pmxbot.config.package_index_url
	cheese.upload_file(repo, rest)
	return "Done"
