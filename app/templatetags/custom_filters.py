from django import template

register = template.Library()

@register.filter(name='abs')
def abs_filter(value):
    """Returns the absolute value"""
    return abs(value)


@register.filter
def sub(value, arg):
    """Subtracts arg from value"""
    return value - arg

@register.filter
def div(value, arg):
    """Divides value by arg"""
    try:
        return value / arg
    except ZeroDivisionError:
        return 0

@register.filter
def mul(value, arg):
    """Multiplies value by arg"""
    return value * arg