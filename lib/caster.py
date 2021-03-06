import os,time,threading
import socket,http.server,socketserver
import pychromecast

def create_dir(dir_name):
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    except:
        return False

def host_server(hosting_port,server_root_dir):
    create_dir(server_root_dir)

    try:
        server_port = int(hosting_port)
        os.chdir(server_root_dir)

        Handler = http.server.SimpleHTTPRequestHandler

        httpd = socketserver.TCPServer(('',server_port),Handler)
        server_port = str(httpd.server_address[1])
        httpd.serve_forever()
        return True
    except:
        return False

def get_cc(cc_name=''):
    if cc_name == '':
        try:
            return pychromecast.get_chromecasts()[0]
        except:
            return None
    else:
        for cc in pychromecast.get_chromecasts():
            if cc.device.friendly_name == cc_name:
                return cc

    return None

def send_to_chromecast(cast_url,cast):
    if cast is not None:
        mc = cast.media_controller
        mc.play_media(cast_url,'image/png')
        mc.block_until_active()
        return True
    else:
        return False
        

def cast_image(image_location,cc):
    server_host = socket.gethostbyname(socket.gethostname())
    server_port = 55555
    server_root_dir = os.path.split(image_location)[0]
   
    threading.Thread(target=host_server,args=(server_port,server_root_dir,)).start()

    cast_url = 'http://'+server_host+':'+str(server_port)+'/'+os.path.split(image_location)[1]
    send_to_chromecast(cast_url,cc)
    return True
