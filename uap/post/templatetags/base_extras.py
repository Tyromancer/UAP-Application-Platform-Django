from django import template

register = template.Library()


# check if user is in a specified user group
@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
    