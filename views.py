from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
from models import AestheticOptions
import nullaesthetic

#noinspection PyUnusedLocal
@login_required
def ensure_aesthetic_options_defaults(request):
    AestheticOptions.ensure_defaults()
    return HttpResponse(u"done")


def random_aesthetic(request):
    aesthetic = recipeer.null_aesthetic()
    ctx = {
        'aesthetic': aesthetic
    }
    content = simplejson.dumps(ctx, indent=4)
    return HttpResponse(content, content_type='application/json')
