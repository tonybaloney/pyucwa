===============================
pyucwa
===============================

.. image:: https://img.shields.io/pypi/v/ucwa.svg
        :target: https://pypi.python.org/pypi/ucwa

.. image:: https://img.shields.io/travis/tonybaloney/ucwa.svg
        :target: https://travis-ci.org/tonybaloney/ucwa

.. image:: https://readthedocs.org/projects/ucwa/badge/?version=latest
        :target: https://readthedocs.org/projects/ucwa/?badge=latest
        :alt: Documentation Status


Skype for Business UCWA API client

* Free software: MIT license
* Documentation: https://ucwa.readthedocs.org.

Usage
-----

Setup your tenant

Follow the steps in https://msdn.microsoft.com/en-us/office/office365/howto/add-common-consent-manually

Enter the pool for your tenant by visiting the URL : https://webdir.online.lync.com/Autodiscover/AutodiscoverService.svc/root?originalDomain=parliamentfunksterhotmail.onmicrosoft.com with your domain.

Create a file config.yml with similar details

    redirect_uri: "http://127.0.0.1:5000"
    client_id: "0b78a9be-6b65-1234-b8e6-a0b21a8672c3"
    secret: "jPpYkK+sdf3423r="
    domain: "mydomain.onmicrosoft.com"
    app_id: "https://mydomain.onmicrosoft.com/bot"

Start the web server

    python -m ucwa.http


Run a login session to get a token for the application

    python authhelper.py

This will open the browser, get you to login to Office 365 and then create an instance session with a UCWA server in O365/Skype for Business online

You can then run app.py to stream events

    python app.py


Extend app.py to do what you want to the events, like have a chat with other people or integrate into your bot framework.

Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
