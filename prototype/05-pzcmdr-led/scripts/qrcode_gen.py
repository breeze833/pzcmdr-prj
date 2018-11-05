import qrcode
import sys
import hashlib

if __name__=='__main__':
    jpeg_file = 'test.jpg'
    message = None
    if len(sys.argv)==1:
        print('Syntax: {prg} <message to encode> [output JPEG file (defaut test.jpg)]'.format(prg=sys.argv[0]))
        exit()
    elif len(sys.argv)==2:
        message = sys.argv[1]
    else:
        message = sys.argv[1]
        jpeg_file = sys.argv[2]

    digest = hashlib.md5(message.encode()).hexdigest()
    print('The hashed message is: {data}'.format(data=digest))
    qr_code = qrcode.make(data=digest)
    qr_code.save(jpeg_file, format='jpeg')

