[![Python 3.8](https://img.shields.io/badge/Python3-%3E%3D3.8-blue)](https://www.python.org/downloads)

# vnharbor
vnharbor is a Python tool to export/import/migrate data to another Harbor Registry.

#
## vnharbor Features
> Data Export:
>>- List of projects
>>- List of repositories
>>- List of artifacts (tags)
>>- List of members followed by Project name
>>- List of users

> Data Import:
>>- List of projects
>>- List of repositories
>>- List of artifacts (tags) #Ability to migrate with option -m/--migrate
>>- List of members followed by Project name
>>- List of users

#
## vnharbor structure
```python3
vnharbor/
├── bin
├── config
├── data
├── docs
│   └── CHANGELOG.md
├── LICENSE
├── README.md
├── requirements.txt
├── tests
└── vnHarbor
    ├── auth
    │   ├── __init__.py
    │   └── validate.py
    ├── data
    │   ├── dockerClient.py
    │   ├── exportData.py
    │   ├── importData.py
    │   ├── __init__.py
    │   ├── listData.py
    │   └── processData.py
    ├── run.py
    └── utils
        ├── __init__.py
        └── utils.py

9 directories, 15 files
```

#
## Requirements
```bash
PyYAML==5.4.1
docker==6.0.0
```

#
## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.
```bash
pip3 install -r requirements.txt
```

#
## Usage
```bash
$ python3 run.py -h
usage: run.py [-h] [-e [project|repo|artifact|user|member|all]] [-i [project|repo|artifact|user|member|all]]
              [-l [project|repo|artifact|user|member]] [-p PROJECT] [-r REPOSITORY] [-f FILE] [-d] [-m new REGISTRY domain]
              registry

Harbor management tool

positional arguments:
  registry              Registry domain

options:
  -h, --help            show this help message and exit
  -e [project|repo|artifact|user|member|all], --exp [project|repo|artifact|user|member|all]
                        export Harbor data
  -i [project|repo|artifact|user|member|all], --imp [project|repo|artifact|user|member|all]
                        import Harbor data
  -l [project|repo|artifact|user|member], --list [project|repo|artifact|user|member]
                        list projects
  -p PROJECT, --project PROJECT
                        interact to Harbor projects
  -r REPOSITORY, --repository REPOSITORY
                        interact to Harbor repositories
  -f FILE, --file FILE  path to exported files
  -d, --drain           save information to file
  -m new REGISTRY domain, --migrate new REGISTRY domain
                        new registry
```

#
## License
[MIT](LICENSE)