# Workflow

Here's a rough overview of the workflow we use in the main class. We'll base the
rest of this tutorial on these steps. Feel free to add/remove steps as fit for
your course.

Click a link to jump to that section of this guide.

1. [Create a notebook.](#creating-notebooks)
2. [Push the notebook to Github.](#pushing-your-notebooks-to-github)
3. [Distribute the notebook to students.](#distributing-notebooks)
4. [Students work on notebooks.](#student-work)
5. [Students submit their completed notebooks to you.](#student-submission)

[data-8]: https://github.com/data-8
[interact]: http://data8.org/text/1_data.html#example-plotting-the-classics

Here's a diagram of the steps.

![connector-instructor](https://cloud.githubusercontent.com/assets/2468904/12474089/f8ac3700-bfcc-11e5-988a-5f686788c4fc.png)

Let's talk in more detail about each of these steps.

# Creating notebooks

![step1](https://cloud.githubusercontent.com/assets/2468904/12474029/6d17c1be-bfcc-11e5-80f8-fbc7ff25aa57.png)

This guide is intended for those with **no prior experience** with Jupyter,
`git`, or Github. Feel free to develop your own workflow if you know what you're
doing.

## Setting up your repo

First, visit https://data8.berkeley.edu/ and log in. You should see a screen that
looks something like the one below. Click the "Terminal" button as marked:

![screenshot 2016-01-05 17 54 11](https://cloud.githubusercontent.com/assets/2468904/12132922/70ea3a22-b3d5-11e5-983a-6cd2aae3b10f.png)

You should see a screen that looks like this:

![screenshot 2016-01-05 17 56 14](https://cloud.githubusercontent.com/assets/2468904/12132944/a2dfd758-b3d5-11e5-920b-14b622d4efec.png)

This is a terminal that allows you to run commands. Type the following into the
terminal:

    git clone https://github.com/data-8/<repo_name>

Where the `<repo_name>` is the name of the repository for your connector. The
repository names are listed at https://github.com/data-8. For example, if you
are the instructor for the Health connector, you'd write:

    git clone https://github.com/data-8/health-connector

## Adding your content

After this step, you should be able to see your connector's folder at
https://data8.berkeley.edu/ . **Once your folder is there, you do not have to
repeat the steps in the Setting up your repo section.**

Click on your folder to go inside that directory.

![screenshot 2016-01-05 18 02 28](https://cloud.githubusercontent.com/assets/2468904/12133071/a1a3be9e-b3d6-11e5-9efa-74cffcaba1e0.png)

You should see a screen like the one below. Click the button marked by the arrow
in the below image to create a new notebook. You may create a notebook in any
folder as long as the folder is in your connector folder. That is, in the
above example you may create a notebook in `~/health-connector/foo/bar/`, but
not `~/some_other_folder`.

![screenshot 2016-01-05 18 04 33](https://cloud.githubusercontent.com/assets/2468904/12133094/d7786e98-b3d6-11e5-8118-3a82bec33492.png)

Fill in the notebook with your content.

**Example notebooks:** For examples of notebooks, you can see
the [table demos][demos] or find all raw notebooks for the textbook [here](https://github.com/data-8/textbook/tree/gh-pages/notebooks).The main class uses notebooks for lectures, labs, and
projects. In addition,

**Adding datasets:** If you have datasets/other needed files to distribute or
use in a notebook, you can upload them using the button as labeled below:

![screenshot 2016-01-19 22 15 32](https://cloud.githubusercontent.com/assets/2468904/12441280/429ce95a-befa-11e5-8e61-869452920490.png)

[demos]: https://github.com/deculler/TableDemos
[textbook]: http://data8.org/text/

## Pushing your notebooks to Github

![step2](https://cloud.githubusercontent.com/assets/2468904/12474031/6d1a12e8-bfcc-11e5-83e4-e2dc5b420e6b.png)

Once your notebook is ready for distribution, you must to upload it to Github so
that it can publicly accessed online.

For those who are familiar with `git` and Github, push your file(s) to the
`gh-pages` of your repo. The file(s) should then be available at
`http://data8.org/<repo_name>/<file_name>`.

If you are not familiar with `git`/Github, follow the instructions below.

1. On data8.berkeley.edu, open a new terminal. (New -> Terminal)
2. Type in

        cd <repo_name>

    Where the `<repo_name>` is the name of your repository (eg.
    `health-connector`).

3. Type

        git status

    You should see something that lists the files you've changed. If your
    changed files don't show up, ensure that they are in your repo's folder.

4. Type the following commands:

        git add -A
        git commit -m 'Update'
        git push origin gh-pages

    If you run into something that looks like:

        ERROR: Permission to data-8/some-connector.git denied

    Contact Sam. This means that you don't have the right access to Github.

5. Verify that you can access your file by visiting
`http://data8.org/<repo_name>/<file_name>`. For example, for the `Demo2.ipynb`
file in the `health-connector` repo you'd use the link:
http://data8.org/health-connector/Demo2.ipynb .

If the last step doesn't work, double the check the steps above and contact us
on a persisting issue.

# Distributing notebooks

![step3](https://cloud.githubusercontent.com/assets/2468904/12474090/f9d45bb2-bfcc-11e5-8884-1ec12945f828.png)

Once your notebook is uploaded to Github, you can give your students links that
work like the Interact buttons in the textbook.

**Automatically creating a link** can be done with [this jupyter notebook](http://mybinder.org/repo/choldgraf/connector-instructors/ntbk/url_to_interact.ipynb). This will open a mini python session along with a function we've written to make creating interact links easy.

Alternatively, manually create a link like the following:

    https://data8.berkeley.edu/hub/interact?repo=<repo_name>&path=<path_name>

Where the `<repo_name>` is replaced with your repo name and `<path_name>` is
replaced with the path to a file or folder in the repo.

For example, if you have a working link of
http://data8.org/health-connector/Demo2.ipynb, the link you'd give students is:

    https://data8.berkeley.edu/hub/interact?repo=health-connector&path=Demo2.ipynb

Any student that visits this link will end up with their own copy of the
`Demo2.ipynb` file in a folder called `health-connector` their
data8.berkeley.edu account. You can repeat this for any file, not just
notebooks.

**I want to push a folder of content to students.** You can! If you have a
folder called `datasets` in the `health-connector` repo, you'd give students:

    https://data8.berkeley.edu/hub/interact?repo=health-connector&path=datasets

**I made a typo and want students to get an updated version.** Sure! If you
update a file, students can grab the update by visiting the original link again.

Note that in some cases an update would conflict with students' work (eg.
updating a notebook that students have filled out). In such a case, the system
will give up trying to update the file in favor of preserving the students'
work.

**A student messed up his work. Can he/she start over?** Certainly. Have the
student delete or rename the bad file/folder, then visit the link again. The
original file/folder will appear good as new!

# Student work

![step4](https://cloud.githubusercontent.com/assets/2468904/12474033/6d1d97ce-bfcc-11e5-8fb5-373c31c034b2.png)

You can use notebooks as a supplement to a lecture. For example, [here's a cool
notebook about probability][prob-nb]. Here's [a notebook we use to explore
literature][books-nb] in the [first chapter of the textbook][ch1].

[prob-nb]: http://nbviewer.jupyter.org/url/norvig.com/ipython/Probability.ipynb
[books-nb]: https://github.com/data-8/textbook/blob/gh-pages/notebooks/Books.ipynb
[ch1]: https://ds8.gitbooks.io/textbook/content/chapter1/example-plotting-the-classics.html

You can also use notebooks as assignments (the Data 8 class does both). You can
check out [the notebook we use for Lab 1 for Data 8][lab1] as an example of
this.

[lab1]: https://github.com/data-8/data8assets/blob/master/labs/lab01/lab01.ipynb

As you can see from the lab, we have cells that the students fill in. You can
make notebooks like this as well and distribute them to students in the same way
as detailed above.

In that example above, we give Data 8 students this link to get the lab (and its
related files):

    https://data8.berkeley.edu/hub/interact?repo=data8assets&path=labs/lab01

# Student submission

![step5](https://cloud.githubusercontent.com/assets/2468904/12474032/6d1a431c-bfcc-11e5-9944-e150c2277eef.png)

As of right now we don't have an easy way for students to submit
their work programmatically. You can accept submissions through email, bCourses,
or otherwise.

Students are currently able to download their notebooks off their
data8.berkeley.edu accounts in multiple formats, including `.pdf`, `.py`, and
`.ipynb`. They can download a notebook by opening it, turning Edit mode **on**,
then navigating to File -> Download as -> Format of choice.

An easy way to collect work is for students to export a notebook as a PDF file
and then submit to bCourses. We have autograding for Data 8 but it requires set
up. Let us know if you'd like to learn how to set that up.