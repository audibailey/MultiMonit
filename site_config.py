import os


class SiteConfig:
    # whether or not we're running in production (I determine this via the path)
    # we use this to determine whether or not to show stack traces when errors occur
    is_prod = os.path.abspath("./").startswith("/srv")
    home = '/srv/www/mysite.com/application' if is_prod else os.path.abspath("./")
