# Fotoboxserver App

Python/Flask Application for handling and displaying fotobox pictures. The application can handle multiple partys.
Notice that this stuff has been hacked in a rush for my wedding, so don't expect any fancy stuff. It just works. Period :-)
But I encourage you sharing improvements as pull requests.

## Dependencies

flask, python-qrcode, werkzeug, PIL

## Setup

First time you need to do the following:

* set up admin password (for frontend login)
* set up api key (for permitting the fotobox uploader uploading files)
* initialize SQLite Database 

This is done by running the following command

```
FLASK_APP=fotoboxserverapp flask makeconfig --apikey <somesecretkey> --adminpassword <somesecretpassword> --initdb
```

Please make sure using strong passwords.... bla bla... 

## Running

```
FLASK_APP=fotoboxserverapp flask run
```
or use the WSGI server of your choice

Notice: The application will respond with 404 when accessing the root page or an unexisting party for security by obscurity reasons ;-)

## Usage

* browse to http://fotoboxserver/admin
* log in using the admin password
* create party
* set up fotobox uploader on fotobox with the correct party uuid, api key and URL for your fotobox server
* print out qr codes and place them around the party location or share party link for easy access to the pictures
* invite friends and party hard

## FAQ

Q: The interface is ugly as hell!!!
A: I suck at frontend-dev. So feel free to add CSS and custom stuff in templates. 

Q: What about privacy? Who can see the pictures?
A: Everybody who's in posession of the link can see the pictures. So make sure only people who are attending to your party know the link 




