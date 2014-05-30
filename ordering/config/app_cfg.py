# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in ordering.

This file complements development/deployment.ini.

Please note that **all the argument values are strings**. If you want to
convert them into boolean, for example, you should use the
:func:`paste.deploy.converters.asbool` function, as in::
    
    from paste.deploy.converters import asbool
    setting = asbool(global_conf.get('the_setting'))
 
"""

from tg.configuration import AppConfig
from tg.util import Bunch

import ordering
from ordering import model
from ordering.lib import app_globals, helpers

from ordering.config.authMiddleware import MySQLAlchemyAuthenticatorPlugin, FriendlyTimeoutPlugin

base_config=AppConfig()
base_config.renderers=[]

base_config.package=ordering

#Enable json in expose
base_config.renderers.append('json')
#Set the default renderer
base_config.default_renderer='mako'
base_config.renderers.append('mako')

#Configure the base SQLALchemy Setup
base_config.use_sqlalchemy=True
base_config.model=ordering.model
base_config.DBSession=ordering.model.DBSession

# Configure the authentication backend

# YOU MUST CHANGE THIS VALUE IN PRODUCTION TO SECURE YOUR APP 
base_config.sa_auth.cookie_secret="dingnigefei"

base_config.auth_backend='sqlalchemy'
base_config.sa_auth.dbsession=model.DBSession
# what is the class you want to use to search for users in the database
base_config.sa_auth.user_class=model.User
# what is the class you want to use to search for groups in the database
base_config.sa_auth.group_class=model.Group
# what is the class you want to use to search for permissions in the database
base_config.sa_auth.permission_class=model.Permission

# override this if you would like to provide a different who plugin for
# managing login and logout of your application
base_config.sa_auth.form_plugin=FriendlyTimeoutPlugin('/login', '/login_handler', '/post_login', '/logout_handler', '/post_logout', 'cookie')

myPlugin=MySQLAlchemyAuthenticatorPlugin(model.User, model.DBSession)

base_config.sa_auth.authenticators=[("MySQLAlchemyAuthenticatorPlugin", myPlugin)]

# You may optionally define a page where you want users to be redirected to
# on login:
base_config.sa_auth.post_login_url='/post_login'

# You may optionally define a page where you want users to be redirected to
# on logout:
base_config.sa_auth.post_logout_url='/post_logout'


#special configure for the Financial project.

base_config.ldap=Bunch()
base_config.ldap.host='192.168.42.167'
base_config.ldap.port=389
base_config.ldap.basedn=['ou=sz,dc=r-pac,dc=local', 'ou=hk,dc=r-pac,dc=local', 'ou=sh,dc=r-pac,dc=local']
base_config.ldap.initdn='CN=adAuth,OU=System Account,DC=r-pac,DC=local'
base_config.ldap.initpw='ky2379ck$'
