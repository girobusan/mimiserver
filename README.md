Mimi server
===========

Simplified Python 3 implementation of TiddlyWiki server for __local usage.__ Save your TiddlyWikis easy, without plugins, from any browser.

Requirements
------------
1. Python 3 installed.
2. You can run Python 3 scripts.
3. Your OS allows you to set up local server.

Usage
-----

Let's assume that your TiddlyWiki kept in file named mywiki.html. 

Put the file mimiserver.py to the same directory with that file and run it (depends on your OS). Than navigate to http://localhost:9889/mywiki.html. On Linux and Mac OS you may need to fix executable flag:

    chmod +x mimiserver.py

If you don't like the port, you can run it like this:

    ./mimiserver.py 4242

 To run it at port 4242. Choose your favourite number.

Usage — advanced
----------------

Open mimiserver.py in your text editor. There are some configuration variables on top. Edit them to suit your needs. 
