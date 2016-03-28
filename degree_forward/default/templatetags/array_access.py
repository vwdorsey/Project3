from django import template
register = template.Library()


@register.filter
def lookup(list,i):
    return list[int(i)-1]
