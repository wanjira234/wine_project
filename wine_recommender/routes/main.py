from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user, logout_user
from datetime import datetime
from forms.preferences import UserPreferencesForm
from models.common.enums import (
    WineTraitCategory, WineTrait, WineCategory, WineType,
    ExperienceLevel, DrinkingFrequency, Currency, BodyType,
    FlavorIntensity, PriceSensitivity, QualityPreference
)
from models.wine.recommendations import WineRecommender
from models.order import Order
from models.order_item import OrderItem
from extensions import db
import json

main = Blueprint('main', __name__)

def minimize_wine_data(wine):
    """Helper function to minimize wine data stored in session.
    Handles both dictionary and object formats."""
    if isinstance(wine, dict):
        return {
            'id': str(wine.get('id')),
            'title': wine.get('title'),
            'price': float(wine.get('price', 0)),
            'points': int(wine.get('points', 0))
        }
    else:
        return {
            'id': str(wine.id),
            'title': wine.title,
            'price': float(wine.price),
            'points': int(wine.points)
        }

def get_cart_totals(cart_items):
    """Helper function to calculate cart totals."""
    subtotal = sum(item.get('price', 0) * item.get('quantity', 0) for item in cart_items)
    shipping_cost = 10 if subtotal < 100 else 0
    return subtotal, shipping_cost, subtotal + shipping_cost

def get_traits_by_category():
    """Helper function to organize wine traits by category."""
    traits_by_category = {}
    
    # Get all traits if not already initialized
    if not hasattr(current_app, 'all_traits'):
        current_app.all_traits = [trait.value for trait in WineTrait]
    
    for category in WineTraitCategory:
        traits_by_category[category.value] = [
            trait.value for trait in WineTrait 
            if trait.value in current_app.all_traits
        ]
    return traits_by_category

@main.route('/')
def index():
    traits_by_category = get_traits_by_category()
    trait_categories = [category.value for category in WineTraitCategory]
    return render_template('home.html', 
                         traits_by_category=traits_by_category,
                         trait_categories=trait_categories,
                         current_year=datetime.now().year)

@main.route('/about')
def about():
    return render_template('about.html', current_year=datetime.now().year)

@main.route('/catalog')
def catalog():
    return render_template('catalog.html', current_year=datetime.now().year)

@main.route('/predict')
@login_required
def predict():
    return render_template('predict.html', current_year=datetime.now().year)

@main.route('/contact')
def contact():
    return render_template('contact.html', current_year=datetime.now().year)

@main.route('/profile')
@login_required
def profile():
    """Display user profile and preferences."""
    return render_template('profile.html', 
                         preferences={
                             'experience': current_user.get_preferences().get('experience').get('experience_level'),
                             'wine_types': current_user.get_preferences().get('wine_types'),
                             'taste': current_user.get_preferences('taste'),
                             'regions': current_user.get_preferences('regions'),
                             'budget': current_user.get_preferences('budget')
                         })

@main.route('/update_wine_experience', methods=['POST'])
@login_required
def update_wine_experience():
    """Update user's wine experience preferences."""
    if request.method == 'POST':
        experience = request.form.getlist('experience[]')
        current_user.update_preferences('experience', experience)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True})
        flash('Wine experience preferences updated successfully!', 'success')
        return redirect(url_for('main.profile'))

@main.route('/update_wine_types', methods=['POST'])
@login_required
def update_wine_types():
    """Update user's preferred wine types."""
    if request.method == 'POST':
        wine_types = request.form.getlist('wine_types[]')
        current_user.update_preferences('wine_types', wine_types)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True})
        flash('Wine type preferences updated successfully!', 'success')
        return redirect(url_for('main.profile'))

@main.route('/update_taste_preferences', methods=['POST'])
@login_required
def update_taste_preferences():
    """Update user's taste preferences."""
    if request.method == 'POST':
        taste_prefs = request.form.getlist('taste[]')
        current_user.update_preferences('taste', taste_prefs)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True})
        flash('Taste preferences updated successfully!', 'success')
        return redirect(url_for('main.profile'))

@main.route('/update_regions', methods=['POST'])
@login_required
def update_regions():
    """Update user's preferred wine regions."""
    if request.method == 'POST':
        regions = request.form.getlist('regions[]')
        current_user.update_preferences('regions', regions)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True})
        flash('Region preferences updated successfully!', 'success')
        return redirect(url_for('main.profile'))

@main.route('/update_budget', methods=['POST'])
@login_required
def update_budget():
    """Update user's budget preferences."""
    if request.method == 'POST':
        budget = {
            'min_price': float(request.form.get('min_price', 60.0)),
            'max_price': float(request.form.get('max_price', 200.0))
        }
        current_user.update_preferences('budget', budget)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True})
        flash('Budget preferences updated successfully!', 'success')
        return redirect(url_for('main.profile'))

@main.route('/delete_profile', methods=['POST'])
@login_required
def delete_profile():
    """Delete user profile."""
    if request.method == 'POST':
        password = request.form.get('password')
        if not current_user.check_password(password):
            flash('Incorrect password. Profile deletion cancelled.', 'error')
            return redirect(url_for('main.profile'))
        
        # Delete the user's profile
        user = current_user._get_current_object()
        logout_user()
        db.session.delete(user)
        db.session.commit()
        
        flash('Your profile has been deleted successfully.', 'success')
        return redirect(url_for('main.home'))

@main.route('/preferences', methods=['GET', 'POST'])
@login_required
def edit_preferences():
    form = UserPreferencesForm()
    traits_by_category = get_traits_by_category()
    trait_categories = [category.value for category in WineTraitCategory]
    
    if request.method == 'GET':
        # Pre-fill form with existing preferences
        if current_user.preferences_model:
            wine_experience = current_user.preferences_model.wine_experience or {}
            wine_style = current_user.preferences_model.wine_style or {}
            wine_traits = current_user.preferences_model.wine_traits or {}
            
            # Experience and drinking frequency
            form.experience_level.data = wine_experience.get('experience_level', ExperienceLevel.BEGINNER.value)
            form.drinking_frequency.data = wine_experience.get('drinking_frequency', DrinkingFrequency.OCCASIONALLY.value)
            
            # Budget preferences
            price_ranges = wine_style.get('price_ranges', {})
            regular = price_ranges.get('regular', {})
            special = price_ranges.get('special', {})
            
            form.min_price.data = regular.get('min', 15)
            form.max_price.data = regular.get('max', 50)
            form.currency.data = regular.get('currency', Currency.USD.value)
            form.special_occasion_price.data = special.get('min', 100)
            
            # Wine style preferences
            form.red_wine_body.data = wine_style.get('body_preference', BodyType.MEDIUM.value)
            form.sweetness_level.data = wine_style.get('sweetness_level', SweetnessLevel.DRY.value)
            form.flavor_intensity.data = wine_style.get('flavor_intensity', FlavorIntensity.MEDIUM.value)
            
            # Wine traits
            form.wine_traits.data = wine_traits.get('preferred_traits', [])
    
    if form.validate_on_submit():
        # Get array preferences from form
        wine_traits_list = request.form.getlist('wine_traits')
        
        # Create or update preferences model
        if not current_user.preferences_model:
            current_user.preferences_model = UserPreference(user_id=current_user.id)
        
        print("\n=============== EXECUTING PREFERENCES EDIT PAGE ================\n{}".format(current_user))
        print("{}\n".format(current_user.preferences_model))
        
        # Update wine experience
        current_user.preferences_model.wine_experience = {
            'experience_level': form.experience_level.data,
            'drinking_frequency': form.drinking_frequency.data,
            'wine_types': []  # This will be updated through another form
        }
        
        # Update wine style
        current_user.preferences_model.wine_style = {
            'body_preference': form.red_wine_body.data,
            'sweetness_level': form.sweetness_level.data,
            'flavor_intensity': form.flavor_intensity.data,
            'price_ranges': {
                'regular': {
                    'min': form.min_price.data,
                    'max': form.max_price.data,
                    'currency': form.currency.data
                },
                'special': {
                    'min': form.special_occasion_price.data,
                    'max': form.special_occasion_price.data * 2,  # Just an example
                    'currency': form.currency.data
                }
            }
        }
        
        # Update wine traits
        current_user.preferences_model.wine_traits = {
            'preferred_traits': wine_traits_list,
            'disliked_characteristics': []  # This will be updated through another form
        }
        
        # Save changes
        current_user.preferences_model.save()
        
        flash('Your preferences have been updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('preferences.html',
                         form=form,
                         traits_by_category=traits_by_category,
                         trait_categories=trait_categories,
                         current_year=datetime.now().year)

@main.route('/update_wine_preferences', methods=['POST'])
@login_required
def update_wine_preferences():
    wine_types = request.form.getlist('wine_types')
    
    if not current_user.preferences_model:
        current_user.preferences_model = UserPreference(user_id=current_user.id)
    
    # Update wine experience
    wine_experience = current_user.preferences_model.wine_experience or {}
    wine_experience['wine_types'] = wine_types
    current_user.preferences_model.wine_experience = wine_experience
    current_user.preferences_model.save()
    
    flash('Wine preferences updated successfully!', 'success')
    return redirect(url_for('main.profile'))

@main.route('/update_tasting_profile', methods=['POST'])
@login_required
def update_tasting_profile():
    if not current_user.preferences_model:
        current_user.preferences_model = UserPreference(user_id=current_user.id)
    
    # Update wine experience
    wine_experience = current_user.preferences_model.wine_experience or {}
    wine_experience.update({
        'experience_level': request.form.get('experience_level'),
        'drinking_frequency': request.form.get('drinking_frequency')
    })
    current_user.preferences_model.wine_experience = wine_experience
    
    # Update wine style
    wine_style = current_user.preferences_model.wine_style or {}
    wine_style.update({
        'body_preference': request.form.get('body_preference'),
        'flavor_intensity': request.form.get('flavor_intensity')
    })
    current_user.preferences_model.wine_style = wine_style
    
    current_user.preferences_model.save()
    flash('Tasting profile updated successfully!', 'success')
    return redirect(url_for('main.profile'))

@main.route('/update_budget_preferences', methods=['POST'])
@login_required
def update_budget_preferences():
    if not current_user.preferences_model:
        current_user.preferences_model = UserPreference(user_id=current_user.id)
    
    # Update wine style with price ranges
    wine_style = current_user.preferences_model.wine_style or {}
    wine_style['price_ranges'] = {
        'regular': {
            'min': float(request.form.get('min_price')),
            'max': float(request.form.get('max_price')),
            'currency': request.form.get('currency')
        },
        'special': {
            'min': float(request.form.get('special_occasion_price')),
            'max': float(request.form.get('special_occasion_price')) * 2,  # Example
            'currency': request.form.get('currency')
        }
    }
    current_user.preferences_model.wine_style = wine_style
    
    current_user.preferences_model.save()
    flash('Budget preferences updated successfully!', 'success')
    return redirect(url_for('main.profile'))

@main.route('/update_wine_traits', methods=['POST'])
@login_required
def update_wine_traits():
    if not current_user.preferences_model:
        current_user.preferences_model = UserPreference(user_id=current_user.id)
    
    # Get all selected traits
    all_traits = request.form.getlist('wine_traits')
    
    # Update wine traits
    current_user.preferences_model.wine_traits = {
        'preferred_traits': all_traits,
        'disliked_characteristics': request.form.getlist('disliked_characteristics', [])
    }
    
    current_user.preferences_model.save()
    flash('Wine traits updated successfully!', 'success')
    return redirect(url_for('main.profile'))

@main.route('/update_account_settings', methods=['POST'])
@login_required
def update_account_settings():
    if not current_user.check_password(request.form.get('current_password')):
        flash('Current password is incorrect!', 'error')
        return redirect(url_for('main.profile'))
    
    current_user.email = request.form.get('email')
    current_user.username = request.form.get('username')
    
    new_password = request.form.get('new_password')
    if new_password:
        current_user.set_password(new_password)
    
    current_user.save()
    flash('Account settings updated successfully!', 'success')
    return redirect(url_for('main.profile'))

@main.route('/recommendations')
@login_required
def recommendations():
    page = request.args.get('page', 1, type=int)
    min_points = request.args.get('min_points', type=int)
    country = request.args.get('country')
    variety = request.args.get('variety')
    
    recommender = WineRecommender(current_user)
    
    # Create filters dictionary for the recommender
    filters = {
        'min_points': min_points if min_points else None,
        'country': country if country else None,
        'variety': variety if variety else None
    }
    # Remove None values from filters
    filters = {k: v for k, v in filters.items() if v is not None}
    
    all_recommendations = recommender.get_recommendations(filters=filters)
    
    # Paginate recommendations
    per_page = 9
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    current_recommendations = all_recommendations[start_idx:end_idx]
    
    # Store minimal data in session
    session['recommendations'] = [minimize_wine_data(wine) for wine in current_recommendations]
    
    # Get minimal filter options - handle dictionary access
    countries = sorted(list(set(wine.get('country', '') for wine in all_recommendations)))[:20]
    varieties = sorted(list(set(wine.get('variety', '') for wine in all_recommendations)))[:20]
    
    # Remove empty strings from filter options
    countries = [c for c in countries if c]
    varieties = [v for v in varieties if v]
    
    return render_template('recommendations.html',
                         recommendations=current_recommendations,
                         countries=countries,
                         varieties=varieties,
                         selected_country=country,
                         selected_variety=variety,
                         min_points=min_points,
                         current_year=datetime.now().year)

@main.route('/api/provinces')
@login_required
def get_provinces():
    """Get provinces for a given country."""
    country = request.args.get('country')
    if not country:
        return jsonify([])
    
    recommender = WineRecommender(current_user.id)
    provinces = recommender.get_unique_provinces(country)
    return jsonify(provinces)

@main.route('/cart')
@login_required
def cart():
    # Initialize cart if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []
    
    # Ensure all cart items have a quantity
    for item in session['cart']:
        if 'quantity' not in item:
            item['quantity'] = 1
    
    session.modified = True
    subtotal, shipping_cost, total = get_cart_totals(session['cart'])
    
    return render_template('cart.html',
                         cart_items=session['cart'],
                         subtotal=subtotal,
                         shipping_cost=shipping_cost,
                         total=total)

@main.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    wine_id = request.form.get('wine_id')
    try:
        quantity = int(request.form.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1
    
    if not wine_id:
        return jsonify({'success': False, 'message': 'No wine ID provided'})
    
    # Initialize cart if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []
    
    # Find wine in recommendations
    wine = next(
        (wine for wine in session.get('recommendations', [])
         if str(wine['id']) == str(wine_id)),
        None
    )
    
    if not wine:
        return jsonify({'success': False, 'message': 'Wine not found'})
    
    # Check if wine already in cart
    cart_item = next(
        (item for item in session['cart']
         if str(item.get('id')) == str(wine_id)),
        None
    )
    
    if cart_item:
        # Ensure quantity exists and increment it
        if 'quantity' not in cart_item:
            cart_item['quantity'] = 0
        cart_item['quantity'] += quantity
    else:
        # Add new item with required fields
        cart_item = {
            'id': wine['id'],
            'title': wine['title'],
            'price': wine['price'],
            'quantity': quantity
        }
        session['cart'].append(cart_item)
    
    session.modified = True
    
    # Calculate cart count safely
    cart_count = sum(item.get('quantity', 0) for item in session['cart'])
    
    return jsonify({
        'success': True,
        'message': 'Added to cart successfully',
        'cart_count': cart_count
    })

@main.route('/cart/update', methods=['POST'])
@login_required
def update_cart():
    try:
        data = request.get_json()
        item_id = data.get('item_id')
        change = data.get('change', 0)
        
        if not item_id:
            return jsonify({'success': False, 'message': 'No item ID provided'}), 400

        # Get cart from session
        cart = session.get('cart', [])
        
        # Find the item in cart
        item = next((item for item in cart if str(item['id']) == str(item_id)), None)
        
        if not item:
            return jsonify({'success': False, 'message': 'Item not found in cart'}), 404
        
        # Update quantity
        current_quantity = item.get('quantity', 0)
        new_quantity = current_quantity + change
        
        if new_quantity < 1:
            # Remove item if quantity would be less than 1
            cart.remove(item)
        else:
            item['quantity'] = new_quantity
        
        session['cart'] = cart
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': 'Cart updated successfully',
            'cart_count': sum(item.get('quantity', 0) for item in cart)
        })
        
    except Exception as e:
        current_app.logger.error(f"Error updating cart: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred while updating cart'}), 500

@main.route('/cart/remove', methods=['POST'])
@login_required
def remove_from_cart():
    # Remove item logic here
    # This should remove the item from the session or database
    try:
        data = request.get_json()
        item_id = data.get('item_id')
        
        print("ITEM ID::  {}\n".format(item_id))

        if not item_id:
            return jsonify({'success': False, 'message': 'No item ID provided'}), 400
        
        # get cart from session
        cart = session.get('cart', [])

        # find the item in the cart
        item = next((item for item in cart if str(item['id']) == str(item_id)), None)
        if not item:
            return jsonify({'success': False, 'message': 'Item not found in cart'}), 404
        
        # remove the item
        cart.remove(item)
        session['cart'] = cart
        session.modified = True

        return jsonify({
            'success': True,
            'message': 'Item removed successfully',
            'cart_count': sum(i.get('quantity', 0) for i in cart)
        })
    except Exception as e:
        current_app.logger.error(f"Error removing item from cart: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred while removing item'}), 500

@main.route('/checkout')
@login_required
def checkout():
    """Handle the checkout process."""
    # Get cart items from the session
    #cart_items = []  # Replace with actual cart items retrieval
    cart_items = session.get('cart', [])
    
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('main.cart'))
    
    # Calculate order summary
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    shipping_cost = 0 if subtotal > 100 else 10  # Free shipping over $100
    discount = 0  # Implement discount logic if needed
    total = subtotal + shipping_cost - discount
    
    return render_template('checkout.html',
                         cart_items=cart_items,
                         subtotal=subtotal,
                         shipping_cost=shipping_cost,
                         discount=discount,
                         total=total,
                         current_year=datetime.now().year)

@main.route('/process-checkout', methods=['POST'])
@login_required
def process_checkout():
    """Finalize checkout by creating an order and clearing the cart.""" 
    if not request.form:
        flash('Invalid form submission.', 'error')
        return redirect(url_for('main.checkout'))
    
    # Here you would typically:
    # 1. Validate the form data
    # 2. Process the payment
    # 3. Create an order record
    # 4. Clear the cart
    # 5. Send confirmation email
    try:
        # 1. Validate form data
        shipping_address = request.form.get('address')
        billing_address = request.form.get('billing_address') or shipping_address

        if not shipping_address:
            flash('Shipping address is required.', 'error')
            return redirect(url_for('main.checkout'))

        cart_items = session.get('cart', [])
        if not cart_items:
            flash('Your cart is empty.', 'warning')
            return redirect(url_for('main.cart'))

        # 2. Simulate payment processing
        payment_success = True  # Replace with real payment logic
        if not payment_success:
            flash('Payment failed. Please try again.', 'error')
            return redirect(url_for('main.checkout'))

        # 3. Create Order
        subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
        shipping_cost = 0 if subtotal > 100 else 10
        discount = 0
        total = subtotal + shipping_cost - discount

        order = Order(
            user_id=current_user.id,
            total_amount=total,
            shipping_address=shipping_address,
            billing_address=billing_address
        )
        
        db.session.add(order)
        db.session.flush()  # So order.id is available

        # 3b. Add items using OrderItem model
        for item in cart_items:
            item_model = OrderItem(
                order_id=order.id,
                wine_id=item['id'],
                wine_name=item['title'],
                quantity=item['quantity'],
                price_per_unit=item['price']
            )
            db.session.add(item_model)

        # Update order status
        order.update_payment_status('paid')
        order.update_status('confirmed')
        db.session.commit()

        # 4. Clear the cart
        session['cart'] = []
        session.modified = True

        # 5. (Optional) Send confirmation email
        # send_order_confirmation_email(current_user.email, order)
        print("\n\n{}\n".format(url_for('main.orders')))
        flash('Your order has been placed successfully!', 'success')
        return redirect(url_for('main.orders'))

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error during checkout: {e}")
        flash('Something went wrong while placing your order.', 'error')
        return redirect(url_for('main.checkout'))

    
    # For now, just show a success message
    #flash('Order placed successfully! This is a demo checkout.', 'success')
    #return redirect(url_for('main.orders'))

@main.route('/guide')
def guide():
    return render_template('guide.html')

@main.route('/orders')
@login_required
def orders():
    """Display user's order history."""
    # For now, return an empty orders page until we implement the order system
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).all()
    return render_template('orders.html', 
                         orders=user_orders,  # This will be replaced with actual orders when implemented
                         current_year=datetime.now().year) 