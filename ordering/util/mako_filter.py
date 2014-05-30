# -*- coding: utf-8 -*-

__all__ = []

b = lambda v:"&nbsp;" if not v else v
na = lambda v: 'N/A' if not v else v
status_show = lambda v: 'Active' if v == '0' else 'Inactive'
active_item = lambda v:  v if len(v) > 1 else 'Inactive'
non_qty = lambda v: '0' if not v else v

def tp(v):
    if not v : return "&nbsp;"
    return "<span class='tooltip' title='%s'>%s</span>" % (v, v)
