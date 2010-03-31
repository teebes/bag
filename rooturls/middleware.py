import re

from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponseRedirect

from rooturls.models import ExternalUrl, NamedUrl

class RootUrlMiddleware(object):
    def __init__(self):
        self._external_urls = ExternalUrl.objects.values()
        self._named_urls = NamedUrl.objects.values()
    
    def process_request(self, request):

        split_path = request.path.split('/')[1:]
        root_url = split_path[0]

        if split_path:
            # check for external urls
            for external_url in self._external_urls:
                if root_url == external_url['short_name']:
                    return HttpResponseRedirect(external_url['redirect_to'])

            # check for named, internal urls
            for named_url in self._named_urls:
                if root_url == named_url['short_name']:

                    # get the args list
                    if named_url['url_args'] == '':
                        args = []
                    else:
                        args = map(lambda x: re.sub('\s*', '', x),
                                   named_url['url_args'].split(','))
                    
                    to_url = reverse(named_url['url_name'], args=args)
                    
                    if named_url['redirect']:
                        return HttpResponseRedirect(to_url)
                    else:
                        func, args, kwargs = resolve(to_url)
                        return func(request, *args, **kwargs)

        return None
