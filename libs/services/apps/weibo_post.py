import socialoauth

from settings import SOCIALOAUTH_SITES
from socialoauth import socialsites
from socialoauth.utils import import_oauth_class
from socialoauth.exception import SocialAPIError
from socialoauth.sites.weibo import get_access_token
from helper import Session, UserStorage, gen_session_id