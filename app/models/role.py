def is_admin(user):
    return user.get('role') == 'admin'

def is_owner(user):
    return user.get('role') == 'owner'

def is_parent(user):
    return user.get('role') == 'parent'
