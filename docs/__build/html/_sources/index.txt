######################
Loslassa Documentation
######################

========
Workflow
========

Start
=====

.. code-block:: bash

    loslassa start <relative or absolute path to>project

e.g. if you are in your home folder at C:\Users\maedle and you want
to start a project there::

    loslassa gugga


How it works
------------

Following a slightly adapted hub-prime-clones pattern
from http://joemaller.com/990/a-web-focused-git-workflow/ and http://danbarber.me/using-git-for-deployment/

Have a look at this: https://github.com/gerhard/deliver or: http://mikeeverhart.net/git/using-git-to-deploy-code/ or: http://toroid.org/ams/git-website-howto or: http://danielmiessler.com/study/git/#website

The pattern described there is only working for pure HTML/Javascript projects - a loslassa project though consists of the sources and a build. As the project as a whole should be under source control ans movable, the deployment has to be adjusted in so far as the web root has to point to the HTML part of the build, but the rest of the project has to be uploaded as well. Beside from that the clones-prime-hub scheme fits nicely for this use case.

Lets say you are on the commandline in ~/projects
(where "~" is your home directory - wherever that might be) and you want
to start a new loslassa project called gugga (swabian word for bag). This
is what happens under the hood:

**LOCAL: create prime**

.. code-block:: bash

    mkdir gugga
    cp -r /path/to/loslassa/projects/skeleton/* gugga
    cd gugga
    git init
    git add .
    git commit -m "initialized gugga"

Now the remote comes into play:

As example we'll say your host is called maedle.net ...

**REMOTE: create bare git repo to hold the hub**

.. code-block:: bash

    ssh user@maedle.net mkdir /path/to/hub/repos/gugga.git
    cd gugga.git
    git --bare init

**LOCAL: push prime to hub**

.. code-block:: bash

    cd ~/www
    git remote add hub ~/site_hub.git
    git push hub master

Creates a new project with a basic structure and configuration
similar to sphinx-quickstart only simpler and tailored to only HTML output.


Play
''''

Playing with the source and create your page. Add content and see the
changes right away thanks to local server with automatic
rebuild of the web pages::

    cd */path/to/project*
    loslassa play

Starts a local development server reachable on http://localhost:8080.
All files in project folder are being watched and if something changes
the project is rebuild.

Publish
'''''''
**not implemented yet**

This part is a bit vague still but basically it should simply push the
generated pages to the server, by maintaining them in a git repository

First time publishing would clone the repository bare to the web space and
set it to be origin from then on
... or summin like that, didn't think that through yet::

    cd */path/to/project*
    loslassa loslassa

Customize
'''''''''
This is not thought out yet, but I imagine that additional customization
can be done easily by expanding the settings in the sphinx conf.py and
do more involved stuff via sphinx extensions.




Hello this is some random content to have something to work with and to
test the workflow and functionality of `Loslassa <https://github.com/obestwalter/loslassa>`_

.. toctree::
    :maxdepth: 2

    news
    about
    inner_folder/file_in_inner_folder

====================
Second level heading
====================

Second level here

Third level heading
===================

Third level here.

Fourth level heading
--------------------

quite deep ...

Fifth level heading
'''''''''''''''''''

Even deeper


