import hashlib
import time


def encrypt_to_md5_string(content, app_key):
    """
    用于生成签名，基于内容和 app_key
    """
    trimmed_app_key = app_key.strip()
    trimmed_content = content.strip()
    combined_content = trimmed_app_key + trimmed_content
    return encrypt_md5(combined_content)


def encrypt_md5(content):
    """
    将字符串生成 MD5 值，并转换为大写的十六进制格式
    """
    md5_hash = hashlib.md5()
    md5_hash.update(content.encode('utf-8'))
    return parse_byte_to_hex_string(md5_hash.digest())


def parse_byte_to_hex_string(byte_data):
    """
    将字节数组转换为十六进制字符串
    """
    hex_string = ''.join(f'{byte:02X}' for byte in byte_data)
    return hex_string


def get_timestamp():
    return int(time.time() * 1000)


def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        url = f'{url}{str(key)}={str(value)}&' if value != '' else url
    url = url[0:-1]
    return url


def get_header(timestamp, sign):
    header = {
        'User-Agent': 'openApi',
        'Content-Type': 'application/json; charset=utf-8',
        'accept-encoding': 'gzip, deflate',
        'time-stamp': str(timestamp),
        'data-signature': sign
    }
    return header
