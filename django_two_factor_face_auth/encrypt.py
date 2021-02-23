from Crypto.Cipher import AES
from Crypto import Random
import face_recognition
from django.core.files.base import ContentFile

key = b'0123456789012345'
iv = b'0123456789012345'

def encrypti(image):
  
    name = image.name.split('.')[0]
    image_file =  image.open('rb')
    image_data = image_file.read()
    cfb_cipher = AES.new(key, AES.MODE_CFB, iv)
    enc_data = cfb_cipher.encrypt(image_data)
    enc_file = ContentFile(enc_data, name = name + ".enc", )
    image_file.close()
    return enc_file

def decrypti(encimage):
    
    name = encimage.name.split('.')[0]
    enc_file = encimage.open('rb')
    enc_data = enc_file.read()
    cfb_decipher = AES.new(key, AES.MODE_CFB, iv)
    plain_data = cfb_decipher.decrypt(enc_data)
    dec_file = ContentFile(plain_data, name = name + ".png")
    enc_file.close()
    return dec_file

