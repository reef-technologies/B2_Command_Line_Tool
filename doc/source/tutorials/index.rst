#########################################
Tutorials
#########################################


***********************
Installation
***********************

To continue with any of the tutorials below, you must install B2 CLI. Detailed instructions can be found here
:doc:`./installation`.

***********************
Authorization
***********************

After signing in to `B2 Cloud Storage website <https://www.backblaze.com/cloud-storage>`_ generate a new Master
Application Key from the "Application Keys" view.

.. image:: ./generating_keys.png

Copy the presented `keyId` and `applicationKey` and use them in the following command:

.. code-block:: shell

    B2_APPLICATION_KEY_ID=keyId B2_APPLICATION_KEY=applicationKey b2 authorize-account

after that operation, your CLI tool is authorized and all following commands will operate in the context of
this account.

**********************************************
Buckets
**********************************************

Before you start uploading and downloading objects (files) you must create a bucket.

.. code-block:: shell

    b2 create-bucket pictures-of-toads allPrivate

NOTE: bucket name has to be globally unique, otherwise you will get an error. For the sake of this tutorial we only
focus on private buckets.

***********************
simple upload
***********************

Now, on any machine that ran :code:`b2 authorize-account` with the same key you can upload a file to
:code:`pictures-of-toads`:

.. raw:: html

    <div class="tab">
    <button class="tablinks" onclick="unfoldCodeSnippet(event, 'WebUI')">WebUI</button>
    <div class="dropdown">
    <button class="tablinks dropbtn">Command line</button>
    <div class="dropdown-content">
        <button class="tablinks" onclick="unfoldCodeSnippet(event, 'B2 CLI')">B2 CLI</button>
        <button class="tablinks" onclick="unfoldCodeSnippet(event, 'AWS CLI')">AWS CLI</button>

    </div>
    </div>

    <div class="dropdown">
    <button class="tablinks dropbtn">SDK</button>
    <div class="dropdown-content">
        <button class="tablinks" onclick="unfoldCodeSnippet(event, 'b2sdk')">b2sdk</button>
        <button class="tablinks" onclick="unfoldCodeSnippet(event, 'boto3')">boto3</button>

    </div>
    </div>
    </div>

    <script>
    function unfoldCodeSnippet(evt, language) {
      var i, tabcontent, tablinks;
      tabcontent = document.getElementsByClassName("tabcontent");
      for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
      }
      tablinks = document.getElementsByClassName("tablinks");
      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
      }
     snippets = document.querySelectorAll(`[data-language="${language}"]`);
     for (i = 0; i < snippets.length; i++) {
        snippets[i].style.display = "block";
     }
      evt.currentTarget.className += " active";
    }
    </script>


    <div class="snippet-holder">
        <div data-language="WebUI" class="tabcontent">
          some instructions will go here
        </div>

        <div data-language="B2 CLI" class="tabcontent">
              <div class="highlight-shell notranslate"><div class="highlight"><pre><span></span>b2<span class="w"> </span>upload-file<span class="w"> </span>pictures-of-toads<span class="w"> </span>/home/todd/pictures/fire-bellied-toad.png<span class="w"> </span>fire-bellied-toad.png
                </pre></div></div>
        </div>

        <div data-language="AWS CLI" class="tabcontent">
          AWS CLI
        </div>

        <div data-language="b2sdk" class="tabcontent">
          b2sdk
        </div>

        <div data-language="boto3" class="tabcontent">
          boto3
        </div>
    </div>


.. code-block:: python

    import b2sdk
    b2sdk.dupa("a", 7)


.. code-block:: shell

    b2 upload-file pictures-of-toads /home/todd/pictures/fire-bellied-toad.png fire-bellied-toad.png

this will create an object that users of your account can download.


***********************
upload to a directory
***********************

B2 objects aren't **exactly** stored in directories, but for all practical purposes you can use slashes in file paths as
if they were

.. code-block:: shell

    b2 upload-file pictures-of-toads /home/todd/pictures/fire-bellied-toad.png indo-european-toads/fire-bellied-toad.png

***********************
simple download
***********************

Downloading is as simple as

.. code-block:: shell

    b2 download-file-by-name pictures-of-toads fire-bellied-toad.png /home/fred/pictures/fire-bellied-toad.png


***********************
listing files
***********************

For seeing what files are already uploaded to a bucket, use the :code:`ls` command:

.. code-block:: shell

    b2 ls pictures-of-toads

you will see:

.. code-block:: shell

    fire-bellied-toad.png
    indo-european-toads/

if you need to know the contents of a directory, you can specify it

.. code-block:: shell

    b2 ls pictures-of-toads indo-european-toads


.. code-block:: shell

    indo-european-toads/fire-bellied-toad.png


Or even browse everything in one go:

.. code-block:: shell

    b2 ls pictures-of-toads --recursive

.. code-block:: shell

    fire-bellied-toad.png
    indo-european-toads/fire-bellied-toad.png


***********************
reupload
***********************

If you happen to upload a file again (with the same name in the same bucket):

.. code-block:: shell

    b2 upload-file pictures-of-toads /home/todd/pictures/fire-bellied-toad-v2.png fire-bellied-toad.png

you will only see the new one when listing files:

.. code-block:: shell

    b2 ls pictures-of-toads

you will see:

.. code-block:: shell

    fire-bellied-toad.png
    indo-european-toads/

also the new file will be downloaded if you try it:

.. code-block:: shell

    b2 download-file-by-name pictures-of-toads fire-bellied-toad.png /home/fred/pictures/fire-bellied-toad.png

but the "old version" is not gone (unlike on local drive). B2 Cloud Storage holds versions of files. If you "reupload"
a file, the new version "covers" the old one, but the old one can still be accessed:

.. code-block:: shell

    b2 ls pictures-of-toads --versions --long

.. code-block:: shell

   4_z7786dd31f6631c2a7cc8071c_f410587b5929a76ac_d20230921_m195738_c000_v0001061_t0047_u01695326258129  upload  2023-09-21  19:57:38          5  fire-bellied-toad.png
   4_z7786dd31f6631c2a7cc8071c_f402fafdefdfb97f9_d20230921_m191948_c000_v0001049_t0047_u01695323988977  upload  2023-09-21  19:19:48          5  fire-bellied-toad.png
                                                                                  -       -           -         -          0  indo-european-toads/

.. code-block:: shell

    b2 ls download-file-by-id 4_z7786dd31f6631c2a7cc8071c_f402fafdefdfb97f9_d20230921_m191948_c000_v0001049_t0047_u01695323988977 /home/fred/pictures/fire-bellied-toad.png

(Notice how `bucket_name` is not specified for this download operation, that's because and `id` uniquely identifies
a file in B2 Cloud Storage).

Because the "old" file is still accessible, it still incurs storage costs.

***********************
directory upload
***********************

There is a separate command for uploading directories

.. code-block:: shell

    b2 sync /home/fred/pictures/ b2://pictures-of-toads/some-directory/


***********************
directory download
***********************

As well as for downloading

.. code-block:: shell

    b2 sync b2://pictures-of-toads/some-directory/ /home/fred/pictures/


***********************
hiding files
***********************

Hiding files allows for making them invisible to `ls` and `sync` commands, while leaving the ability to download them
by id.

.. code-block:: shell

    b2 hide-file pictures-of-toads fire-bellied-toad.png

***********************
deleting files
***********************
It is possible to irreversibly delete a file, though that requires fetching it's `id` first:

.. code-block:: shell

    b2 delete-file-version fire-bellied-toad.png 4_z7786dd31f6631c2a7cc8071c_f402fafdefdfb97f9_d20230921_m191948_c000_v0001049_t0047_u01695323988977

*********************************************************************
deleting buckets
*********************************************************************




***********************
key creation
***********************

