#MultiMonit

A M/Monit Alternative coded in Python. Heavily based on Monittr (https://github.com/karmi/monittr)
Version: 2.13

#Important

* There is one error which makes it impossible to kill MultiMonit using Ctrl + C. Please use Ctrl + \ to kill MultiMonit, kill -9 {PID} still works as usual.
* If there is in error or you cant figure something out, use the github Issues tab please.

#To Do

* Utilise simply HTTP Auth headers and make a config setup for that
* Fix the Ctrl+C error
* Add new proposed features

# Requirements:

Python 2.7+
Jinja2 >= 2.8
CherryPy >= 4.0.0
MarkupSafe >= 0.23
PyYAML >= 3.11

#Instructions for Debian/Ubuntu:

sudo apt-get update
sudo apt-get python2 git
sudo pip install jinja2 cherrypy markupsafe PyYAML
cd /opt
git clone git://github.com/desgyz/MultiMonit.git MultiMonit
cd MultiMonit
Run the run.py and goto localhost:3005 for the setup to begin.
(Some people may require python dev to use this)

#Credits

Mike (http://htpcguides.com)
Karmi (https://github.com/karmi/monittr)
Jason (https://simpletutorials.com/c/2543/MVC+with+CherryPy+and+Jinja2+%28updated%29)
MetroUI (http://metroui.org.ua/)