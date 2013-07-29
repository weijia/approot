import os
from libs.utils.filetools import getTimestampWithFreeName
import libsys
import qrcode
from libs.utils.misc import ensureDir as ensure_dir


def get_qr_code(data):
    qr = qrcode.QRCode(version=8, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(data)
    qr.make() # Generate the QRCode itself

    # im contains a PIL.Image.Image object
    im = qr.make_image()

    # To save it
    target_dir = os.path.join(libsys.get_root_dir(), "../qrcode")
    ensure_dir(target_dir)
    target_file_path = getTimestampWithFreeName(target_dir, ".png")
    im.save(target_file_path)
    return target_file_path