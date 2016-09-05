Register your application with Azure AD

Sign in to the Azure Management Portal, then do the following:

Click the Active Directory node in the left column and select the directory linked to your Skype for Business subscription.

Select the Applications tab and then Add at the bottom of the screen.

Select Add an application my organization is developing.

Choose a name for your application, such as skypewebsample, and select Web application and/or web API as its Type. Click the arrow to continue.

The value of Sign-on URL is the URL at which your application is hosted.

The value of App ID URI is a unique identifier for Azure AD to identify your application. You can use http://{your_subdomain}/skypewebsample, where {your_subdomain} is the subdomain of .onmicrosoft you specified while signing up for your Skype for Business Web App (website) on Azure. Click the check mark to provision your application.

Select the Configure tab, scroll down to the Permissions to other applications section, and click the Add application button.

In order to show how to create online meetings, add the Skype for Business Online application. Click the plus sign in the application's row and then click the check mark at the top right to add it. Then click the check mark at the bottom right to continue.

In the Skype for Business Online row, select Delegated Permissions, and in the selection list, choose Create Online Meetings.

Select Application is Multi-Tenant to configure the application as a multi-tenant application.

Click Save to save the application's configuration.

These steps register your application with Azure AD, but you still need to configure your app's manifest to use OAuth implicit grant flow, as explained below.

Configure your app for OAuth implicit grant flow

In order to get an access token for Skype for Business API requests, your application will use the OAuth implicit grant flow. You need to update the application's manifest to allow the OAuth implicit grant flow because it is not allowed by default.

Select the Configure tab of your application's entry in the Azure Management Portal.

Using the Manage Manifest button in the drawer, download the manifest file for the application and save it to your computer.

Open the manifest file with a text editor. Search for the oauth2AllowImplicitFlow property. By default it is set to false; change it to true and save the file.

Using the Manage Manifest button, upload the updated manifest file.

This will register your application with Azure AD.