# Official Modular Repo atop F28 Traditional

A container that provides the pre-alpha of Fedora 28 which will provide modules in a separate repository. The container should be fully enabled. 

# Directions for use

```
$ docker run --rm -it docker.io/langdon/addon-modular-boltron
# dnf module list
```

# You can also now make your local module builds available 
```
$ docker run --rm -it $HOME/modulebuild/builds/:/local-modules:z docker.io/langdon/addon-modular-boltron
Making module-bind-9-20180328194441 repo available #(for example)
Making module-postgresql-9.6-20180328190827 repo available #(for example)
# dnf module list 
```


# Basic Examples

## Install the default nodejs

```# dnf install nodejs```

## Install a non-default default version of nodejs

```# dnf install @nodejs:6```

## Install a non-default profile of nodejs

```# dnf install @nodejs/development```

# Making your own

* Install Fedora 28 Server Edition on a virtual or physical system using the
  standard install media. Run this on a disposable installation; it changes
  core system functionality (DNF) and may cause heartbreak if used on
  critical systems.
* Record the IP address or resolvable DNS hostname of the system in an
  [ansible host inventory](https://ansible-tips-and-tricks.readthedocs.io/en/latest/ansible/inventory/)
* Ansible 2.x (I used 2.4.1.0) to run on the managing system

## Adding modularity to the system
```
ansible-playbook -i <host_inventor_file> semimodular-play.yml
```

This will perform the following actions:
* Install a version of DNF that is module-aware from the Fedora 28 repository
* Copy the latest system profile definition from the files directory
* Configures DNF to use the modular repository by way of installing the fedora-repos-modular package.

# More Advanced Testing & Examples
SSH into the modified system and play around with `dnf module` commands. For
example:

```
[root@semimodular yum.repos.d]# dnf module list
Last metadata expiration check: 0:00:07 ago on Wed 29 Nov 2017 09:06:20 PM EST.
Test repo for modules
Name                     Stream                   Version                          Profiles                                  
nodejs                   6                        20171116134309                   default, development, ...                 
nodejs                   8 [d]                    20171116133906                   default, development, ...                 

Hint: [d]efault, [e]nabled, [i]nstalled, [l]ocked
[root@semimodular yum.repos.d]# dnf install nodejs
Last metadata expiration check: 0:00:17 ago on Wed 29 Nov 2017 09:06:20 PM EST.
Dependencies resolved.
=============================================================================================================================
 Package             Arch                Version                                            Repository                  Size
=============================================================================================================================
Installing:
 nodejs              x86_64              1:8.9.1-1.module_d4e9ce34                          local-modules              5.6 M
Installing dependencies:
 libicu              x86_64              57.1-9.fc27                                        updates                    8.4 M
Installing weak dependencies:
 npm                 x86_64              1:5.5.1-1.8.9.1.1.module_d4e9ce34.2                local-modules              4.2 M

Transaction Summary
=============================================================================================================================
Install  3 Packages

Total size: 18 M
Total download size: 8.4 M
Installed size: 67 M
Is this ok [y/N]: n
Operation aborted.
[root@semimodular yum.repos.d]# dnf module enable nodejs:6
Last metadata expiration check: 0:00:28 ago on Wed 29 Nov 2017 09:06:20 PM EST.
'nodejs:6' is enabled
[root@semimodular yum.repos.d]# dnf module list
Last metadata expiration check: 0:00:32 ago on Wed 29 Nov 2017 09:06:20 PM EST.
Test repo for modules
Name                     Stream                   Version                          Profiles                                  
nodejs                   6 [e]                    20171116134309                   default, development, ...                 
nodejs                   8 [d]                    20171116133906                   default, development, ...                 

Hint: [d]efault, [e]nabled, [i]nstalled, [l]ocked
[root@semimodular yum.repos.d]# dnf install nodejs
Last metadata expiration check: 0:00:38 ago on Wed 29 Nov 2017 09:06:20 PM EST.
Dependencies resolved.
=============================================================================================================================
 Package             Arch                Version                                            Repository                  Size
=============================================================================================================================
Installing:
 nodejs              x86_64              1:6.12.0-1.module_91d2e14d                         local-modules              4.8 M
Installing dependencies:
 libicu              x86_64              57.1-9.fc27                                        updates                    8.4 M
Installing weak dependencies:
 npm                 x86_64              1:3.10.10-1.6.12.0.1.module_91d2e14d               local-modules              2.5 M

Transaction Summary
=============================================================================================================================
Install  3 Packages

Total size: 16 M
Total download size: 8.4 M
Installed size: 55 M
Is this ok [y/N]: y
Downloading Packages:
libicu-57.1-9.fc27.x86_64.rpm                                                                2.7 MB/s | 8.4 MB     00:03    
-----------------------------------------------------------------------------------------------------------------------------
Total                                                                                        2.4 MB/s | 8.4 MB     00:03     
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                                     1/1 
  Installing       : libicu-57.1-9.fc27.x86_64                                                                           1/3 
  Running scriptlet: libicu-57.1-9.fc27.x86_64                                                                           1/3 
  Installing       : nodejs-1:6.12.0-1.module_91d2e14d.x86_64                                                            2/3 
  Installing       : npm-1:3.10.10-1.6.12.0.1.module_91d2e14d.x86_64                                                     3/3 
  Running scriptlet: npm-1:3.10.10-1.6.12.0.1.module_91d2e14d.x86_64                                                     3/3 
  Verifying        : nodejs-1:6.12.0-1.module_91d2e14d.x86_64                                                            1/3 
  Verifying        : libicu-57.1-9.fc27.x86_64                                                                           2/3 
  Verifying        : npm-1:3.10.10-1.6.12.0.1.module_91d2e14d.x86_64                                                     3/3 

Installed:
  nodejs.x86_64 1:6.12.0-1.module_91d2e14d    npm.x86_64 1:3.10.10-1.6.12.0.1.module_91d2e14d    libicu.x86_64 57.1-9.fc27   

Complete!
[root@semimodular yum.repos.d]# dnf module install nodejs:8
Last metadata expiration check: 0:02:06 ago on Wed 29 Nov 2017 09:06:20 PM EST.
Dependencies resolved.
=============================================================================================================================
 Package             Arch                Version                                            Repository                  Size
=============================================================================================================================
Upgrading:
 nodejs              x86_64              1:8.9.1-1.module_d4e9ce34                          local-modules              5.6 M
 npm                 x86_64              1:5.5.1-1.8.9.1.1.module_d4e9ce34.2                local-modules              4.2 M

Transaction Summary
=============================================================================================================================
Upgrade  2 Packages

Total size: 9.8 M
Is this ok [y/N]: y
Downloading Packages:
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                                     1/1 
  Upgrading        : nodejs-1:8.9.1-1.module_d4e9ce34.x86_64                                                             1/4 
  Upgrading        : npm-1:5.5.1-1.8.9.1.1.module_d4e9ce34.2.x86_64                                                      2/4 
  Cleanup          : npm-1:3.10.10-1.6.12.0.1.module_91d2e14d.x86_64                                                     3/4 
  Cleanup          : nodejs-1:6.12.0-1.module_91d2e14d.x86_64                                                            4/4 
  Running scriptlet: nodejs-1:6.12.0-1.module_91d2e14d.x86_64                                                            4/4 
  Verifying        : nodejs-1:8.9.1-1.module_d4e9ce34.x86_64                                                             1/4 
  Verifying        : npm-1:5.5.1-1.8.9.1.1.module_d4e9ce34.2.x86_64                                                      2/4 
  Verifying        : npm-1:3.10.10-1.6.12.0.1.module_91d2e14d.x86_64                                                     3/4 
  Verifying        : nodejs-1:6.12.0-1.module_91d2e14d.x86_64                                                            4/4 

Upgraded:
  nodejs.x86_64 1:8.9.1-1.module_d4e9ce34                   npm.x86_64 1:5.5.1-1.8.9.1.1.module_d4e9ce34.2                  

Complete!
[root@semimodular yum.repos.d]# dnf module install nodejs:6
Last metadata expiration check: 0:02:17 ago on Wed 29 Nov 2017 09:06:20 PM EST.
Enabling different stream for 'nodejs'
Is this ok [y/N]: y
Dependencies resolved.
=============================================================================================================================
 Package             Arch                Version                                            Repository                  Size
=============================================================================================================================
Downgrading:
 nodejs              x86_64              1:6.12.0-1.module_91d2e14d                         local-modules              4.8 M
 npm                 x86_64              1:3.10.10-1.6.12.0.1.module_91d2e14d               local-modules              2.5 M

Transaction Summary
=============================================================================================================================
Downgrade  2 Packages

Total size: 7.3 M
Is this ok [y/N]: y
Downloading Packages:
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                                     1/1 
  Downgrading      : nodejs-1:6.12.0-1.module_91d2e14d.x86_64                                                            1/4 
  Downgrading      : npm-1:3.10.10-1.6.12.0.1.module_91d2e14d.x86_64                                                     2/4 
  Erasing          : npm-1:5.5.1-1.8.9.1.1.module_d4e9ce34.2.x86_64                                                      3/4 
  Erasing          : nodejs-1:8.9.1-1.module_d4e9ce34.x86_64                                                             4/4 
  Running scriptlet: nodejs-1:8.9.1-1.module_d4e9ce34.x86_64                                                             4/4 
  Verifying        : npm-1:3.10.10-1.6.12.0.1.module_91d2e14d.x86_64                                                     1/4 
  Verifying        : nodejs-1:6.12.0-1.module_91d2e14d.x86_64                                                            2/4 
  Verifying        : npm-1:5.5.1-1.8.9.1.1.module_d4e9ce34.2.x86_64                                                      3/4 
  Verifying        : nodejs-1:8.9.1-1.module_d4e9ce34.x86_64                                                             4/4 

Downgraded:
  nodejs.x86_64 1:6.12.0-1.module_91d2e14d                  npm.x86_64 1:3.10.10-1.6.12.0.1.module_91d2e14d                 

Complete!
[root@semimodular yum.repos.d]# 
```
