########
Loslassa
########

A simple way to generate static web pages with `Python <http://python.org>`_,
`reStructuredText <http://docutils.sourceforge.net/rst.html>`_,
`git <http://git-scm.com>`_ and `love <http://en.wikipedia.org/wiki/Love>`_ :)

**WARNING**

    **This is just a vague concept atm and serves me as a vehicle to play through**
    **the whole process of getting an open source project in the python**
    **ecosystem on the road - but I reallly hope this will turn into something useful**


Other important ingredients are the documentation generator
`sphinx <http://sphinx-doc.org>`_ and some other yet undisclosed tools.

==============
About the name
==============

**Loslassa** or **los lassa** means to let go and relax in
a german dialect called `Swabian <http://en.wikipedia.org/wiki/Swabian_German>`_
spoken in parts of South Germany. As I moved into this part of Germany in
2011 I came in direct contact with this dialect and I am still quite in
awe of it, but I really like it, so I thought I give my first open source
project a Swabian name :)

Anyway, when I came up with the idea to this project I went to my Yoga class
and my Swabian Yoga teacher always says "loslassa" whenever she wants us to
relax after some contortion she made us go through - so this is my favorite
part of the lessons :)

So in the true spirit of **Loslassa** I hope this little project helps you let go of your
preconceptions how static web pages have to be generated and you try the Loslassa way :).

===========
Basic Ideas
===========

::

    loslassa start <project name>

    in directory:
        loslassa build
        loslassa serve (with watcher that rebuilds after cheanges)
        loslassa push
        loslassa fetch
        loslassa build serve

Start locally. Creating a new project initializes a new git repository with the basix structure

Publishing it would clone the repository bare to the web space and set it to be origin from then on.

==========
Next Steps
==========

Flesh out the readme with the usage scenarios

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

Marrying bash/cmd.exe with python - plumbum:
    * http://plumbum.readthedocs.org/en/latest/
    * Might be better to use git bindings

=======
License
=======
I know, this is really important ... so after thinking long and hard and
consulting squillions of lawyers I decided to put this world changing project
under the `DBAD License <http://www.dbad-license.org>`_.
