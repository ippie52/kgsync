# Repository information
kgsync is a tool to synchronise multiple git repositories within a top-level git repository.

Whilst git does have the submodule command, I have often found it a little cumbersome for some tasks with multiple repositories. This tool is aimed to simplify the process somewhat for users by providing a minimalistic interface, but maintaining some flexibility.

Repositories are tracked using the kgsync tool, which keep track of changes using a manifest JSON file.

# Contents
* [Contents](#contents)
* [Installation](#installation)
 - [Linux](#linux)
 - [Windows](#windows)
* [Usage instructions](#usage-instructions)
* [Basic usage examples](#basic-usage-examples)
 - [Generating the initial manifest](#generating-the-initial-manifest)
 - [Removing repositories from the manifest](#removing-repositories-from-the-manifest)
 - [Adding repositories to the manifest](#adding-repositories-to-the-manifest)
 - [Updating the manifest](#updating-the-manifest)
 - [Synchronising repositories](#synchronising-repositories)
 - [Input and output files](#input-and-output-files)
  * [Generating and using a manifest not named ```manifest.json```](#generating-and-using-a-manifest-not-named-manifestjson)
  * [Dry-run tests](#dry-run-tests)
 - [Stash flag](#stash-flag)
 - [Minimal flag](#minimal-flag)

#Installation
## Linux
```kgsync``` is simply a python script. Feel free to place it into a directory and use it as is.

For ease, I use the following method:

### Clone the repository:
```user@ubuntu:~/git$ git clone https://github.com/ippie52/kgsync.git```

```
Cloning into 'kgsync'...
remote: Counting objects: 4, done.
remote: Compressing objects: 100% (4/4), done.
remote: Total 4 (delta 0), reused 4 (delta 0), pack-reused 0
Unpacking objects: 100% (4/4), done.
Checking connectivity... done.
```
### Create a soft link to the script in ```/usr/bin/```:
```user@ubuntu:~/git$ sudo ln -s ~/git/kgsync/kgsync /usr/bin/kgsync```

Now, I can use kgsync with all my repositories.

## Windows
As mentioned in the [Linux](#linux) section above, ```kgsync``` is just a python script, and so can be placed into any directory and called: ```python kgsync ... ```

If you wish to have an executable and are familiar with [py2exe](http://www.py2exe.org/), please feel free to convert the script using:

```python setup.py py2exe```

After which, the ```kgsync.exe``` executable should be available in the ```dist``` directory. You may then add the location of this to your local path.


# Usage instructions

```
Usage: kgsync [options] (repositories)

kgsync is a tool to synchronise multiple git repositories within a top-level
git repository.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -g, --generate        Generates a new manifest file (requires directory
                        argument -d).
  -a, --add             Adds a sub repository to the manifest file (requires
                        directory argument -d)
  -r, --remove          Removes a sub repository from the manifest file
                        (required directory argument -d).
  -u, --update          Updates the commit ID used for each repository to
                        match the current commit ID
  -o file.json, --output=file.json
                        Specifies the output file name of the manifest file
                        when generating, updating or amending.
  -i file.json, --input=file.json
                        Specifies the name of the input manifest file
  -m, --minimal         Minimalistic clone. Potentially beneficial for large
                        repositories (may be slower)
  -s, --stash           Stashes any changes before syncing, generating or
                        updating
  -d level, --debug=level
                        Sets the level of debug (default warning and above)

```

# Basic usage examples

For the usage examples, the following directory structure is assumed:
```
parent_repository/  <== The parent repository, in which the manifest will be created
├── afile           <-- Files tracked by parent_repository
├── bfile           <-- ...
├── cfile           <-- ...
├── .git            <-- parent_repository's .git folder
├── repo_1          <== The first git repository to track (origin https://example.com/1.git/)
│   ├── 1_file_a    <-- Files tracked by repo_1
│   ├── 1_file_b    <-- ...
│   ├── 1_file_c    <-- ...
│   └── .git        <-- repo_1's .git folder
├── repo_2          <== The second git repository to track (origin https://example.com/2.git/)
│   ├── 2_file_a    <-- Files tracked by repo_2
│   ├── 2_file_b    <-- ...
│   ├── 2_file_c    <-- ...
│   └── .git        <-- repo_2's .git folder
└── repo_3          <== The third git repository to track (origin https://example.com/3.git/)
    ├── 3_file_a    <-- Files tracked by repo_3
    ├── 3_file_b    <-- ...
    ├── 3_file_c    <-- ...
    └── .git        <-- repo_3's .git folder
```
## Generating the initial manifest
The manifest file contains all the information required to obtain a copy of all required sub-repositories, and should be tracked in git by your parent repository.

To quickly generate a manifest file (default name ```manifest.json```), for the above structure, where we want all three sub-repositories to be tracked, the following could be used:

```user@ubuntu:~/parent_repository$ kgsync -g repo_1 repo_2 repo_3```

Expected output:
```
INFO: Generating manifest: manifest.json
INFO: Successfully added repo_1
INFO: Successfully added repo_2
INFO: Successfully added repo_3
INFO: Writing to file: manifest.json
SUCCESS: Manifest file manifest.json generated.
```

Contents of the ```manifest.json``` file:
```
{
    "directories": {
        "repo_1": {
            "commit": "e9b2b670a6f286b89f7708a7dcf245302ab09c66",
            "modified": 0,
            "origin": "https://example.com/1.git/",
            "repo": "repo_1",
            "valid": true
        },
        "repo_2": {
            "commit": "a31cadb3232a48c2512445f99ec71bc0b3d7e24d",
            "modified": 0,
            "origin": "https://example.com/2.git/",
            "repo": "repo_2",
            "valid": true
        },
        "repo_3": {
            "commit": "166ddc331eefb3cdc6c0a0c693636160b6999ba4",
            "modified": 0,
            "origin": "https://example.com/3.git/",
            "repo": "repo_3",
            "valid": true
        }
    },
    "meta": {
        "version": 0.1
    }
}
```
## Removing repositories from the manifest
To remove repositories from the manifest, the following could be used:

```user@ubuntu:~/parent_repository$ kgsync -r repo_2 repo_3```

Expected output:
```
INFO: Removing from manifest: manifest.json
INFO: Removing repo_2 from the repository list
INFO: Removing repo_3 from the repository list
INFO: Writing to file: manifest.json
SUCCESS: Directories were successfully removed from manifest.json.
```

Contents of the ```manifest.json``` file:
```
{
    "directories": {
        "repo_1": {
            "commit": "e9b2b670a6f286b89f7708a7dcf245302ab09c66",
            "modified": 0,
            "origin": "https://example.com/1.git/",
            "repo": "repo_1",
            "valid": true
        }
    },
    "meta": {
        "version": 0.1
    }
}
```

## Adding repositories to the manifest
Adding repositories is a simple as removing them. To add the repositories removed in the previous section, the following could be used:

```user@ubuntu:~/parent_repository$ kgsync -a repo_2 repo_3```

Expected output:
```
INFO: Adding to manifest: manifest.json
INFO: Successfully added repo_2
INFO: Successfully added repo_3
INFO: Writing to file: manifest.json
SUCCESS: Directories were successfully added to manifest.json.
```

Contents of the ```manifest.json``` file:
```
{
    "directories": {
        "repo_1": {
            "commit": "e9b2b670a6f286b89f7708a7dcf245302ab09c66",
            "modified": 0,
            "origin": "https://example.com/1.git/",
            "repo": "repo_1",
            "valid": true
        },
        "repo_2": {
            "commit": "a31cadb3232a48c2512445f99ec71bc0b3d7e24d",
            "modified": 0,
            "origin": "https://example.com/2.git/",
            "repo": "repo_2",
            "valid": true
        },
        "repo_3": {
            "commit": "166ddc331eefb3cdc6c0a0c693636160b6999ba4",
            "modified": 0,
            "origin": "https://example.com/3.git/",
            "repo": "repo_3",
            "valid": true
        }
    },
    "meta": {
        "version": 0.1
    }
}
```
The above is now the same as the initial file generated.

## Updating the manifest
When the time comes to update the manifest to point a repository at a different commit, simply update the remote's content as required, then run the following:

```user@ubuntu:~/parent_repository$ kgsync -u```

Expected output:
```
INFO: Updating manifest: manifest.json
INFO: Updating data in repository repo_3
INFO: Updating data in repository repo_2
INFO: Updating data in repository repo_1
INFO: Writing to file: buh.json
SUCCESS: Repositories are up to date.
```

Contents of the ```manifest.json``` file:
```
{
    "directories": {
        "repo_1": {
            "commit": "e9b2b670a6f286b89f7708a7dcf245302ab09c66",
            "modified": 0,
            "origin": "https://example.com/1.git/",
            "repo": "repo_1",
            "valid": true
        },
        "repo_2": {
            "commit": "d4d06e18a0bd0725c57df3a08fb06153010d2713",
            "modified": 0,
            "origin": "https://example.com/2.git/",
            "repo": "repo_2",
            "valid": true
        },
        "repo_3": {
            "commit": "166ddc331eefb3cdc6c0a0c693636160b6999ba4",
            "modified": 0,
            "origin": "https://example.com/3.git/",
            "repo": "repo_3",
            "valid": true
        }
    },
    "meta": {
        "version": 0.1
    }
}
```
Noting that the SHA1 for repo_2 has been updated from ```a31cadb3232a48c2512445f99ec71bc0b3d7e24d``` to ```d4d06e18a0bd0725c57df3a08fb06153010d2713```.

## Synchronising repositories
This is the main function of the kgsync tool, and as such, this can be performed by simply calling ```kgsync``` without any arguments.

For this example, assume that a fresh clone of the parent repository has been performed:

```
user@ubuntu:~$ git clone http://example.com/parent.git/
user@ubuntu:~$ cd parent
user@ubuntu:~/parent$ kgsync
```

Expected output:

```
INFO: Synchronising repositories in manifest: manifest.json
INFO: Synchronising repository repo_3
INFO: Performing a full clone https://example.com/3.git/ into directory repo_3, please wait...
Cloning into 'repo_3'...
done.
INFO: Synchronising repository repo_2
INFO: Performing a full clone https://example.com/2.git/ into directory repo_2, please wait...
Cloning into 'repo_2'...
done.
INFO: Synchronising repository repo_1
INFO: Performing a full clone https://example.com/1.git/ into directory repo_1, please wait...
Cloning into 'repo_1'...
done.
SUCCESS: Synchronisation complete.
```

Now, the repository should contain all the remotes:

```
user@ubuntu:~/parent$ ls
manifest.json  repo_1  repo_2  repo_3
```

**Tip:** If you only wish to update a single repository, you may specify the repository by its directory name.

## Input and output files
From time-to time, you may wish to output to a different file name, or simply run a test without updating the original manifest file.

To do this, the ```input``` and ```output``` options become useful.

### Generating and using a manifest not named ```manifest.json```

To generate a manifest file called ```another.json```, simply use the ```-o``` (```--output```) flag, which names the output file.

```user@ubuntu:~/parent_repository$ kgsync -g -o another.json repo_1 repo_2```

**NOTE:** The ```-i``` (```--input```) options is not used when generating a manifest.

If we wish to update the new file ```another.json```, we would then need to use the ```-i``` (```--input```). By default, the input file will be modified.

```user@ubuntu:~/parent_repository$ kgsync -a -i another.json repo_3```

Expected output:

```
INFO: Adding to manifest: another.json
INFO: Successfully added repo_3
INFO: Writing to file: another.json
SUCCESS: Directories were successfully added to another.json.
```

The above example (using the ```input``` option) would also work with the ```update``` and ```remove``` commands.

### Dry-run tests
If you wish to test the outcome of your update, add or remove without affecting the original manifest file, you can specify both the input and the output as separate files, without worry of overwriting your original manifest file. During the operation, any warnings or errors can be checked and afterwards, the files can be compared to ensure the desired action has been carried out.

This will mostly be useful when dealing with multiple repositories which may contain local changes, although it may also be useful for generating another manifest for a branch or for testing.

For example, running an update and saving to another file:

```user@ubuntu:~/parent_repository$ kgsync -u -i another.json -o yet_another.json```

If there were some uncommitted changes in ```repo_2```, the following output would be expected:

```
INFO: Updating manifest: another.json
INFO: Updating data in repository repo_3
INFO: Updating data in repository repo_2
INFO: Updating data in repository repo_1
ERROR: Modifications present in repo_2. Please stash or commit these before continuing.
ERROR: There was a problem updating the manifest.
```

No new manifest would be created, and the input manifest would be left untouched.


If all changes in the repositories were committed, then the following would be expected:
```
INFO: Updating manifest: another.json
INFO: Updating data in repository repo_3
INFO: Updating data in repository repo_2
INFO: Updating data in repository repo_1
INFO: Writing to file: yet_another.json
SUCCESS: Repositories are up to date.
```

The new manifest ```yet_another.json``` would have been created, the original would be untouched, and a diff between the two should show something like this:

```
user@ubuntu:~/parent_repository$ diff another.json yet_another.json
11c11
<             "commit": "d4d06e18a0bd0725c57df3a08fb06153010d2713",
---
>             "commit": "a31cadb3232a48c2512445f99ec71bc0b3d7e24d",
```

## Stash flag

**NOTE:** Please use this feature with caution! Whilst your changes won't be deleted, they may be forgotten about.

This feature allows you to ignore any changes you may have locally, and stash them when running a command. A warning will be issued, and an attempt to stash will be made. Following which, it is up to you to handle the stashed changes.

For example, in the previous example where there were changes in ```repo_2```, which prevented the update command from succeeding, this is what would happen if the ```-s``` (```--stash```) option had been provided while the repository had local modifications:

```user@ubuntu:~/parent_repository$ kgsync -u -i another.json -o yet_another.json -s```

Example output:

```
INFO: Updating manifest: another.json
INFO: Updating data in repository repo_3
INFO: Updating data in repository repo_2
INFO: Updating data in repository repo_1
Saved working directory and index state WIP on (no branch): a31cadb Initial commit
HEAD is now at a31cadb Initial commit
WARNING: Stashed changes in repo_2
INFO: Writing to file: yet_another.json
SUCCESS: Repositories are up to date.
```

```kgsync``` will store the face that the repository had local changes, which may be useful to some maintainers. As we can see from the diff between ```another.json``` and ```yet_another.json```:

```
user@ubuntu:~/parent_repository$ diff another.json yet_another.json
11,12c11,12
<             "commit": "d4d06e18a0bd0725c57df3a08fb06153010d2713",
<             "modified": 0,
---
>             "commit": "a31cadb3232a48c2512445f99ec71bc0b3d7e24d",
>             "modified": 1,
```

## Minimal flag

The purpose of the ```-m``` (```--minimal```) flag is to reduce the overhead of larger git repositories by performing a shallow clone of the repository, and expanding it until the required commit is found.

**NOTE:** For smaller repositories, this is more than likely slower.

Assuming that ```repo_4``` is added to the manifest and happens to be an incredibly large repository, then in a fresh clone, the following is called:

```user@ubuntu:~/fresh_clone$ kgsync -m```

Example output:
```
INFO: Synchronising repositories in manifest: hlk.json
INFO: Synchronising repository repo_4
INFO: Performing minimal clone of https://exmaple.com/4.git/ into directory repo_4, please wait...
Cloning into 'repo_4'...
remote: Counting objects: 183, done.
remote: Compressing objects: 100% (170/170), done.
remote: Total 183 (delta 16), reused 101 (delta 7), pack-reused 0
Receiving objects: 100% (183/183), 261.02 KiB | 482.00 KiB/s, done.
Resolving deltas: 100% (16/16), done.
Checking connectivity... done.
INFO: Commit not found, expanding depth. This may take some time...
INFO: Synchronising repository repo_1
INFO: Performing minimal clone of https://exmaple.com/1.git/ into directory repo_1, please wait...
Cloning into 'repo_1'...
done.
INFO: Commit not found, expanding depth. This may take some time...
INFO: Synchronising repository repo_2
INFO: Performing minimal clone of https://exmaple.com/1.git/ into directory repo_2, please wait...
Cloning into 'repo_2'...
done.
INFO: Commit not found, expanding depth. This may take some time...
INFO: Synchronising repository repo_3
INFO: Performing minimal clone of https://exmaple.com/1.git/ into directory repo_3, please wait...
Cloning into 'repo_3'...
done.
SUCCESS: Synchronisation complete.
```

As can be seen above, all the repositories are minimally cloned, which may not be desirable. As mentioned in the synchronisation section, you can specify a particular repository to reduce the time taken to perform a fresh clone. For this example, you may wish to perform two syncs:


```user@ubuntu:~/fresh_clone$ kgsync -m repo_4```
```user@ubuntu:~/fresh_clone$ kgsync repo_1 repo_2 repo_3```
