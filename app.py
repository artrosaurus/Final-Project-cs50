# app.py setup made with help of AI, structure and syntax for flask used from Finance problem set.
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError

load_dotenv() # Load environment variables from .env file
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tattoo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY') # Secret key from the file
db = SQLAlchemy(app)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH')

# Create a table with customers who want to book appointments (learned syntax from AI)
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow)

# Create table for portfolio images so admin can upload photos from the dashboard
class PortfolioImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/portfolio')
def portfolio():
    #Get all images for portfolio from database in descending order
    tattoos = PortfolioImage.query.order_by(PortfolioImage.upload_date.desc()).all()
    return render_template('portfolio.html', tattoos=tattoos)
    

@app.route('/contact')
def contact():
    return render_template("contact.html", body_class='contact')


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    
    # Excatly the same as finance problem set: check for request method and conditions
    if request.method == 'POST':
        
        #get the details of the person who wants to book a consultation
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")

        # Check if every field is filled
        if not name or not email or not phone:
            flash("All fields are required!", "error")
            return redirect(url_for('booking'))
        
        # Create customer willing to book consultation in database
        new_customer = Customer(name=name, email=email, phone=phone)

        # Save customer to database / syntax learned from AI
        db.session.add(new_customer)
        db.session.commit()

        flash("Thank you for booking a consultation! We will contact you soon.", "success")
        return redirect(url_for('index'))

    # If GET show the booking page
    return render_template("booking.html", body_class='booking')


@app.route('/delete-booking/<int:customer_id>', methods=['POST'])
def delete_booking(customer_id):
    if not session.get('logged_in'):
        flash('Please log in first', 'error')
        return redirect(url_for('login_admin'))
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        flash('Booking deleted', 'success')
    return redirect(url_for('admin'))


@app.route('/login-admin', methods=['GET', 'POST'])
def login_admin():
    
    # Excatly the same as finance problem set: check for request method and conditions
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username and password is equal to ones from .env
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            
            #store session (same as finance problem)
            session['logged_in'] = True

            flash('Login successful!', 'success')

            return redirect(url_for('admin'))

        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login_admin'))
    
    return render_template('login-admin.html')


@app.route('/admin')
def admin():
    # In this function, we are checking if user is logged in and session is valid and display logs from database.
    if not session.get('logged_in'):
        flash('Please log in first', 'error')
        return redirect(url_for('login_admin'))
    
    # Here we get a customers logs from database
    customers = Customer.query.all()

    # Here we get all uploaded portfolio image to display in admin panel
    portfolio_images = PortfolioImage.query.order_by(PortfolioImage.upload_date.desc()).all()

    return render_template('admin.html', customers=customers, portfolio_images=portfolio_images)


@app.route('/upload-image', methods=['POST'])
def upload_image():
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in first', 'error')
        return redirect(url_for('login_admin'))
    
    # Get list of all uploaded files (multiple=true in HTML)
    files = request.files.getlist('image')
    
    # Check if any files were uploaded
    if not files or files[0].filename == '':
        flash('No files selected', 'error')
        return redirect(url_for('admin'))
    
    uploaded_count = 0
    formats = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Loop through each uploaded file
    for file in files:
        # Check if file has valid format
        if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in formats:
            # Generate unique filename with timestamp and counter
            filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uploaded_count}_{file.filename}"
            
            # Save file to static/images folder
            file.save(os.path.join('static/images', filename))
            
            # Add to database
            new_image = PortfolioImage(filename=filename)
            db.session.add(new_image)
            uploaded_count += 1
    
    # Commit all uploads at once
    db.session.commit()
    
    if uploaded_count > 0:
        flash(f'{uploaded_count} image(s) uploaded successfully', 'success')
    else:
        flash('No valid images uploaded', 'error')
    
    return redirect(url_for('admin'))


@app.route('/delete-image/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    if not session.get('logged_in'):
        flash('Please log in first', 'error')
        return redirect(url_for('login_admin'))
    
    image = PortfolioImage.query.get(image_id)
    if image:
        # Delete file from disk only if it exists
        file_path = os.path.join('static/images', image.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete from database
        db.session.delete(image)
        db.session.commit()
        flash('Image deleted', 'success')
    
    return redirect(url_for('admin'))


@app.route('/delete-images', methods=['POST'])
def delete_images():
    if not session.get('logged_in'):
        flash('Please log in first', 'error')
        return redirect(url_for('login_admin'))
    
    # Associate checked value with image_id 
    checked_value = request.form.get('delete')
    if checked_value:
        selected_images = [checked_value]
    else:
        submitted_images = request.form.getlist('image_ids')
        if not submitted_images:
            flash('No images selected', 'error')
            return redirect(url_for('admin'))
        selected_images = submitted_images
    
    # Convert submitted image id strings to ints
    try:
        selected_images = [int(i) for i in selected_images]
    except (TypeError, ValueError):
        flash('Invalid image selection', 'error')
        return redirect(url_for('admin'))
    
    # Delete DB rows and files for the selected image ids
    matched_images = PortfolioImage.query.filter(PortfolioImage.id.in_(selected_images)).all()
    removed_count = 0
    for image_record in matched_images:
        image_path = os.path.join('static', 'images', image_record.filename)
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except OSError:
                pass
        db.session.delete(image_record)
        removed_count += 1

    db.session.commit()
    flash(f'{removed_count} image(s) deleted', 'success')
    return redirect(url_for('admin'))


@app.route('/logout')
def logout():
    # Clear the session to log out the user
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))
    

with app.app_context():
    db.create_all()
    # Automatically register any image files present in static/images,
    # so people who clone repo can see gallery. (this is a real-life project, so when i deploy it,
    # it will create empty database.)
    
    def register_images_from_static_folder():
        images_directory = os.path.join(app.root_path, 'static', 'images')
        formats = {'png', 'jpg', 'jpeg', 'gif'}

        if not os.path.isdir(images_directory):
            return

        new_images_count = 0
        for filename in sorted(os.listdir(images_directory)):
            filepath = os.path.join(images_directory, filename)
            if not os.path.isfile(filepath):
                continue
            if '.' not in filename:
                continue
            extension = filename.rsplit('.', 1)[1].lower()
            if extension not in formats:
                continue

            # Only add if not already present in DB
            existing = PortfolioImage.query.filter_by(filename=filename).first()
            if existing:
                continue

            try:
                db.session.add(PortfolioImage(filename=filename))
                db.session.commit()
                new_images_count += 1
            except IntegrityError:
                # Another process may have inserted the row concurrently; rollback and continue
                db.session.rollback()

        if new_images_count:
            print(f"Registered {new_images_count} images from static/images into PortfolioImage table")

    register_images_from_static_folder()

if __name__ == '__main__':
    app.run(debug=True) 