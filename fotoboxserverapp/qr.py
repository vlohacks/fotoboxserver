from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_file
)
from .auth import login_required

from io import BytesIO
import qrcode

bp = Blueprint('qr', __name__, url_prefix='/qr')

@bp.route('/<string:uuid>')
def qr(uuid):
    url = url_for('main.main', uuid=uuid, _external=True)
    print(url)

    imgio = BytesIO()

    qr = qrcode.QRCode(
        version=4,
        box_size=6,
        border=3
    )

    qr.add_data(url)

    qr.make(fit=False)
    
    img = qr.make_image()
    img.save(imgio, 'PNG')
    imgio.seek(0)
    return send_file(imgio, mimetype='image/png')