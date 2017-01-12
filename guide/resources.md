# Managing resources and data on the cluster
This is a quick guide on how many resources we have on the cluster, and what considerations you should take in designing your course materials.

# General tips
* Run your code from start to finish in one go before pushing it to students. This ensures that it runs in a timely fashion, and that you aren't baking memory issues into the code itself.
* Always run the code on the cluster before distributing it, just in case you haven't accounted for some hardware or library restriction on the cluster.

# Libraries and packages
To install a new package that all students will have access to, create a new issue in the `connector-instructors` repo and flag the jupyterhub administrator (currently Ryan Lovett). Attach (or point to) a small notebook that uses this package. We'll try to integrate any additional libraries that your notebook specifies. The more lead time we have the better.

Alternatively, it is possible to install packages directly to the data8 cluster. The only trick is that it must be done to your *user* directory, which is generally not the default when using something like `pip`. If you get permissions errors when using `pip`, it's usually because you're trying to write to the base cluster directory, not your user directory.

> When we do update the single user server with new software, it requires that students stop and start their server.

# CPU restrictions
While CPU will restrict how fast your code runs, it's usually not the bottleneck on the cluster. Obviously you want to limit the complexity of the analyses you'd like students to run, and a good rule of thumb is to try and simplify analyses / datasets, and then discuss how they'd be scaled up. For example, running simple machine learning on in-memory data is probably fine. Fitting a multi-layer neural network on multiple batches of data is probably going to take a long time.

# Memory restrictions
Memory management is tricky on the cluster. Currently there is 2GB for each student's session (though this may be different in future iterations of the class). In the top-right of notebooks you will find the amount of memory currently used out of the total amount available to students.

## What if I run out of memory?
* If you run out of memory, the python kernel will automatically restart. This can be frustrating for students because they don't get any kind of message that tells them memory is the problem. It's a good idea to let them know ahead of time.
* If restarting the kernel and re-running the code doesn't help, then usually there is another notebook open from a previous session. Go to the "running notebooks" page, and close anything you're not using right now.
* If all other notebooks are closed and you're *still* running out of memory, then log out and log back in to your jupyterhub account. This will close your session and then start a new one. There have been reports of stray memory being taken up by python even though processes have finished running.

# Storing data and I/O
If you've got data that you want students to use, you have 3 options:

1. Package the data with a github repository. (works if the data is relatively small and won't be modified)
2. Host the data online somewhere and have students download it. (useful for medium-sized data, and often works well with a helper function you write, e.g. `download_dataset(url)`)
3. Host the data on the cluster itself, in a shared directory. For this, speak with the cluster administrator to set up a read-only folder that you can direct students towards. (this is best for large datasets on the order of several GB)
