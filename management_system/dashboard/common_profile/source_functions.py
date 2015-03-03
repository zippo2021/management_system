from dashboard.common_profile.permissions import field_perms
from user_manager.permissions import perms_to_classes

def perms_to_list(perms):
    result = []
    for key in perms:
        if perms[key]: 
           result.append(key)
    return result 

def create_info(viewer, user, restr):
    result = {"teacher":{},"regular":{},\
              "observer":{},"mentor":{},"admin":{}}
    viewer_perms = perms_to_list(viewer.get_permissions())
    user_perms = perms_to_list(user.get_permissions())
    if restr:
        for uperm in user_perms:
            for key in field_perms[uperm]:
                model = getattr(user, perms_to_classes[uperm])
                v_name = model._meta.get_field(key).verbose_name
                if list(set(field_perms[uperm][key]) & set(viewer_perms)):
                    result[uperm][v_name] =\
                                           getattr(model, key)
    else:
       for uperm in user_perms:
           for key in field_perms[uperm]:
               model = getattr(user, perms_to_classes[uperm])
               v_name = model._meta.get_field(key).verbose_name
               result[uperm][v_name] = getattr(model, key)
    return result
