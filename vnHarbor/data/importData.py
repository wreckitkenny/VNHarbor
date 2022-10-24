import json
import requests
import yaml
import os

def importUser(apiUrl, headers, file):
    success = []
    warning = []
    url = "{}/users".format(apiUrl)
    with open(file, 'r', encoding="utf-8") as iu:
        users = iu.readlines()
        for u in users:
            user = json.loads(u.replace("\'", "\"").replace("True", "true").replace("False", "false"))
            r = requests.post(url, headers=headers, json=user)
            if r.status_code != 201: warning.append(dict([(user['username'],str(r.status_code)+'|'+r.json()['errors'][0]['message'])]))
            else: success.append(user['username'])
    return success,warning

def importProject(apiUrl, headers, file):
    success = []
    warning = []
    url = "{}/projects".format(apiUrl)
    with open(file, 'r', encoding="utf-8") as ip:
        projects = ip.readlines()
        for p in projects:
            project = {"project_name": p.strip(), "storage_limit": 21474836480, "public": True}
            r = requests.post(url, headers=headers, json=project)
            if r.status_code != 201: warning.append(dict([(project['project_name'],str(r.status_code)+'|'+r.json()['errors'][0]['message'])]))
            else: success.append(project['project_name'])
    return success,warning

def importMember(apiUrl, headers, file):
    members = yaml.load(open(file), Loader=yaml.FullLoader)
    for project in members.keys():
        for member in members[project]:
            url = "{}/projects/{}/members".format(apiUrl, project)
            projectMember = {"role_id": member["role_id"], "member_user": {"username": member["entity_name"], "user_id": member["entity_id"]}}
            r = requests.post(url, headers=headers, json=projectMember)
            if r.status_code != 201: print(dict([(project,str(r.status_code)+'|'+r.json()['errors'][0]['message'])]))
            return True

def importChart(exportDir, headers, projectName, newRegistry):
    url = "https://{}/api/chartrepo/{}/charts".format(newRegistry, projectName)
    exportedPath = "{}/{}".format(exportDir, projectName)
    for tgz in os.listdir(exportedPath):
        if tgz.endswith(".tgz"):
            files = {'chart': open('{}/{}'.format(exportedPath, tgz), 'rb'), 'Content-Type': 'multipart/form-data'}
            r = requests.post(url, headers=headers, files=files)
            if r.status_code != 201: print(dict([("{}/{}".format(projectName,tgz),str(r.status_code))]))
            return True