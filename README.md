# Information for Connector Instructors

## Publishing Notebooks for ds8

The course text at http://data8.org/text contains INTERACT buttons which upload notebooks to students' accounts when clicked. If you would like to be able to upload notebooks in a similar fashion, please follow these instructions:

1. Create a git branch named **gh-pages** in your https://github.com/dsten/*discipline*-connector repository, where *discipline* is your connector. Files you create in that branch are accessible at http://data8.org/*discipline*-connector/.

1. Send a link of the following form to your students:

  https://ds8.berkeley.edu/hub/interact?file=http://data8.org/*discipline*-connector/filename.ipynb

You can put your notebooks into subdirectories within your repositories, in which case the parameter would become https://ds8.berkeley.edu/hub/interact?file=http://data8.org/*discipline*-connector/subdir/filename.ipynb.

For security reasons, ds8.berkeley.edu will only accept notebooks from http://data8.org/.
