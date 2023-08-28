import requests
import requests_cache
import urllib.parse
import json
from functools import reduce

requests_cache.install_cache('pi_digits_cache', backend='sqlite', expire_after=300)

class ListConvertibleString(str):
    """ Helper class that extends the `str` class
        to allow for a list of digits representation

    Args:
        str (str): string composed of digits only
    """
    def to_list(self) -> list[int]:
        """ Returns a list of digits (int) split from 
            the original string.
            Example: "12345" -> [1,2,3,4,5]

        Returns:
            list[int]: _description_
        """
        # TODO Add exception handling for when int(d) fails
        return [int(d) for d in self]

class PiDigits():
    def __init__(self):
        self.start = 0
        self.numOfDigits = 100
        self.apiBaseUrl = "https://api.pi.delivery/v1/pi?"
        self.params = {'start': self.start, 'numberOfDigits': self.numOfDigits}

    def get_encoded_api_url(self,num=None,start=None) -> str:
        """ Encodes the API URL using the number of digits 
            to fetch and the position in pi's decimal numbers 
            from where to start fetching.

        Args:
            num (int, optional): number of digits to fetch. Defaults to self.numOfDigits.
            start (int, optional): decimal position from where to start fetching. Defaults to self.start.

        Returns:
            str: the api url as a string
        """
        num = num or self.numOfDigits 
        start = start or self.start
        
        self.params["start"] = start
        self.params["numberOfDigits"] = num
        return  self.apiBaseUrl + \
                urllib.parse.urlencode(
                    self.params
                )

    def get_next(self,num=None,start=None) -> str:
        """ Gets the next `num` digits starting from 
            the position of `start`

        Args:
            num (int, optional): the number of . Defaults to self.numOfDigits.
            start (int, optional): _description_. Defaults to self.start.

        Returns:
            str: Returns a ListConvirtableString, i.e. the desired 
            range of digits as a very long string.
            Example:
                >>> PiDigits().get_next(10)
                    '3141592653'
        """
        num = num or self.numOfDigits
        start = start or self.start
        if num > 1000:
            return self._get_range(start,start+num)
        res = ListConvertibleString(
            json.loads(
                    requests.get(
                        self.get_encoded_api_url(num,start)
                    ).content
                )["content"]
        )
        return res

    def _get_range(self,start,end) -> str:
        """
        k,m = divmod(end,1000)
        [start,end] -> [[start,1000],
                        [1001,1000],
                        [2001,1000],
                        ....
                        [(k-1)*1000+1,1000],
                        [k*1000+1,m]
                        ]
        """
        k,m = divmod(end,1000)
        pages = [[start,1000]] + \
                [[start+i*1000+1,1000] for i in range(1,k)] + \
                [[start+k*1000+1,m]]
        if m==0:
            pages.pop()
        
        return reduce(
            lambda x,y: x+y,
            map(
                lambda page: self.get_next(page[1],page[0]),
                pages
            )
        )