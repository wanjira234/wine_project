from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request, current_app
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime, timedelta
from extensions import db
from models.user.user import User
from models.common.enums import UserRole, WineType, WineRegion
from models.wine.wine import Wine
from models.settings.settings import Settings
from forms.wine import AddWineForm
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

@admin.route('/dashboard/')
@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Display admin dashboard with statistics."""
    try:
        # Get user statistics
        total_users = User.query.count()
        admin_users = User.query.filter_by(is_admin=True).count()
        regular_users = total_users - admin_users
        
        # Get wine statistics
        total_wines = Wine.query.count() or 0
        
        # Default data in case there are no wines
        wine_types = ['Red', 'White', 'Rosé', 'Sparkling']
        type_counts = [0, 0, 0, 0]
        wine_regions = ['Napa Valley', 'Bordeaux', 'Tuscany', 'Rioja', 'Champagne']
        region_counts = [0, 0, 0, 0, 0]
        price_ranges = ['$0-20', '$21-50', '$51-100', '$101-200', '$201+']
        price_counts = [0, 0, 0, 0, 0]
        stock_levels = ['Out of Stock', 'Low Stock', 'In Stock']
        stock_counts = [0, 0, 0]
        
        # Only try to get real data if we have wines
        if total_wines > 0:
            # Wine Types Distribution
            wine_types_data = db.session.query(
                Wine.type, 
                func.count(Wine.id).label('count')
            ).group_by(Wine.type).all()
            
            if wine_types_data:
                wine_types = [type[0].value for type in wine_types_data]
                type_counts = [type[1] for type in wine_types_data]
            
            # Wine Regions Distribution (Top 5)
            wine_regions_data = db.session.query(
                Wine.region, 
                func.count(Wine.id).label('count')
            ).group_by(Wine.region).order_by(func.count(Wine.id).desc()).limit(5).all()
            
            if wine_regions_data:
                wine_regions = [region[0].value.replace('_', ' ').title() for region in wine_regions_data]
                region_counts = [region[1] for region in wine_regions_data]
            
            # Price Range Distribution
            price_counts = [
                Wine.query.filter(Wine.price <= 20).count(),
                Wine.query.filter(Wine.price > 20, Wine.price <= 50).count(),
                Wine.query.filter(Wine.price > 50, Wine.price <= 100).count(),
                Wine.query.filter(Wine.price > 100, Wine.price <= 200).count(),
                Wine.query.filter(Wine.price > 200).count()
            ]
            
            # Stock Level Analysis
            stock_counts = [
                Wine.query.filter(Wine.stock == 0).count(),
                Wine.query.filter(Wine.stock > 0, Wine.stock <= 10).count(),
                Wine.query.filter(Wine.stock > 10).count()
            ]
        
        # User roles distribution
        role_distribution = {
            'Customers': regular_users,
            'Admins': admin_users,
            'Sommeliers': User.query.filter_by(role=UserRole.SOMMELIER).count()
        }
        
        return render_template('admin/dashboard.html',
                             users=User.query.all(),
                             total_users=total_users,
                             total_wines=total_wines,
                             wine_types=wine_types,
                             type_counts=type_counts,
                             wine_regions=wine_regions,
                             region_counts=region_counts,
                             price_ranges=price_ranges,
                             price_counts=price_counts,
                             stock_levels=stock_levels,
                             stock_counts=stock_counts,
                             role_distribution=role_distribution,
                             current_year=datetime.now().year,
                             body_class='admin-page')
                             
    except Exception as e:
        current_app.logger.error(f"Error in dashboard route: {str(e)}")
        flash("An error occurred while loading the dashboard. Please try again.", "danger")
        return redirect(url_for('main.index'))

@admin.route('/inventory')
@login_required
@admin_required
def inventory():
    """Display wine inventory."""
    page = request.args.get('page', 1, type=int)
    per_page = 20  # Number of items per page
    
    # Get filter parameters
    wine_type = request.args.get('type')
    region = request.args.get('region')
    stock_filter = request.args.get('stock')
    search = request.args.get('search')
    
    # Build query
    query = Wine.query
    
    if wine_type:
        query = query.filter(Wine.type == WineType(wine_type))
    if region:
        query = query.filter(Wine.region == WineRegion(region))
    if stock_filter:
        if stock_filter == 'low':
            query = query.filter(Wine.stock <= 10)
        elif stock_filter == 'out':
            query = query.filter(Wine.stock == 0)
        elif stock_filter == 'available':
            query = query.filter(Wine.stock > 0)
    if search:
        query = query.filter(Wine.name.ilike(f'%{search}%'))
    
    # Get total count for pagination
    total = query.count()
    
    # Get paginated results
    wines = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Create form instance
    form = AddWineForm()
    
    return render_template('admin/inventory.html',
                         wines=wines,
                         wine_types=WineType,
                         wine_regions=WineRegion,
                         current_year=datetime.now().year,
                         body_class='admin-page',
                         total=total,
                         page=page,
                         per_page=per_page,
                         form=form)

@admin.route('/wine/add', methods=['POST'])
@login_required
@admin_required
def add_wine():
    """Add a new wine to inventory."""
    form = AddWineForm()
    if form.validate_on_submit():
        try:
            wine = Wine.create_wine(
                name=form.name.data,
                type=WineType(form.type.data),
                region=WineRegion(form.region.data),
                price=float(form.price.data),
                year=int(form.year.data) if form.year.data else None,
                description=form.description.data,
                stock=int(form.stock.data),
                image_url=form.image_url.data or None
            )
            flash(f'Wine "{wine.name}" has been added successfully.', 'success')
            return redirect(url_for('admin.inventory'))
        except Exception as e:
            flash(f'Failed to add wine: {str(e)}', 'danger')
            return redirect(url_for('admin.inventory'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
        return redirect(url_for('admin.inventory'))

@admin.route('/wine/<int:wine_id>/update-stock', methods=['POST'])
@login_required
@admin_required
def update_wine_stock(wine_id):
    """Update wine stock level."""
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
    """Delete a wine from inventory."""
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
    """Display user management page."""
    users = User.query.all()
    return render_template('admin/users.html', 
                         users=users, 
                         current_year=datetime.now().year,
                         body_class='admin-page')

@admin.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user."""
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
    """Toggle admin status for a user."""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot modify your own admin status.', 'danger')
    else:
        user.is_admin = not user.is_admin
        db.session.commit()
        flash(f'Admin status for {user.username} has been {"granted" if user.is_admin else "revoked"}.', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/wines')
@login_required
@admin_required
def wines():
    """Display wine catalog."""
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of items per page for grid view
    
    # Get filter parameters
    wine_type = request.args.get('type')
    region = request.args.get('region')
    search = request.args.get('search')
    
    # Build query
    query = Wine.query
    
    if wine_type:
        query = query.filter(Wine.type == WineType(wine_type))
    if region:
        query = query.filter(Wine.region == WineRegion(region))
    if search:
        query = query.filter(Wine.name.ilike(f'%{search}%'))
    
    # Get total count for pagination
    total = query.count()
    
    # Get paginated results
    wines = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/wines.html',
                         wines=wines,
                         wine_types=WineType,
                         wine_regions=WineRegion,
                         current_year=datetime.now().year,
                         body_class='admin-page',
                         total=total,
                         page=page,
                         per_page=per_page)

@admin.route('/settings')
@login_required
@admin_required
def settings():
    """Display and manage application settings."""
    all_settings = Settings.get_all_settings()
    return render_template('admin/settings.html', settings=all_settings)

@admin.route('/settings/update', methods=['POST'])
@login_required
@admin_required
def update_settings():
    """Update application settings."""
    try:
        settings_data = request.get_json()
        for key, value in settings_data.items():
            Settings.set_setting(key, value)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@admin.route('/wine/<int:wine_id>')
@login_required
@admin_required
def get_wine(wine_id):
    """Get wine data for editing."""
    try:
        wine = Wine.query.get_or_404(wine_id)
        return jsonify(wine.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@admin.route('/wine/<int:wine_id>/update', methods=['POST'])
@login_required
@admin_required
def update_wine(wine_id):
    """Update wine data."""
    form = AddWineForm()
    if form.validate_on_submit():
        try:
            wine = Wine.query.get_or_404(wine_id)
            
            # Debug print form data
            print("Form data:", form.data)
            
            # Update wine fields
            wine.name = form.name.data
            wine.type = WineType(form.type.data)
            wine.region = WineRegion(form.region.data)
            wine.price = float(form.price.data)
            wine.year = int(form.year.data) if form.year.data else None
            wine.description = form.description.data
            wine.stock = int(form.stock.data)
            wine.image_url = form.image_url.data or None
            
            # Debug print updated wine data
            print("Updated wine data:", {
                'name': wine.name,
                'type': wine.type,
                'region': wine.region,
                'price': wine.price,
                'year': wine.year,
                'description': wine.description,
                'stock': wine.stock,
                'image_url': wine.image_url
            })
            
            wine.save()
            flash(f'Wine "{wine.name}" has been updated successfully.', 'success')
            return redirect(url_for('admin.inventory'))
        except Exception as e:
            print("Error updating wine:", str(e))
            flash(f'Failed to update wine: {str(e)}', 'danger')
            return redirect(url_for('admin.inventory'))
    else:
        print("Form validation errors:", form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
        return redirect(url_for('admin.inventory')) 