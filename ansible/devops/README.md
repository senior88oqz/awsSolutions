# Deployment Process (Montebello Demo)

## Phase 1 - Manually Setup

`//TODO repo dependencies`
`cp IPC/images/1362serv lexx-core/dist/images/1362serv`

Step 1 - Launch EC2 Instance: Creates t2.medium ec2 instance

- [ ] VPC & subnet configuration
- [ ] IAM Role `//TODO`
- [ ] Add extra storage
- EBS Volume
- S3 Buckets
- [ ] Add tags
- [ ] Configure Security Group (open port 80 for web server)
- [ ] Key pairs
- [ ] DNS setup via Route 53

Step 2 - Configurate EC2 Environment:

- [ ] Add personal public to `~/.ssh/authorized_keys`
- [ ] Configurate SSH connection to CodeCommit
- copy `config` and codecommit private key to `~/.ssh`
- [ ] Mount additional volume
- `sudo fdisk -l`
- `mkfs.ext4 <device name>`
- `mkdir webApp`
- `sudo mount <device name> wenApp`
- automount at boot (change [`/etc/fstab`](https://help.ubuntu.com/community/Fstab))
- [ ] Install `java`, `python`, `pip`, `NVM`
- create symbolic link from `/usr/bin` to NVM_folder
- set `LC_ALL="en_US.UTF-8` `LC_CTYPE="en_US.UTF-8` in `/etc/environment` (for installation from `pip`)
- install `forever` via `npm` (link `/usr/bin/forever` to `NVM_forlder/bin/forever`)

Step 3 - Deploy Web Application

- [ ] Checkout lexx-core repo (_develop_ branch)
- [ ] Install app dependencies defined in `package.json` (via `npm`)
- [ ] Run `build.sh` and build the web app in `dist` folder
- [ ] Start web application by running `forever start path_to_dist/server/run.js` (default port 9000 unless specify in command line)
- prot forwarding: `sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 9000`
- check by `forever list`
- [ ] Stop web app by `forever stopall`

Step 4 - Setup Solr

- [ ] Download and unzip solr
- Add `export SOLR_HOME="/home/ubuntu/solr-7.4.0/server/solr"` in `/etc/environment` (used by `conf.sh`)
- [ ] Run solr in cloud mode
- `cd path_to_solrDir/bin && ./solr -c`
- _Don't run solr as service for now_
- [ ] Checkout montebello repo (_MBL-29_ branch)
- [ ] `cd scripts/dev && ./conf.sh`
- [ ] Indexing data to solr (in the same directory as above)
- install `pysolr`, `lxml`
- `yes | index.sh`

## Phase 2 - Automate configuration by Ansible

 Step 1 - Launch EC2 Instance: Creates t2.medium ec2 instance
- [ ] Automate via `boto`(single instance), AWS CloudFormation template `//TODO`

Step 2 - Initial instance configuration, web application and solr setup

- [ ] [Ansible Setup](https://1ansah.atlassian.net/wiki/spaces/DEV/pages/530513922/Ansible+for+DevOps)
- [ ] `ansible-playbook webAppSetup.yml`
- [ ] `ansible-playbook solrSetup.yml`

Step 3 - Creates admin/maintaince playbooks for regular setup/update of the web app, datapipe `//TODO`

## Useful Commands

- Check on port usage
  - `lsof -i :8000` <-> check on port 8000
  - `ps -fp 1289` <-> more details by checking on `pid` return from the above command 
  - `sudo netstat -peanut` <-> all network usage info
