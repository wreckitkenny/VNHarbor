import base64
import os
import json
import shutil

HOMEPATH = os.path.expanduser('~')

def addAuth(username, password, registry):
    token = (base64.b64encode('{}:{}'.format(username, password).encode())).decode()
    with open('{}/.docker/config.json'.format(HOMEPATH), 'r') as jsonRead, open('{}/.docker/tmp.json'.format(HOMEPATH), 'w') as jsonWrite:
        auths = json.load(jsonRead)
        auths['auths'][registry] = { 'auth': token }
        jsonWrite.write(json.dumps(auths, indent=4))
    shutil.copyfile('{}/.docker/tmp.json'.format(HOMEPATH),'{}/.docker/config.json'.format(HOMEPATH))
    return token

def checkAuth(registry):
    if not os.path.exists('{}/.docker/config.json'.format(HOMEPATH)):
        return False
    with open('{}/.docker/config.json'.format(HOMEPATH), 'r') as configJson:
        auths = json.load(configJson)
        if registry not in auths['auths'].keys():
            return False
        else: return True

def getAuth(registry):
    with open('{}/.docker/config.json'.format(HOMEPATH), 'r') as configJson:
        auths = json.load(configJson)
        token = auths['auths'][registry]['auth']
    return token
