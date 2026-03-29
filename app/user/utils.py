from flask import url_for,current_app
import secrets
from PIL import Image
import os
from flask_mail import Message
from app import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pic', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    # Generate the reset token
    token = user.get_reset_token()

    # Create the email message
    msg = Message(
        subject='Password Reset Request',
        sender=current_app.config['MAIL_USERNAME'],  # your TestMail email
        recipients=[user.email]
    )
    
    msg.body = f'''Hello {user.username},

To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not request this password reset, please ignore this email.
'''

    try:
        mail.send(msg)
        print(f"Password reset email sent to {user.email}")
    except Exception as e:
        print(f"Failed to send email: {e}")