# encoding: utf-8

# page show record size
show_cnt = 15

# msyql dababase connection info
mysqldb_conn = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : '',
    'db' : 'wyproxy',
    'charset' : 'utf8'
}

# with out save http response content to database
save_content = True

# http map filenames to MIME types
# https://docs.python.org/2/library/mimetypes.html
http_mimes = ['text', 'image', 'application', 'video', 'message', 'audio']

# http static resource file extension
static_ext = ['js', 'css', 'ico']

# media resource files type
media_types = ['image', 'video', 'audio']

# http static resource files
static_files = [
    'text/css',
    # 'application/javascript',
    # 'application/x-javascript',
    'application/msword',
    'application/vnd.ms-excel',
    'application/vnd.ms-powerpoint',
    'application/x-ms-wmd',
    'application/x-shockwave-flash',
    # 'image/x-cmu-raster',
    # 'image/x-ms-bmp',
    # 'image/x-portable-graymap',
    # 'image/x-portable-bitmap',
    # 'image/jpeg',
    # 'image/gif',
    # 'image/x-xwindowdump',
    # 'image/png',
    # 'image/vnd.microsoft.icon',
    # 'image/x-portable-pixmap',
    # 'image/x-xpixmap',
    # 'image/ief',
    # 'image/x-portable-anymap',
    # 'image/x-rgb',
    # 'image/x-xbitmap',
    # 'image/tiff',
    # 'video/mpeg',
    # 'video/x-sgi-movie',
    # 'video/mp4',
    # 'video/x-msvideo',
    # 'video/quicktime'
    # 'audio/mpeg',
    # 'audio/x-wav',
    # 'audio/x-aiff',
    # 'audio/basic',
    # 'audio/x-pn-realaudio',
    ]

