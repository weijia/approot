from models import StaticFile
import re
from django.http import HttpResponse

class ManifestRecorderMiddleware:
    def process_request(self, request):
        if re.search(r"\.(jpg|gif|png|css|js|html|htm)$", request.path):
            if StaticFile.objects.filter(path = request.path).count == 0:
                StaticFile(path = request.path, cachable = False).save()
                print request.path

def manifest(request):
    item = []
    for i in StaticFile.objects.all():
        item.append(i.path)
    response = '''CACHE MANIFEST
CACHE:
%s
NETWORK:
*
FALLBACK:'''%'\n'.join(item)
    return HttpResponse(response, mimetype="text/cache-manifest")
