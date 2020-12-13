# ServiceNow Record Lookup Client

This is a simple command line application for looking up details of any record that you have access to in
ServiceNow, as well as downloading any related attachments. 

In my day job, I support multiple ServiceNow clients, and the ticket handling often happens in their own instances. This means I may have to log in and out many times a day into many instances. I also like
to keep a folder on my computer for each ticket and download any related attachments there. I find
this looking up of tickets, creating folders and downloading attachments tedious, so I created this 
app to make that a bit easier. 

In this app you use your own ServiceNow credentials. You can save the credentials for as many instances you want. The credentials are saved encrypted in a file in the application folder.

In order to access a record, you will need to know its exact ID (for example INC0000001) and have the rights to read the record as well as use the ServiceNow REST API.

In the settings.py file you can find some configuration options. If you want to downlod attachments from a record, you will need to specify a root path and a parent directory name. This is the directory where the app will create a folder name with the record ID and where it will save the attachments related to that record. You can also specify which field values you want to have returned for the record, as well as the regex used to identify a record ID from your input.

GUI version of this app is underway!