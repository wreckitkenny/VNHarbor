from utils import doubleEncode, doubleDecode
import requests

def getProject(apiUrl, headers):
    url = "{}/projects".format(apiUrl)
    payload = {'page':'1', 'page_size':'100', 'with_detail': 'true'}
    r = requests.get(url, headers=headers, params=payload)
    data = r.json()
    projects = [project['name'] for project in data]
    return projects

def getProjectId(apiUrl, headers, projectName):
    url = "{}/projects".format(apiUrl)
    payload = {'page':'1', 'page_size':'100', 'with_detail': 'true'}
    r = requests.get(url, headers=headers, params=payload)
    data = r.json()
    if projectName == "all": projectIds = [dict([(project['name'],project['project_id'])]) for project in data]
    else: projectIds = [dict([(project['name'],project['project_id'])]) for project in data if project['name'] == projectName]
    return projectIds

def getRepository(apiUrl, headers, projectName):
    repositories = {}
    if projectName == "all":
        projects = getProject(apiUrl, headers)
        for project in projects:
            url = "{}/projects/{}/repositories".format(apiUrl, project)
            payload = {'page':'1', 'page_size':'100', 'with_detail': 'true'}
            r = requests.get(url, headers=headers, params=payload)
            data = r.json()
            repos = [repo['name'] for repo in data]
            repositories[project] = repos
    else:
        project = projectName
        url = "{}/projects/{}/repositories".format(apiUrl, project)
        payload = {'page':'1', 'page_size':'100', 'with_detail': 'true'}
        r = requests.get(url, headers=headers, params=payload)
        data = r.json()
        repos = [repo['name'] for repo in data]
        repositories[project] = repos
    return repositories

def getArtifact(apiUrl, headers, projectName, repoName):
    artifacts = {}
    if repoName == "all":
        repositories = getRepository(apiUrl, headers, projectName)[projectName]
        for repoName in repositories:
            repoName = doubleEncode("/".join(repoName.split('/')[1:]))
            url = "{}/projects/{}/repositories/{}/artifacts".format(apiUrl, projectName, repoName)
            payload = {'page':'1', 'page_size':'100', 'with_tag': 'true'}
            r = requests.get(url, headers=headers, params=payload)
            data = r.json()
            arts = [art['tags'][0]['name'] for art in data if art['tags'] != None]
            if projectName not in artifacts.keys():
                artifacts[projectName] = dict([(doubleDecode(repoName),arts)])
            else: artifacts[projectName][doubleDecode(repoName)] = arts
    else:
        repoName = "/".join(repoName.split('/')[1:])
        repoName = doubleEncode(repoName)
        url = "{}/projects/{}/repositories/{}/artifacts".format(apiUrl, projectName, repoName)
        payload = {'page':'1', 'page_size':'100', 'with_tag': 'true'}
        r = requests.get(url, headers=headers, params=payload)
        data = r.json()
        arts = [art['tags'][0]['name'] for art in data if art['tags'] != None]
        artifacts[projectName] = dict([(doubleDecode(repoName),arts)])
    return artifacts

def getUser(apiUrl, headers):
    users = []
    url = "{}/users".format(apiUrl)
    payload = {'page':'1', 'page_size':'100'}
    r = requests.get(url, headers=headers, params=payload)
    data = r.json()
    for userData in data:
        users.append(userData['username'])
    return users

def getMember(apiUrl, headers, projectName):
    members = {}
    projectId = getProjectId(apiUrl, headers, projectName)
    if projectName == "all":
        for pId in projectId:
            url = "{}/projects/{}/members".format(apiUrl, list(pId.values())[0])
            r = requests.get(url, headers=headers)
            data = r.json()
            members[list(pId.keys())[0]] = data
    return members