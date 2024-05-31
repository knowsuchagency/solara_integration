from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render
from django.conf import settings
from pathlib import Path
import mimetypes
import os
from urllib.parse import urlparse
from uuid import uuid4
import logging
from solara.server import server
from solara.server import cdn_helper, kernel_context, server, settings, websocket, app as appmod


logger = logging.getLogger("solara.server.django")

def kernels(request, id):
    return JsonResponse({"name": "lala", "id": "dsa"})

def close(request, kernel_id):
    page_id = request.GET.get("session_id")
    context = kernel_context.contexts.get(kernel_id, None)
    if context:
        context.page_close(page_id)
    return HttpResponse("")

def public(request, path):
    directories = [app.directory.parent / "public" for app in appmod.apps.values()]
    for directory in directories:
        file = directory / path
        if file.exists():
            return serve_file(directory, path)
    return HttpResponse("not found", status=404)

def assets(request, path):
    directories = server.asset_directories()
    for directory in directories:
        file = directory / path
        if file.exists():
            return serve_file(directory, path)
    return HttpResponse("not found", status=404)

def nbext(request, dir, filename):
    for directory in server.nbextensions_directories:
        file = directory / dir / filename
        if file.exists():
            return serve_file(directory / dir, filename)
    return HttpResponse("not found", status=404)

def serve_static(request, path):
    return serve_file(server.solara_static, path)

def cdn(request, path):
    cache_directory = settings.assets.proxy_cache_dir
    content = cdn_helper.get_data(Path(cache_directory), path)
    mime = mimetypes.guess_type(path)
    return HttpResponse(content, content_type=mime[0])

def read_root(request, path=""):
    root_path = request.build_absolute_uri('/')
    if root_path.endswith("/"):
        root_path = root_path[:-1]

    if not settings.main.base_url:
        settings.main.base_url = root_path

    session_id = request.COOKIES.get(server.COOKIE_KEY_SESSION_ID) or str(uuid4())
    content = server.read_root(path, root_path=root_path)
    if content is None:
        return HttpResponse("not found", status=404)


    samesite = "Lax"
    secure = False
    o = urlparse(request.build_absolute_uri())
    if request.headers.get("x-forwarded-proto", "http") == "https" or o.hostname == "localhost":
        samesite = "None"
        secure = True

    response = HttpResponse(content, content_type="text/html")
    response.set_cookie(server.COOKIE_KEY_SESSION_ID, value=session_id, secure=secure, samesite=samesite)
    return response

def serve_file(directory, path):
    file_path = os.path.join(directory, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return HttpResponse(f.read(), content_type=mimetypes.guess_type(file_path)[0])
    raise Http404

def readyz(request):
    json, status = server.readyz()
    return JsonResponse(json, status=status)
