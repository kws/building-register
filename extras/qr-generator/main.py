import qrcode
from PIL import ImageDraw

qr_code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

qr_code.add_data('https://reg.sfintra.net/')
qr_code.make()

qr_image = qr_code.make_image(fill_color='black', back_color="white").convert('RGB')

draw = ImageDraw.Draw(qr_image)

w, h = qr_image.size

# White logo background
draw.rounded_rectangle((
	w / 2 - 60,
	h / 2 - 30,
	w / 2 + 60,
	h / 2 + 30
), radius=10, outline='black', fill='white', width=5)

# Black circle
draw.ellipse((
	w / 2 - 20 - 23,
	h / 2 - 20,
	w / 2 + 20 - 23,
	h / 2 + 20
), fill='black')

# Black square
draw.rectangle((
	w / 2 - 20 + 23,
	h / 2 - 20,
	w / 2 + 20 + 23,
	h / 2 + 20
), fill='black')

# save the QR code generated
qr_image.save('sf-reg-url-qr.png')

print('QR code generated!')
