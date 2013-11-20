import sys


def create_secret_key_file_and_return_key(full_path):
    try:
        from django.utils.crypto import get_random_string
        import os
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = get_random_string(50, chars)
        secret_file = open(os.path.join(full_path, 'secret_key.py'), 'w')
        secret_file.write("SECRET_KEY='%s'" % secret_key)
        secret_file.close()
        sys.path.append(full_path)
        from secret_key import SECRET_KEY
        sys.path.remove(full_path)
        return SECRET_KEY
    except:
        #In case the above not work, use the following.
        # Make this unique, and don't share it with anybody.
        # TODO: need to log this issue
        return 'd&amp;x%x+^l@qfxm^2o9x)6ct5*cftlcu8xps9b7l3c$ul*n&amp;%p-k'
