from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, PasswordEntry
from . import db
import string, random, secrets

main = Blueprint('main', __name__)


@main.route('/about')
def landing():
    return render_template('landing.html')

@main.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        data = request.form

        length = int(data.get('length', 12))
        has_lower = 'hasLower' in data
        has_upper = 'hasUpper' in data
        has_digits = 'hasDigits' in data
        has_symbols = 'hasSymbols' in data

        char_list = ""

        if has_lower:
            char_list += string.ascii_lowercase

        if has_upper:
            char_list += string.ascii_uppercase

        if has_digits:
            char_list += string.digits

        if has_symbols:
            char_list += string.punctuation

        if not char_list:
            return render_template('index.html', error_message="Please select at least on character type for the password.")

        print("Char list:", char_list)

        result = []

        for i in range (length):
            randomChar = secrets.choice(char_list)
            result.append(randomChar)

        password = "".join(result)
        return render_template('index.html', generated_password=password)
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    passwords = PasswordEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', name=current_user.name, passwords=passwords)

@main.route('/profile', methods=['POST'])
@login_required
def save_password():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')


    # Create a new user with the form data. Hash the password for security so not to save the plain text
    new_entry = PasswordEntry(name=name, email=email, password=password, user_id=current_user.id)

    # Add new user to database
    db.session.add(new_entry)
    db.session.commit()

    return redirect(url_for('main.profile'))

@main.route('/delete_password/<int:id>', methods=['POST'])
@login_required
def delete_password(id):
    entry = PasswordEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash('You do not have permission to delete this password')
        return redirect(url_for('main.profile'))


    db.session.delete(entry)
    db.session.commit()
    flash('Password entry deleted successfully.')

    return redirect(url_for('main.profile'))


if __name__ == '__main__':
    main.run()
