from django import template

register = template.Library()

def key(d, key_name):
    return d[key_name]
key = register.filter('key', key)

def ifilter(l, i_type):
    return l.filter(instruction_type=i_type)
ifilter = register.filter('ifilter', ifilter)
