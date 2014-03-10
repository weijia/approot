import os
import qrcode
from libtool import find_root_path
from libtool.filetools import get_free_timestamp_filename_in_path
from utils.misc import ensure_dir as ensure_dir


def get_qr_code(data):
    qr = qrcode.QRCode(version=8, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(data)
    qr.make()  # Generate the QRCode itself

    # im contains a PIL.Image.Image object
    im = qr.make_image()

    # To save it
    target_dir = os.path.join(find_root_path(__file__, "approot"), "../qrcode")
    ensure_dir(target_dir)
    target_file_path = get_free_timestamp_filename_in_path(target_dir, ".png")
    im.save(target_file_path)
    return target_file_path