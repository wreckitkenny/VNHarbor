import docker
import yaml
import os

client = docker.from_env()

def pruneImage(client):
    try:
        [client.images.remove(image = tag, force=True) for image in client.images.list() for tag in image.tags]
        return "Pruned all images."
    except Exception as e:
        return e

def pullImage(registry, projectName, repoName, tagName):
    try:
        client.images.pull(repository=registry+'/'+projectName+'/'+repoName, tag=tagName)
    except Exception as e:
        return e

def pushImage(registry, projectName, repoName, tagName, newRegistry):
    for images in client.images.list():
        for image in images.tags:
            images.tag(repository=image.replace(registry, newRegistry))
            client.images.push(repository=image.replace(registry, newRegistry))

def saveImage(exportPath, projectName, repoName, tagName):
    for i in client.images.list():
        if not os.path.exists('{}'.format(exportPath)): os.makedirs(exportPath)
        with open('{}/{}_{}.tar'.format(exportPath,repoName, tagName), 'wb') as save:
            for chunk in i.save():
                save.write(chunk)

def exportImage(registry, projectName, savedArtPath, exportDir, newRegistry):
    savedInfo = yaml.load(open(savedArtPath), Loader=yaml.FullLoader)
    pruneImage(client)
    print("[+]Pulling all {}'s artifacts from {}.".format(projectName, registry))
    for repoName in list(savedInfo[projectName].keys()):
        for tagName in savedInfo[projectName][repoName]:
            pullImage(registry, projectName, repoName, tagName)
            if newRegistry == None:
                exportPath = '{}/{}'.format(exportDir, projectName)
                print("[+]Saving {}:{} at {}.".format(repoName, tagName, exportPath))
                saveImage(exportPath, projectName, repoName, tagName)
    print("[+]Pushing all {}'s artifacts to {}.".format(projectName, newRegistry))
    pushImage(registry, projectName, repoName, tagName, newRegistry)
    return True