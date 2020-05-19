from lyft.api_client import EnvoyClient
from lyft.functional import memoize
from lyft_requests.response import BadResponse
from lyft.settings import str_env


aardvark_client = EnvoyClient(
    service="aardvark",
    auth_type=EnvoyClient.AUTH_TYPE_BASIC,
    user=str_env("AARDVARK_USER"),
    key=str_env("AARDVARK_API_KEY"),
)


class AardvarkRequestException(Exception):
    def __init__(self, msg):
        super(AardvarkRequestException, self).__init__(msg)


class AardvarkService(object):
    def post(self, url, params=None, json=None):
        """Wrapper over EnvoyClient to send a post request
           The url parameter is intentionally ignored
        """
        json.update(params)
        try:
            return aardvark_client.post("api/v1/advisors", data=json)
        except BadResponse as e:
            raise AardvarkRequestException(e)


@memoize
def get_aardvark_service():
    return AardvarkService()


aardvark_service = get_aardvark_service()
