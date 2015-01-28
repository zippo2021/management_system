from dashboard.common_profile.permissions import field_perms
from user_manager.permissions import perms_to_classes

def perms_to_list(perms):
    result = []
    for key in perms:
        if perms[key]: 
           result.append(perms_to_classes[key])
    return result 

def create_info(viewer, user, restr):
    result = {"Teacher":{},"RegularUser":{},\
              "Observer":{},"Mentor":{},"Admin":{}}
    viewer_perms = perms_to_list(viewer.UserData.get_permissions())
    user_perms = perms_to_list(user.UserData.get_permissions())
    if restr:
        for uperm in user_perms:
            for key in field_perms[uperm]:
                if list(set(field_perms[uperm][key]) & set(viewer_perms)):
                    result[uperm][key] = getattr(getattr(user.UserData,\
                                                            uperm), key)
    else:
       for uperm in user_perms:
           for key in field_perms[uperm]:
               result[uperm][key] = getattr(getattr(user.UserData,\
                                                        uperm), key)
    return result
