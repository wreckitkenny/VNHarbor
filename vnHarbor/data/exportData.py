from .listData import getRepository
from utils import doubleEncode, doubleDecode
import requests
import wget, yaml, os

def downloadChart(registry, projectName, chartList, exportPath):
    for chart in chartList:
        indexUrl = "https://{}/chartrepo/{}/{}".format(registry, projectName, chart)
        if os.path.exists(exportPath+'/'+chart.split('/')[-1]): os.remove(exportPath+'/'+chart.split('/')[-1])
        wget.download(indexUrl, out=exportPath, bar='')
    return True

def exportAllArtifacts(apiUrl, headers):
    artifacts = {}
    repositories = getRepository('all')
    repositories = [value for list in repositories.values() for value in list]
    # print(repositories)
    for repoName in repositories:
        projectName = repoName.split('/')[0]
        repoName = doubleEncode("/".join(repoName.split('/')[1:]))
        url = "{}/projects/{}/repositories/{}/artifacts".format(apiUrl, projectName, repoName)
        payload = {'page':'1', 'page_size':'100', 'with_tag': 'true'}
        r = requests.get(url, headers=headers, params=payload)
        data = r.json()
        arts = [art['tags'][0]['name'] for art in data if art['tags'] != None]
        if projectName not in artifacts.keys():
            artifacts[projectName] = dict([(doubleDecode(repoName),arts)])
        else: artifacts[projectName][doubleDecode(repoName)] = arts
    return artifacts

def exportUser(apiUrl, headers):
    users = []
    url = "{}/users".format(apiUrl)
    payload = {'page':'1', 'page_size':'100'}
    r = requests.get(url, headers=headers, params=payload)
    data = r.json()
    for userData in data:
        users.append({'username': userData['username'], 'email': userData['email'], 'password': userData['password'],
                      'realname': userData['realname'], 'user_id': userData['user_id'], 'deleted': userData['deleted'],
                      'sysadmin_flag': userData['sysadmin_flag'], 'admin_role_in_auth': userData['admin_role_in_auth']})
    return users

def exportChart(registry, exportDir, projectName):
    exportPath = "{}/{}".format(exportDir, projectName)
    exportIndex = "{}/{}/index.yaml".format(exportDir, projectName)
    if not os.path.exists(exportPath): os.makedirs(exportPath)
    indexUrl = "https://{}/chartrepo/{}/index.yaml".format(registry, projectName)
    try:
        if os.path.exists(exportIndex): os.remove(exportIndex)
        tmp = wget.download(indexUrl, out=exportPath, bar='')
        print("[+]Downloaded and saved index.yaml file to {}".format(exportPath))
        chartList = processIndex(exportPath)
        downloadChart(registry, projectName, chartList, exportPath)
        print("[+]Downloaded all charts from {} file.".format(exportIndex))
    except Exception as e:
        return e

def processIndex(exportPath):
    helmList = []
    indexPath = "{}/index.yaml".format(exportPath)
    indexContent = yaml.load(open(indexPath), Loader=yaml.FullLoader)
    for helmKey in indexContent['entries'].keys():
        for helmVersion in indexContent['entries'][helmKey]:
            helmList += helmVersion['urls']
    return helmList

