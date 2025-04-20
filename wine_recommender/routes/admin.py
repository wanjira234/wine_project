from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime, timedelta
from extensions import db
from models.user.user import User
from models.common.enums import UserRole, WineType, WineRegion
from models.wine.wine import Wine
from sqlalchemy import func
import random

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get user statistics
    total_users = User.query.count()
    admin_users = User.query.filter_by(is_admin=True).count()
    regular_users = total_users - admin_users
    
    # Generate sample data for charts (replace with real data later)
    # Last 7 days of user registrations
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    registrations = [random.randint(5, 20) for _ in range(7)]
    
    # Wine categories distribution
    wine_categories = ['Red', 'White', 'Rosé', 'Sparkling', 'Dessert']
    category_counts = [random.randint(50, 200) for _ in range(len(wine_categories))]
    
    # User roles distribution
    role_distribution = {
        'Customers': regular_users,
        'Admins': admin_users,
        'Sommeliers': User.query.filter_by(role=UserRole.SOMMELIER).count()
    }
    
    # Monthly revenue data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    revenue_data = [random.randint(5000, 15000) for _ in range(len(months))]
    
    return render_template('admin/dashboard.html',
                         users=User.query.all(),
                         total_users=total_users,
                         dates=dates,
                         registrations=registrations,
                         wine_categories=wine_categories,
                         category_counts=category_counts,
                         role_distribution=role_distribution,
                         months=months,
                         revenue_data=revenue_data,
                         current_year=datetime.now().year,
                         body_class='admin-page')

@admin.route('/inventory')
@login_required
@admin_required
def inventory():
    wines = Wine.query.all()
    return render_template('admin/inventory.html',
                         wines=wines,
                         wine_types=WineType,
                         wine_regions=WineRegion,
                         current_year=datetime.now().year,
                         body_class='admin-page')

@admin.route('/wine/add', methods=['POST'])
@login_required
@admin_required
def add_wine():
    try:
        wine = Wine.create_wine(
            name=request.form['name'],
            type=WineType(request.form['type']),
            region=WineRegion(request.form['region']),
            price=float(request.form['price']),
            year=int(request.form['year']) if request.form['year'] else None,
            description=request.form['description'],
            stock=int(request.form['stock']),
            image_url=request.form['image_url'] or None
        )
        flash(f'Wine "{wine.name}" has been added successfully.', 'success')
        return redirect(url_for('admin.inventory'))
    except Exception as e:
        flash(f'Failed to add wine: {str(e)}', 'danger')
        return redirect(url_for('admin.inventory'))

@admin.route('/wine/<int:wine_id>/update-stock', methods=['POST'])
@login_required
@admin_required
def update_wine_stock(wine_id):
    try:
        wine = Wine.query.get_or_404(wine_id)
        data = request.get_json()
        wine.update_stock(data['stock'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@admin.route('/wine/<int:wine_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_wine(wine_id):
    try:
        wine = Wine.query.get_or_404(wine_id)
        db.session.delete(wine)
        db.session.commit()
        flash(f'Wine "{wine.name}" has been deleted.', 'success')
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', 
                         users=users, 
                         current_year=datetime.now().year,
                         body_class='admin-page')

@admin.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} has been deleted.', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/user/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot modify your own admin status.', 'danger')
    else:
        user.is_admin = not user.is_admin
        db.session.commit()
        flash(f'Admin status for {user.username} has been {"granted" if user.is_admin else "revoked"}.', 'success')
    return redirect(url_for('admin.users')) 