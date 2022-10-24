import data
from auth import checkAuth, addAuth, getAuth
import argparse
import getpass
import sys, os
import yaml

def processData(exportDir):
    parser = argparse.ArgumentParser(description="Harbor management tool")
    parser.add_argument('-e', '--exp', metavar='[project|repo|artifact|user|member|all]', help='export Harbor data', action='store')
    parser.add_argument('-i', '--imp', metavar='[project|repo|artifact|user|member|all]', help='import Harbor data', action='store')
    parser.add_argument('-l', '--list', metavar='[project|repo|artifact|user|member]', help='list projects', action='store')
    parser.add_argument('-p', '--project', help='interact to Harbor projects', action='store')
    parser.add_argument('-r', '--repository', help='interact to Harbor repositories', action='store')
    parser.add_argument('-f', '--file', help='path to exported files', action='store')
    parser.add_argument('-d', '--drain', help='save information to file', action='store_true')
    parser.add_argument('-m', '--migrate', metavar='new REGISTRY domain', help='new registry', action='store')
    parser.add_argument('registry', help='Registry domain', action='store')
    args = parser.parse_args()
    # print(args)
    if not len(sys.argv) > 1: parser.print_help()

    ## Check Registry
    authenticated = checkAuth(args.registry)
    if not authenticated:
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        token = addAuth(username, password, args.registry)
    else:
        token = getAuth(args.registry)

    apiUrl = "https://{}/api/v2.0".format(args.registry)
    headers = {'accept': 'application/json', 'Authorization': 'Basic {}'.format(token), 'Content-Type': 'application/json'}
    chartPostHeaders = {'accept': 'application/json', 'Authorization': 'Basic {}'.format(token)}

    ## List data
    if args.list == "project":
        projects = data.getProject(apiUrl, headers)
        for p in range(len(projects)): print('{}.{}'.format(p+1,projects[p]))
    if args.list == "repo":
        if not args.project: sys.exit("[-]ERROR: Argument [-p/--project PROJECT] is required")
        else:
            repos = data.getRepository(apiUrl, headers, args.project)
            print(yaml.dump(repos))
    if args.list == "artifact":
        if not args.project or not args.repository: sys.exit("ERROR: Arguments [-p/--project PROJECT] and [-r/--repository REPOSITORY] are required")
        else:
            arts = data.getArtifact(apiUrl, headers, args.project, args.repository)
            print(yaml.dump(arts))
    if args.list == "user":
        users = data.getUser(apiUrl, headers)
        for u in range(len(users)): print('{}.{}'.format(u+1,users[u]))
    if args.list == "member":
        if not args.project: sys.exit("ERROR: Argument [-p/--project PROJECT] is required")
        else:
            members = data.getMember(apiUrl, headers, args.project)
            print(yaml.dump(members))

    ## Export data
    if args.exp == "project":
        if not os.path.exists(exportDir): os.makedirs(exportDir)
        with open('{}/projects.yaml'.format(exportDir), mode='w') as ep:
            projects = data.getProject(apiUrl, headers)
            for p in projects: ep.write(p+'\n')
    if args.exp == "repo":
        if not args.project: sys.exit("ERROR: Argument [-p/--project PROJECT] is required")
        if not os.path.exists(exportDir): os.makedirs(exportDir)
        with open('{}/[repo]{}.yaml'.format(exportDir,args.project), mode='w') as er:
            repos = data.getRepository(apiUrl, headers, args.project)
            yaml.dump(repos,er)
            print("[+]{}'s artifact information is saved to {}".format(args.project, savedArtPath))
    if args.exp == "artifact":
        savedArtPath = '{}/[art]{}_{}.yaml'.format(exportDir, args.project, args.repository.replace('/','-'))
        if not args.project or not args.repository: sys.exit("ERROR: Arguments [-p/--project PROJECT] and [-r/--repository REPOSITORY] are required")
        if not os.path.exists(exportDir): os.makedirs(exportDir)
        with open(savedArtPath, mode='w') as ea:
            arts = data.getArtifact(apiUrl, headers, args.project, args.repository)
            yaml.dump(arts,ea)
            print("[+]{}'s artifact information is saved to {}".format(args.project, savedArtPath))
        if args.drain == False:
            print("[+]Migrating images from {} to {} based on {}...".format(args.registry, args.migrate, savedArtPath))
            exportStatus = data.exportImage(args.registry, args.project, savedArtPath, exportDir, args.migrate)
            if exportStatus: print("--> Migrated {}/{} from {} to {}.".format(args.project, args.repository, args.registry, args.migrate))
    if args.exp == "user":
        if not os.path.exists(exportDir): os.makedirs(exportDir)
        with open('{}/users.txt'.format(exportDir), mode='w') as eu:
            users = data.exportUser(apiUrl, headers)
            for u in users: eu.write(str(u)+'\n')
    if args.exp == "member":
        if not os.path.exists(exportDir): os.makedirs(exportDir)
        if not args.project: sys.exit("ERROR: Argument [-p/--project PROJECT] is required")
        else:
            with open('{}/members.yaml'.format(exportDir), mode='w') as em:
                members = data.getMember(apiUrl, headers, args.project)
                yaml.dump(members,em)
    if args.exp == "chart":
        if not args.project: sys.exit("ERROR: Argument [-p/--project PROJECT] is required")
        else: data.exportChart(args.registry, exportDir, args.project)
        if args.drain == False:
            chartStatus = data.importChart(exportDir, chartPostHeaders, args.project, args.migrate)
            if chartStatus: print("[+]Imported Helm charts successfully.")
    if args.exp == "all":
        if not os.path.exists(exportDir): os.makedirs(exportDir)
        with open('{}/all.yaml'.format(exportDir), mode='w') as all:
            alls = data.exportAllArtifacts(apiUrl, headers)
            yaml.dump(alls,all)

    ## Import data
    if args.imp == "user":
        if not args.file: sys.exit("ERROR: Argument [-f/--file EXPORTED_FILE] is required")
        success, warning = data.importUser(apiUrl, headers, args.file)
        for r in warning: print("Warning: {}.".format(r))
        print("Imported {}/{} users to {}".format(len(success), len(success)+len(warning), args.registry))
    if args.imp == "project":
        if not args.file: sys.exit("ERROR: Argument [-f/--file EXPORTED_FILE] is required")
        success, warning = data.importProject(apiUrl, headers, args.file)
        for r in warning: print("Warning: {}.".format(r))
        print("Imported {}/{} projects to {}".format(len(success), len(success)+len(warning), args.registry))
    if args.imp == "artifact":
        if not args.file: sys.exit("ERROR: Argument [-f/--file EXPORTED_FILE] is required")
        data.importArtifact(apiUrl, headers, args.file)
    if args.imp == "member":
        if not args.file: sys.exit("ERROR: Argument [-f/--file EXPORTED_FILE] is required")
        memberStatus = data.importMember(apiUrl, headers, args.file)
        if memberStatus: print("Importing members: DONE.")