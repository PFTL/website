Store Data in Your Python Applications Part 2
=============================================

:status: draft
:date: 2018-07-23
:author: Aquiles Carattino
:subtitle: Learn different ways of storing data in your projects
:header: {attach}tom-hermans-642319-unsplash.jpg
:tags: Data, Storing, sqlite, HDF5, ascii, json
:description: Learn different ways of storing data in your projects

Last week we have seen how to store data into plain text files that can be read by any editor and by other programs. We have also seen that if you separate your data with commas your file will be compatible with other programs, mainly spread sheets. One of the main limitations of this strategy is that if your data contains a comma, your file will not be readable anymore.

In this article we are going to discuss about encoding of data, basically to understand how come that what you save with Python can be read by a normal text editor or your web browser. We will also see that you can save space if you encode your data in the proper way. In the end what you will have is a clear picture of the difference between saving text files and binary data.

.. contents::

What does it really mean to save text files
-------------------------------------------
Last week you have seen different ways of saving text files. One of the most noticeable attributes is that those files can be opened with any basic text editor, you don't need Python to read them. This already should indicate that there is an underlying property that allows programs to share files.