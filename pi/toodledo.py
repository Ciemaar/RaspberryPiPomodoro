from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError

__author__ = 'andriod'

import re

from poodledo.apiclient import ApiClient, PoodledoError, ToodledoError


taskRegex = re.compile(r'\[(\d)\].*')

config = SafeConfigParser()

config.read(["pom.cur","pom.cfg"])

client = ApiClient(app_id=config.get('toodledo', 'id'),app_token=config.get('toodledo', 'token'))

def save_current_config():
    config.write(open("pom.cur", "wt"))

try:
    client._key = config.get('session-cache', 'key')
    client.getAccountInfo()
    print "Using Cached Token"
except (NoSectionError, NoOptionError, ToodledoError):
    print "Establishing new token"
    client._key = None
    client.authenticate(config.get('toodledo', 'username'),config.get('toodledo', 'password'))

    if not config.has_section('session-cache'):
        config.add_section('session-cache')
    config.set('session-cache', 'key', client.key)
    save_current_config()

def get_pom_tasks():
    return  [task for task in client.getTasks(cache=True, fields='tag') if not task.completed and "pom" in task.tag]

def update_task_numbers():
    pomTasks = get_pom_tasks()
    assignedNumbers = set(taskRegex.match(task.title).group(1) for task in pomTasks if taskRegex.match(task.title))
    #print assignedNumbers
    #Remove the already assigned numbers
    taskNumbers = set(str(x) for x in xrange(1, 8))
    taskNumbers -= assignedNumbers
    while pomTasks and taskNumbers:
        task = pomTasks.pop()
        if taskRegex.match(task.title):
            continue
        newNum = taskNumbers.pop()
        client.editTask(task.id, title=("[%s] " % newNum) + task.title)

if __name__ == '__main__':
    update_task_numbers()