#########################################
Tutorials
#########################################

.. raw:: html

    <script>
    function unfoldCodeSnippets(evt, language) {
      var elementToKeepInPlace = null;
      var initialPosition = null;
      if (evt) {
          elementToKeepInPlace = evt.srcElement
          if (elementToKeepInPlace.classList.contains('dropdown-item')) {
              elementToKeepInPlace = elementToKeepInPlace.parentNode.parentNode.getElementsByTagName('button')[0];
          }
          initialPosition = elementToKeepInPlace.getBoundingClientRect().y;
      }

      var i, tabcontent, tablinks;
      tabcontent = document.getElementsByClassName("tabcontent");
      for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
      }

      top_level_selectors = document.getElementsByClassName("top-level-selector");
      for (i = 0; i < top_level_selectors.length; i++) {
        top_level_selectors[i].className = top_level_selectors[i].className.replace("btn-primary", "btn-secondary");
        if (top_level_selectors[i].originalText) {
              top_level_selectors[i].textContent = top_level_selectors[i].originalText;
          }
      }

     snippets = document.querySelectorAll(`div[data-language="${language}"]`);
     for (i = 0; i < snippets.length; i++) {
        snippets[i].style.display = "block";
     }
     buttons = document.querySelectorAll(`button[data-language="${language}"]`);
     for (i = 0; i < buttons.length; i++) {
        buttons[i].className = buttons[i].className.replace("btn-secondary", "btn-primary");
        if (buttons[i].classList.contains('dropdown-item')) {
            dropdown_parent = buttons[i].parentNode.parentNode.getElementsByTagName('button')[0]
            dropdown_parent.className = dropdown_parent.className.replace("btn-secondary", "btn-primary");
            if (!dropdown_parent.originalText) {
                      dropdown_parent.originalText = dropdown_parent.textContent;
            }
            dropdown_parent.textContent += ` (${language})`
            }
     }
    if (evt) {
        window.scrollBy(0, - initialPosition + elementToKeepInPlace.getBoundingClientRect().y);
    }
     //if (evt != null) {
    //  evt.currentTarget.className += " active";
    //}
    }
    window.onload = function () {
        unfoldCodeSnippets(null, "WebUI");
    };
    </script>



***********************
Installation
***********************

To continue with any of the tutorials below, you must install your tool of choice. You can find short
installation instructions below.

.. raw:: html


        <nav class="navbar navbar-expand-lg navbar-light bg-light"
             style="padding-left: 8px; background-color: #cccccc63; border: 1px solid #ccc;">

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <button type="button" class="top-level-selector btn btn-secondary" onclick="unfoldCodeSnippets(event, 'WebUI')" data-language="WebUI">WebUI</button>
            <div class="btn-group btn-secondary" style="margin-left: 4px;">
                <button type="button" class="top-level-selector btn btn-secondary dropdown-toggle" data-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">
                    Command line
                </button>
                <div class="dropdown-menu">
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'B2 CLI')" data-language="B2 CLI">B2 CLI</a>
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'AWS CLI')" data-language="AWS CLI">AWS CLI</a>
                </div>
            </div>
            <div class="btn-group btn-secondary" style="margin-left: 4px;">
                <button type="button" class="top-level-selector btn btn-secondary dropdown-toggle" data-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">
                    SDK
                </button>
                <div class="dropdown-menu">
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'b2-sdk-python')" data-language="b2-sdk-python">b2-sdk-python</a>
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'boto3')" data-language="boto3">boto3</a>
                </div>
            </div>
        </div>
    </nav>

        <div data-language="WebUI" class="tabcontent">

No installation required.

.. raw:: html

    </div>
    <div data-language="B2 CLI" class="tabcontent">


.. code-block:: shell

    pip install b2


.. raw:: html

    </div>
    <div data-language="AWS CLI" class="tabcontent">

Follow instructions here: `https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
<https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html>`_

.. raw:: html

    </div>
    <div data-language="b2-sdk-python" class="tabcontent">

.. code-block:: shell

    pip install b2sdk


.. raw:: html

    </div>
    <div data-language="boto3" class="tabcontent">


.. code-block:: shell

    pip install boto3

.. raw:: html

    </div>

***********************
Authorization
***********************

After signing in to `B2 Cloud Storage website <https://www.backblaze.com/cloud-storage>`_ go to keys
"Application Keys" view.

.. image:: ./key_creation_1.png

Hit "Add a New Application Key" and fill out the details (just the name, for the sake of this tutorial).

.. image:: ./key_creation_2.png

Take note of the presented `keyId` and `applicationKey`.

.. raw:: html


        <nav class="navbar navbar-expand-lg navbar-light bg-light"
             style="padding-left: 8px; background-color: #cccccc63; border: 1px solid #ccc;">

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <button type="button" class="top-level-selector btn btn-secondary" onclick="unfoldCodeSnippets(event, 'WebUI')" data-language="WebUI">WebUI</button>
            <div class="btn-group btn-secondary" style="margin-left: 4px;">
                <button type="button" class="top-level-selector btn btn-secondary dropdown-toggle" data-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">
                    Command line
                </button>
                <div class="dropdown-menu">
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'B2 CLI')" data-language="B2 CLI">B2 CLI</a>
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'AWS CLI')" data-language="AWS CLI">AWS CLI</a>
                </div>
            </div>
            <div class="btn-group btn-secondary" style="margin-left: 4px;">
                <button type="button" class="top-level-selector btn btn-secondary dropdown-toggle" data-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">
                    SDK
                </button>
                <div class="dropdown-menu">
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'b2-sdk-python')" data-language="b2-sdk-python">b2-sdk-python</a>
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'boto3')" data-language="boto3">boto3</a>
                </div>
            </div>
        </div>
    </nav>

        <div data-language="WebUI" class="tabcontent">

No authorization, past the login screen, required.

.. raw:: html

    </div>
    <div data-language="B2 CLI" class="tabcontent">


.. code-block:: shell

    B2_APPLICATION_KEY_ID=keyId B2_APPLICATION_KEY=applicationKey b2 authorize-account
    # After this operation, your CLI tool is authorized and
    # all following commands will operate in the
    # context of this account.


.. raw:: html

    </div>
    <div data-language="AWS CLI" class="tabcontent">

.. code-block:: shell

    aws configure --profile b2tutorial
    # fill in the prompting inputs as follows:
    # AWS Access Key ID [None]: keyId
    # AWS Secret Access Key [None]: applicationKey
    # Default region name [None]:
    # Default output format [None]: json
    aws configure --profile b2tutorial set default.s3.signature_version s3v4

In order to interact with B2 using :code:`aws` CLI you will need to provide the :code:`--profile` and
:code:`--endpoint-url` parameters with each invocation, e.g.

.. code-block:: shell

    aws –-profile b2tutorial --endpoint-url https://s3.us-west-004.backblazeb2.com s3api list-buckets

To get your :code:`--endpoint-url` follow `this guide <./s3_endpoint_url.html>`_


.. raw:: html

    </div>
    <div data-language="b2-sdk-python" class="tabcontent">

.. code-block:: python

    from b2sdk.v2 import B2Api
    b2_api = B2Api(info)
    b2_api.authorize_account("production", keyId, applicationKey)
    # from now on, any operation you make on `b2api` will be executed in the context of your account


.. raw:: html

    </div>
    <div data-language="boto3" class="tabcontent">


.. code-block:: python

    import boto3
    from botocore.client import Config
    b2 = boto3.resource(
        service_name='s3',
        endpoint_url='https://s3.us-west-004.backblazeb2.com',
        aws_access_key_id=keyId,
        aws_secret_access_key=applicationKey,
        config=Config(signature_version='s3v4'),
    )


To get your :code:`--endpoint-url` follow `this guide <./s3_endpoint_url.html>`_

.. raw:: html

    </div>



***********************
Key creation
***********************


.. raw:: html


        <nav class="navbar navbar-expand-lg navbar-light bg-light"
             style="padding-left: 8px; background-color: #cccccc63; border: 1px solid #ccc;">

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <button type="button" class="top-level-selector btn btn-secondary" onclick="unfoldCodeSnippets(event, 'WebUI')" data-language="WebUI">WebUI</button>
            <div class="btn-group btn-secondary" style="margin-left: 4px;">
                <button type="button" class="top-level-selector btn btn-secondary dropdown-toggle" data-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">
                    Command line
                </button>
                <div class="dropdown-menu">
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'B2 CLI')" data-language="B2 CLI">B2 CLI</a>
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'AWS CLI')" data-language="AWS CLI">AWS CLI</a>
                </div>
            </div>
            <div class="btn-group btn-secondary" style="margin-left: 4px;">
                <button type="button" class="top-level-selector btn btn-secondary dropdown-toggle" data-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">
                    SDK
                </button>
                <div class="dropdown-menu">
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'b2-sdk-python')" data-language="b2-sdk-python">b2-sdk-python</a>
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'boto3')" data-language="boto3">boto3</a>
                </div>
            </div>
        </div>
    </nav>

        <div data-language="WebUI" class="tabcontent">

As presented in `Authorization`_

.. raw:: html

    </div>
    <div data-language="B2 CLI" class="tabcontent">


.. code-block:: shell

    b2 create-key --allCapabilities toad-enthusiast
    # you will see keyId and applicationKey

.. raw:: html

    </div>
    <div data-language="AWS CLI" class="tabcontent">

Not supported.

.. raw:: html

    </div>
    <div data-language="b2-sdk-python" class="tabcontent">

.. code-block:: python

    from b2sdk.v2 import ALL_CAPABILITIES
    key = b2_api.create_key(ALL_CAPABILITIES, 'toad-enthusiast')
    print(key.id_, key.application_key)


.. raw:: html

    </div>
    <div data-language="boto3" class="tabcontent">


Not supported.

.. raw:: html

    </div>

**********************************************
Buckets
**********************************************

Before you start uploading and downloading objects (files) you must create a bucket.

.. raw:: html


        <nav class="navbar navbar-expand-lg navbar-light bg-light"
             style="padding-left: 8px; background-color: #cccccc63; border: 1px solid #ccc;">

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <button type="button" class="top-level-selector btn btn-secondary" onclick="unfoldCodeSnippets(event, 'WebUI')" data-language="WebUI">WebUI</button>
            <div class="btn-group btn-secondary" style="margin-left: 4px;">
                <button type="button" class="top-level-selector btn btn-secondary dropdown-toggle" data-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">
                    Command line
                </button>
                <div class="dropdown-menu">
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'B2 CLI')" data-language="B2 CLI">B2 CLI</a>
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'AWS CLI')" data-language="AWS CLI">AWS CLI</a>
                </div>
            </div>
            <div class="btn-group btn-secondary" style="margin-left: 4px;">
                <button type="button" class="top-level-selector btn btn-secondary dropdown-toggle" data-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">
                    SDK
                </button>
                <div class="dropdown-menu">
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'b2-sdk-python')" data-language="b2-sdk-python">b2-sdk-python</a>
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'boto3')" data-language="boto3">boto3</a>
                </div>
            </div>
        </div>
    </nav>

        <div data-language="WebUI" class="tabcontent">

Go to buckets view.

.. image:: ./creating_buckets_1.png

Hit "create bucket" and fill out the details.

.. image:: ./creating_buckets_2.png

.. raw:: html

    </div>
    <div data-language="B2 CLI" class="tabcontent">


.. code-block:: shell

    b2 create-bucket pictures-of-toads allPrivate


.. raw:: html

    </div>
    <div data-language="AWS CLI" class="tabcontent">

.. code-block:: shell

    aws --profile b2tutorial --endpoint-url https://s3.us-west-004.backblazeb2.com s3api create-bucket --bucket pictures-of-toads

.. raw:: html

    </div>
    <div data-language="b2-sdk-python" class="tabcontent">

.. code-block:: python

    bucket = b2api.create_bucket('pictures-of-toads', 'allPrivate')


.. raw:: html

    </div>
    <div data-language="boto3" class="tabcontent">


.. code-block:: python

    b2.create_bucket(Bucket='pictures-of-toads', ACL='private')

.. raw:: html

    </div>

NOTE: bucket name has to be globally unique, otherwise you will get an error. For the sake of this tutorial we only
focus on private buckets.

***********************
Simple upload
***********************

Now, on any machine that ran :code:`b2 authorize-account` with the same key you can upload a file to
:code:`pictures-of-toads`:

.. raw:: html


        <nav class="navbar navbar-expand-lg navbar-light bg-light"
             style="padding-left: 8px; background-color: #cccccc63; border: 1px solid #ccc;">

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <button type="button" class="top-level-selector btn btn-secondary" onclick="unfoldCodeSnippets(event, 'WebUI')" data-language="WebUI">WebUI</button>
            <div class="btn-group btn-secondary" style="margin-left: 4px;">
                <button type="button" class="top-level-selector btn btn-secondary dropdown-toggle" data-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">
                    Command line
                </button>
                <div class="dropdown-menu">
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'B2 CLI')" data-language="B2 CLI">B2 CLI</a>
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'AWS CLI')" data-language="AWS CLI">AWS CLI</a>
                </div>
            </div>
            <div class="btn-group btn-secondary" style="margin-left: 4px;">
                <button type="button" class="top-level-selector btn btn-secondary dropdown-toggle" data-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">
                    SDK
                </button>
                <div class="dropdown-menu">
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'b2-sdk-python')" data-language="b2-sdk-python">b2-sdk-python</a>
                    <button class="dropdown-item" onclick="unfoldCodeSnippets(event, 'boto3')" data-language="boto3">boto3</a>
                </div>
            </div>
        </div>
    </nav>

        <div data-language="WebUI" class="tabcontent">

Go to file browsing view.

.. image:: ./upload_file_1.png

Choose destination bucket.

.. image:: ./upload_file_2.png

Upload your file.

.. image:: ./upload_file_3.png

.. raw:: html

    </div>
    <div data-language="B2 CLI" class="tabcontent">


.. code-block:: shell

    b2 upload-file pictures-of-toads /home/todd/pictures/fire-bellied-toad.png fire-bellied-toad.png


.. raw:: html

    </div>
    <div data-language="AWS CLI" class="tabcontent">

.. code-block:: shell

    aws --profile b2tutorial --endpoint-url https://s3.us-west-004.backblazeb2.com s3api put-object \
      --bucket pictures-of-toads --key fire-bellied-toad.png --body /home/todd/pictures/fire-bellied-toad.png

.. raw:: html

    </div>
    <div data-language="b2-sdk-python" class="tabcontent">

.. code-block:: python

    bucket = b2api.get_bucket_by_name('pictures-of-toads')
    bucket.upload_local_file('/home/todd/pictures/fire-bellied-toad.png', 'fire-bellied-toad.png')


.. raw:: html

    </div>
    <div data-language="boto3" class="tabcontent">


.. code-block:: python

    with open('/home/todd/pictures/fire-bellied-toad.png', 'br') as file:
        b2.Object(  # TODO: this doesn't work, need to figure out why
            'fire-bellied-toad.png',
            'pictures-of-toads',
        ).put(Body=file)

.. raw:: html

    </div>

this will create an object that users of your account can download.
