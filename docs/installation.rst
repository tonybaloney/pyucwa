.. highlight:: shell

============
Installation
============

At the command line:

.. code-block:: console

    $ easy_install ucwa

Or, if you have virtualenvwrapper installed:

.. code-block:: console

    $ mkvirtualenv ucwa
    $ pip install ucwa


Configuring SfB Online
----------------------

Follow the steps in https://msdn.microsoft.com/en-us/office/office365/howto/add-common-consent-manually

Enter the pool for your tenant by visiting the URL : https://webdir.online.lync.com/Autodiscover/AutodiscoverService.svc/root?originalDomain=parliamentfunksterhotmail.onmicrosoft.com with your domain.



You will need to know for the given user which Skype pool they are running on, login to the Office 365 Admin Center, go to the Lync/SfB Admin Console.
