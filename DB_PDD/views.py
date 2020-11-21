# -*- coding: utf-8 -*-
from django.http import FileResponse, HttpResponse
from wsgiref.util import FileWrapper


client_secret = "wvl68m4dR1UpLrVRli"


def index(request):
    response = FileResponse(open('DB_PDD/MTA-QMoi7Ns.jpg', 'rb'))
    return response

def index2(request):
    class FixedFileWrapper(FileWrapper):
        def __iter__(self):
            self.filelike.seek(0)
            return self

    import mimetypes, os
    response = HttpResponse(FixedFileWrapper(open('DB_PDD/FCC5B4FCF83FAFE7EC4AD9D6AA7383AC.txt', 'rb')), content_type=mimetypes.guess_type('DB_PDD/FCC5B4FCF83FAFE7EC4AD9D6AA7383AC.txt')[0])
    response['Content-Length'] = os.path.getsize('DB_PDD/FCC5B4FCF83FAFE7EC4AD9D6AA7383AC.txt')
    response['Content-Disposition'] = "attachment; filename=%s" % os.path.basename('DB_PDD/FCC5B4FCF83FAFE7EC4AD9D6AA7383AC.txt')
    return response