# About
Sitenode is a simple framework to create fast content driven websites for
blogs or layouting the whole page.

it is abstract and simple for a reason, it should not be taken as an all
knowing api. copy parts or the whole thing if you need and modify it to
your needs.

But used wisely, it can take away some pain in the webapp business, since it
offers you to use pages from the database, as well as easy setups for blogs

# Installation

get the app into your pythonpath.

settings.py:

urls.py:
include in urls e.g.:
    (r'^nodes/', include('sitenode.urls')),
includes the standard setup.

that should be it.

note:
it is prefered practice to the user to use absolute imports of the needed views 
in the project, since thats more declarative configuration, which is superior.
for this of course, you have to dig into the software to understand what it does
sitenode is not a big thing, so that shouldnt take long.


# Changelog
SiteNode was usually installed as an app inside the project in older versions,
but this version should work as a standalone 3rdparty app.

the Gdjet extensions used are now bundled in jsonstore.py

