from proxypool.untils.loggings import Logging

logging = Logging()


def bytes_convert_string(data):
    if isinstance(data, bytes):
        return data.decode('utf8')
    return data

def is_valid_proxy(ip_port):
    if ip_port is None:
        return
    elif isinstance(ip_port, str):
        try:
            ip_port_list = ip_port.split(':')
            if len(ip_port_list) == 2:
                port = ip_port_list.pop()
                if not port.isdigit():
                    return
                ip_list = ip_port_list
                ip_str = ",".join(ip_list)
                li = ip_str.split('.')
                if len(li) == 4:
                    _ip = [int(s) for s in li if 0 < int(s) <= 254]
                    if len(_ip) == 4:
                        return ip_port
        except ValueError:  # int(x), x = 'a' --> ValueError
            logging.error(f'ip not valid -- {ip_port}')


if __name__ == '__main__':
    by = b'27a.191.60.60:3256'
    ip = bytes_convert_string(by)
    is_valid_proxy(ip)
