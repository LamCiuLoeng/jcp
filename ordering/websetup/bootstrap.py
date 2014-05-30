# -*- coding: utf-8 -*-
"""Setup the ordering application"""

import logging
from tg import config
from ordering import model

import transaction


def bootstrap(command, conf, vars):
    """Place any commands to setup ordering here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        u = model.User()
        u.user_name = "admin"
        u.display_name = "Administrator"
        u.email_address = u'manager@somedomain.com'
        u.password = "ecrmadmin"
    
        model.DBSession.add(u)
    
        g = model.Group()
        g.group_name = "Admin"
        g.display_name = "Admin"
        g.users.append(u)
    
    
        model.DBSession.add(g)
        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print 'Warning, there was a problem adding your auth data, it may have already been added:'
        import traceback
        print traceback.format_exc()
        transaction.abort()
        print 'Continuing with bootstrapping...'
        

    # <websetup.bootstrap.after.auth>
