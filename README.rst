Loslassa
========

This project started with a problem, bad solutions and a question.

**Problem** Several members of my family who know how to use a computer but don't speek HTML, CSS and such needed a "a website".

**Bad solutions** (in my opinion) are the gazillions of WebSiteCreatorThingies (TM) that are trying to abstract away the actual generation of the web pages in ways that it gives you the illusion of power and freedom long enough to be too committed to switch to something better when you find out that it simply not does what you want it to do.

**Question** If i create something that is based on the way I create the documentation for my Python projects and add a friendly command line interfaca for all essential operations: is it possible to make the non-Nerds in my family actually like creating their websites like that?

What is needed?
---------------

* Easy to install
* Works on Windows and Linux
* Good examples to get started
* Easy to administrate
* Offers a short feedback loop
* Gives helpful error messages
* publishing content is easy

Check it out
============

This is early days: creation and publishing functionality
does not actually exist yet ... but you can play with it already:

#. ``pip install loslassa``
#. Manually copy the example_project folder from dist-packages to your home
#. Change into example_project/source
#. ``loslassa play``
#. Point your browser to http://localhost:8080

Now you can edit the rst files or conf.py in the example project
and check the changes in the browser.

About the name
==============

**Loslassa** or **los lassa** means to let go and relax in a german dialect
called `Swabian <http://en.wikipedia.org/wiki/Swabian_German>`_
spoken in parts of South Germany. As I moved into this part of Germany in
2011 I came in direct contact with this dialect and I am still quite in
awe of it, but I really like it ... or at least I am really trying very hard to
like it - so I thought I give my first open source project a Swabian name.

Anyway, when I came up with the idea to this project I went to my Yoga class
and my Swabian Yoga teacher always says "loslassa" whenever she wants us to
relax after some contortion she made us go through - so this is my favorite
part of the lessons.

So in the true spirit of **Loslassa** I hope this little project helps
you let go of your preconceptions how web pages have to be
created and you try the Loslassa way ;).

Inspiration
===========

README driven development:
    * http://tom.preston-werner.com/2010/08/23/readme-driven-development.html

Nice command line usage - heroku:
    * https://devcenter.heroku.com/articles/python
    * https://devcenter.heroku.com/articles/quickstart

Layering of functionality - git:
    * plumbing/porcelain paradigm
