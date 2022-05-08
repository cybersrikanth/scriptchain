# Script Chain

Note: This is rough draft. To be updated clearly.

This tool can be used chain system commands and custom python functions in a sequence to perform certain actions.

Currently this tool has one configuration **webasset_scan**.

#### Usage

* Install virtual env (with name "venv") and install dependencies.
* Install the following tools in the folder **tools/**
```
* Subfinder
* httpx
* nuclei
* nuclei_templates
```
* Create a file 'example.txt' in storage/domain_list_files
* Add all domains of the target in that file.
* Open **webasset_scan.json**, in that update *project_domain_list* attribute
```
["Example Project Name", "storage/domain_list_files/example.txt", true]
```
* Feel free to edit the commands in the config file.
* Now enter `bash run.sh webasset_scan` to start scan.
* Logs can be found in `tools.log` file
* Outputs will be in `out/*` folder

---
Note: This is rough draft