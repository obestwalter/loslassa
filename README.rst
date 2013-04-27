########
Loslassa
########

A simple way to create web pages with `Python <http://python.org>`_,
`reStructuredText <http://docutils.sourceforge.net/rst.html>`_,
`git <http://git-scm.com>`_ and `love <http://en.wikipedia.org/wiki/Love>`_ :)

Other important ingredients:
    * `sphinx <http://sphinx-doc.org>`_  the documentation generator
    * simple reloading development server based on code from
      `Werkzeug  <http://www.pocoo.org/projects/werkzeug/#werkzeug>`_
    * `Plumbum <http://plumbum.readthedocs.org/en/latest/>`_ for convenient shell access
    * Permissive `BSD License <https://en.wikipedia.org/wiki/BSD_licenses>`_

============
Check it out
============

This is early days, so the proper workflow and publishing functionality
does not actually exist yet ... but you can play around with it already:

.. sourcecode:: bash
    $ [sudo] pip install loslassa

In an interactive shell:

>>> from loslassa.main import main
>>> main()

Point your browser to http://localhost:8080

Edit the rst files or conf.py in ``example_project``

Check the changes in the browser.

==========
Basic Idea
==========

If you want to create a simple web page without having to bother about
HTML, CSS, Javascript and all that, but don't want to suffer through those
browserbased website creatorthingies there is an alternative:
work locally with simple text files, let some clever system (sphinx) generate
the HTML and Javascript and then push the results online.

The basic workflow is inspired by the way how developing for example a
`flask <http://flask.pocoo.org/>`_ web application works: a local server runs in the
background while you edit your files and it reloads the changes as soon as they
happen. This makes it very easy to make quick changes and see the
results right away. Any errors or problems are logged to the console or are
shown right in the HTML output.

========
Workflow
========

Start
=====

::

    loslassa start */path/to/project*

Creates a new project with a basic structure and configuration
similar to sphinx-quickstart only simpler and tailored to only HTML output.

Play
====
Playing with the source and create your page. Add content and see the
changes right away thanks to local server with automatic rebuild of the web pages::

    cd */path/to/project*
    loslassa play

Starts a local development server reachable on http://localhost:8080.
All files in project folder are being watched and if something changes
the project is rebuild.

Publish
=======
This part is a bit vague still but basically it should simply push the
generated pages to the server, by maintaining them in a git repository

First time publishing would clone the repository bare to the web space and
set it to be origin from then on ... or summin like that, didn't think that through yet::

    cd */path/to/project*
    loslassa loslassa

Customize
=========

This is not thought out yet, but I imagine that additional customization
can be done easily by expanding the settings in the sphinx conf.py and
do more involved stuff via sphinx extensions.

==============
About the name
==============

**Loslassa** or **los lassa** means to let go and relax in
a german dialect called `Swabian <http://en.wikipedia.org/wiki/Swabian_German>`_
spoken in parts of South Germany. As I moved into this part of Germany in
2011 I came in direct contact with this dialect and I am still quite in
awe of it, but I really like it ... or at least I am really trying very hard to
 like it - so I thought I give my first open source project a Swabian name.

Anyway, when I came up with the idea to this project I went to my Yoga class
and my Swabian Yoga teacher always says "loslassa" whenever she wants us to
relax after some contortion she made us go through - so this is my favorite
part of the lessons.

So in the true spirit of **Loslassa** I hope this little project helps you let go of your
preconceptions how web pages have to be created and you try the Loslassa way ;).

===========
Inspiration
===========

README driven development:
    * http://tom.preston-werner.com/2010/08/23/readme-driven-development.html

Nice command line usage - heroku:
    * https://devcenter.heroku.com/articles/python
    * https://devcenter.heroku.com/articles/quickstart

Layering of functionality - git:
    * plumbing/porcelain paradigm
