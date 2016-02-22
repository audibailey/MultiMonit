# MultiMonit

A M/Monit Alternative coded in Python. Heavily based on Monittr (https://github.com/karmi/monittr)
Version: 2.39

# Important

* Default username and password is: admin/password You can change it in the run.py config section.
* There is one error which makes it impossible to kill MultiMonit using Ctrl + C. Please use Ctrl + \ to kill MultiMonit, kill -9 {PID} still works as usual.
* If there is in error or you cant figure something out, use the GitHub Issues tab please.

# To Do

* Fix the Ctrl+C error (For now use Kill or Ctrl + \ )
* Add new proposed features

# Requirements:

* Python 2.7+
* Jinja2 >= 2.8
* CherryPy >= 4.0.0
* MarkupSafe >= 0.23
* PyYAML >= 3.11

#Instructions for Debian/Ubuntu:

1. sudo apt-get update
2. sudo apt-get install build-essential python2.7 python-dev git python-pip libyaml-dev
3. sudo pip install jinja2 cherrypy markupsafe PyYAML
4. sudo git clone git://github.com/desgyz/MultiMonit.git /opt/MultiMonit
5. sudo chown -R user:group /opt/MultiMonit
6. sudo python2.7 /opt/MultiMonit/run.py
7. Goto ip-address:3005 for the setup to begin.

#Credits

* Mike (http://htpcguides.com)
* Karmi (https://github.com/karmi/monittr)
* Jason (https://simpletutorials.com/c/2543/MVC+with+CherryPy+and+Jinja2+%28updated%29)
* MetroUI (http://metroui.org.ua/)