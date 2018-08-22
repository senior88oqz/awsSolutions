# Ansible Setup

## Installation

```
$ sudo pip install ansible
```

## Creat a basic inventory
Ansible uses an inventory file to communicates with your servers.

```
$ sudo mkdir /etc/ansible
$ sudo touch /etc/ansible/hosts
```

Edit _hosts_ file created above (**with sudo as root**):

### Example 1

```
[example]
www.example.com
www.example2.com:8898
host0 ansible_ssh_host=115.146.86.214
```

**Note**

* If Ansible reports `No hosts matched` or returns some other inventory- related error, try setting the `ANSIBLE_HOSTS` environment variable explicitly: `export ANSIBLE_HOSTS=/etc/ansible/hosts`.

### Example 2

```

# Application servers
[app]
192.168.60.4
192.168.60.5

# Database server
[db]
192.168.60.6

# Group 'multi' with all servers
[multi:children]
app
db

# Variables that will be applied all servers
[multi:vars]
ansible_ssh_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/privateKey
```

**Note**

* The third block tells ansible to define a new group ‘multi’, with child groups, and we add in both the ‘app’ and ‘db’ groups.

* The fourth block adds variables to the multi group that will be applied to all servers within multi and all its children.

## Faster OpenSSH

Adds `pipelining=True` under the `[ssh_connection]` section of the Ansible configuration file (`ansible.cfg`)

**Note**

The `pipelining=True` configuration option won’t help much unless you have removed or commented the Defaults requiretty option in /etc/sudoers. 

## Ansible Ad-Hoc commands for simple deployments

### Test server connections

```
$ ansible exmaple -m ping -u [username]
```

**Note** 

* Add your [SSH key](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) to the `ssh-agent` and connect to the server once _before_ you run the above command

### Run commands as if in shell

```
$ ansible multi -a "free -m"
```

### Make changes using Ansible modules (`-m`)

```
$ ansible multi -s -m yum -a "name=ntp state=present"
```

```
$ ansible app -s -m package -a "name=git state=present" --limit "192.168.60.4"
```

**Note**

* The `-s` option (alias for `--sudo`) tells Ansible to run the command with sudo.

* `package` works much the same as `yum`, `apt`, it installs a generic package like `git` on any Debian, RHEL, Fedora, Ubuntu, CentOS, FreeBSD, etc. system

* `--limit` will match either an exact string or a regular expression (prefixed with ∼) 

### Manage files and directories

```
$ ansible multi -m copy -a "src=/etc/hosts dest=/tmp/hosts"
```

**Note**

* The `src` can be a file or a directory.

* Perfect for single-file copies, and works very well with small directories

* For deeply nested directory structures, consider either copying then expanding an archive of the files with Ansible’s `unarchive` module, or using Ansible’s `synchronize` or `rsync` modules.

```
$ ansible multi -s -m fetch -a "src=/etc/hosts dest=/tmp"
```

**Note**

* Only use `flat=yes` if you’re copying files from a _single_ host.

Here’s how to create a directory:

```
$ ansible multi -m file -a "dest=/tmp/test mode=644 state=directory"
```

Here’s how to create a symlink (set state=link):

```
$ ansible multi -m file -a "src=/src/symlink dest=/dest/symlink owner=root group=root state=link"
```

**Note**

* Set `state=absent` for delete a file

### Run operations in the background

To run a command in the background, you set the following options:

* `-B <seconds>`: the maximum amount of time (in seconds) to let the job run.

* `-P <seconds>`: the amount of time (in seconds) to wait between polling the servers for an updated job status.

While a background task is running, you can also check on the status elsewhere using Ansible’s `async_status` module, as long as you have the `ansible_job_id` value to pass in as `jid`:

```
    $ ansible multi -s -m async_status -a "jid=763350539037"
```

## Ansible playbook

In Ansible, you write playbooks (a list of instructions describing the steps to bring your server to a certain configuration state) that are then _played_ on your servers.

### Accelerated Mode

    Accelerated mode can offer 2-4 times faster performance (especially for things like file transfers) compared to OpenSSH, and you can enable it for a playbook by adding the option accelerate: true to your playbook, like so:

```yml
    ---
    - hosts: all
      accelerate: true
    [...]
```

**Note**

* Extra package required to use accelerated mode is `python-keyczar`
* Your sudoers file needs to have `requiretty` disabled (comment out the line with it, or set it per user by changing the line to `Defaults:username !requiretty`)
* You must disable sudo passwords by setting `NOPASSWD` in the sudoers file

### Shell Script v.s Playbook

It is easy to convert shell scripts (or one-off shell commands) directly into Ansible plays.

* Shell Script

```bash
# Install Apache.
yum install --quiet -y httpd httpd-devel
# Copy configuration files.
cp httpd.conf /etc/httpd/conf/httpd.conf
cp httpd-vhosts.conf /etc/httpd/conf/httpd-vhosts.conf
# Start Apache and configure it to run at boot.
service httpd start
chkconfig httpd on
```

* Ansible Playbook

```yml
---
- hosts: all
  become: yes

  tasks:
    - name: Install Apache
      yum: name={{item}} state=present
      with_items:
        - httpd
        - httpd-devel
    - name: Copy config files
      copy: 
        src: "{{item.src}}"
        dest: "{{item.dest}}"
        owner: root
        group: root
        mode: 0644
      with_items:
        - src: "httpd.conf"
          dest: "/etc/httpd/conf/httpd.conf"
        - src: "httpd-vhosts.conf"
          dest: "/etc/httpd/conf/httpd-vhosts.conf"
    - name: Make sure Apache is started now and at boot.
      service: name=httpd state=start enabled=yes
```

1. `---` : YAML marker
2. `- host: all` : Telling Ansible to which hosts this playbook applies
3. `become: yes` : Apply _sudo_ prevelige in the following tasks
4. `tasks` : All the tasks after this line will run on all hosts

To run the palybook:

```bash
# (From the same directory in which the playbook resides).
$ ansible-playbook playbook.yml
```

**Some other useful Flags**

* `--list-hosts` show list of hosts that would be affected by your playbook
* `--limit` Overwrites taget host
* `--inventory=PATH` (`-i PATH`): Define a custom inventory file (default is the default Ansible inventory file, usually located at `/etc/ansible/hosts`).
* `--verbose` (`-v`): Verbose mode (show all output, including output from successful options). You can pass in -vvvv to give every minute detail.
* `--check`: Run the playbook in Check Mode (‘Dry Run’); all tasks defined in the playbook will be checked against all hosts, but none will actually be run.

## Reference

1. [Ansible for DevOps](https://github.com/geerlingguy/ansible-for-devops)
2. [List of Modules](https://docs.ansible.com/ansible/2.5/modules/list_of_all_modules.html)
3. [Folder Structure](https://leucos.github.io/ansible-files-layout)