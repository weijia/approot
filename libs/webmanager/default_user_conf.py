try:
    from keys.admin_pass import default_admin_password, default_admin_user
except ImportError:
    from keys_template.admin_pass import default_admin_password, default_admin_user
    
    
def get_default_username_and_pass():
    return default_admin_password, default_admin_user