from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = 'modern_library_system_2025_secure_key'

# Modern Library System - Enhanced User Database with new styling theme
library_users = {
    'admin': {
        'password': 'admin2025',
        'role': 'System Administrator',
        'name': 'Emily Rodriguez',
        'email': 'admin@modernlibrary.edu',
        'employee_id': 'ADM001',
        'last_login': None,
        'access_level': 'full'
    },
    'librarian': {
        'password': 'lib123',
        'role': 'Senior Librarian',
        'name': 'David Thompson',
        'email': 'david.thompson@modernlibrary.edu',
        'employee_id': 'LIB002',
        'last_login': None,
        'access_level': 'high'
    },
    'student': {
        'password': 'student456',
        'role': 'Graduate Student',
        'name': 'Maya Patel',
        'email': 'maya.patel@university.edu',
        'member_id': 'GRD2024001',
        'last_login': None,
        'access_level': 'standard'
    },
    'faculty': {
        'password': 'faculty789',
        'role': 'Research Faculty',
        'name': 'Prof. James Wilson',
        'email': 'j.wilson@university.edu',
        'member_id': 'FAC2024001',
        'last_login': None,
        'access_level': 'extended'
    },
    'researcher': {
        'password': 'research2024',
        'role': 'Research Scholar',
        'name': 'Dr. Lisa Chang',
        'email': 'lisa.chang@research.edu',
        'member_id': 'RES2024001',
        'last_login': None,
        'access_level': 'research'
    }
}

# Enhanced book catalog with more diverse content
book_catalog = [
    {'id': 1, 'title': 'Advanced Python Programming', 'author': 'Luciano Ramalho', 'isbn': '978-1492051282', 'available': True, 'category': 'Programming'},
    {'id': 2, 'title': 'Software Engineering Best Practices', 'author': 'Robert Martin', 'isbn': '978-0134494166', 'available': False, 'category': 'Engineering'},
    {'id': 3, 'title': 'Modern Web Development', 'author': 'Ethan Brown', 'isbn': '978-1491949308', 'available': True, 'category': 'Web Development'},
    {'id': 4, 'title': 'Machine Learning Fundamentals', 'author': 'Andreas Müller', 'isbn': '978-1449369415', 'available': True, 'category': 'AI/ML'},
    {'id': 5, 'title': 'Cloud Computing Architecture', 'author': 'Thomas Erl', 'isbn': '978-0133387520', 'available': False, 'category': 'Cloud'},
    {'id': 6, 'title': 'Data Science with Python', 'author': 'Wes McKinney', 'isbn': '978-1491957660', 'available': True, 'category': 'Data Science'},
    {'id': 7, 'title': 'Cybersecurity Fundamentals', 'author': 'Charles Brooks', 'isbn': '978-1119362395', 'available': True, 'category': 'Security'},
    {'id': 8, 'title': 'DevOps Engineering', 'author': 'Gene Kim', 'isbn': '978-1942788003', 'available': False, 'category': 'DevOps'}
]

# Enhanced transaction and activity tracking
transaction_history = []
activity_log = []
system_stats = {
    'total_visits': 0,
    'successful_logins': 0,
    'search_queries': 0,
    'form_submissions': 0
}

def log_activity(action, user=None, details=None):
    """Enhanced activity logging"""
    activity_log.append({
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'user': user or session.get('username', 'Anonymous'),
        'details': details,
        'ip': request.remote_addr if request else 'localhost'
    })

@app.route('/')
def index():
    """Modern Library System homepage with enhanced analytics"""
    system_stats['total_visits'] += 1
    log_activity('homepage_visit')
    
    # Enhanced statistics
    available_books = len([book for book in book_catalog if book['available']])
    categories = list(set(book.get('category', 'General') for book in book_catalog))
    
    return render_template('index.html', 
                         total_books=len(book_catalog),
                         available_books=available_books,
                         total_categories=len(categories),
                         total_users=len(library_users),
                         system_stats=system_stats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Enhanced modern login system"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        remember_me = request.form.get('remember_me', False)
        
        log_activity('login_attempt', username)
        
        if not username or not password:
            flash('Username and password are required for system access.', 'error')
            return render_template('login.html')
        
        if username in library_users and library_users[username]['password'] == password:
            # Update last login with enhanced tracking
            library_users[username]['last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Enhanced session with more data
            session['username'] = username
            session['user_role'] = library_users[username]['role']
            session['user_name'] = library_users[username]['name']
            session['access_level'] = library_users[username]['access_level']
            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if remember_me:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)
            
            system_stats['successful_logins'] += 1
            log_activity('successful_login', username)
            
            flash(f'Welcome back, {library_users[username]["name"]}! Access granted to Modern Library System.', 'success')
            
            # Redirect based on access level
            if library_users[username]['access_level'] in ['full', 'high']:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            log_activity('failed_login', username)
            flash('Authentication failed. Please verify your credentials and try again.', 'error')
            import time
            time.sleep(2)  # Enhanced security delay
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Standard user dashboard"""
    if 'username' not in session:
        flash('Authentication required. Please log in to continue.', 'warning')
        return redirect(url_for('login'))
    
    username = session['username']
    user_data = library_users[username]
    
    # Enhanced dashboard analytics
    user_activity = [log for log in activity_log if log['user'] == username]
    dashboard_data = {
        'total_books': len(book_catalog),
        'available_books': len([book for book in book_catalog if book['available']]),
        'borrowed_books': len([book for book in book_catalog if not book['available']]),
        'total_members': len(library_users),
        'categories': len(set(book.get('category', 'General') for book in book_catalog)),
        'user_role': session.get('user_role', 'Member'),
        'access_level': session.get('access_level', 'standard'),
        'login_time': session.get('login_time', 'Unknown'),
        'last_login': user_data.get('last_login', 'First login'),
        'user_activity_count': len(user_activity)
    }
    
    log_activity('dashboard_access', username)
    
    return render_template('dashboard.html', 
                         username=username,
                         user_data=user_data,
                         dashboard_data=dashboard_data,
                         recent_books=book_catalog[:4])

@app.route('/admin-dashboard')
def admin_dashboard():
    """Enhanced admin dashboard for high-privilege users"""
    if 'username' not in session or session.get('access_level') not in ['full', 'high']:
        flash('Administrative access required.', 'error')
        return redirect(url_for('dashboard'))
    
    admin_data = {
        'total_activities': len(activity_log),
        'recent_activities': activity_log[-10:] if activity_log else [],
        'system_health': 'Optimal',
        'active_sessions': len([u for u in library_users if library_users[u].get('last_login')]),
        'system_stats': system_stats
    }
    
    log_activity('admin_dashboard_access')
    
    return render_template('admin_dashboard.html', 
                         admin_data=admin_data,
                         user_data=library_users[session['username']])

@app.route('/logout')
def logout():
    """Enhanced logout with activity tracking"""
    username = session.get('username', 'User')
    user_name = session.get('user_name', username)
    
    log_activity('logout', username)
    session.clear()
    
    flash(f'Session terminated successfully. Thank you for using Modern Library System, {user_name}!', 'info')
    return redirect(url_for('index'))

@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    """Enhanced book catalog with advanced filtering"""
    search_query = request.form.get('search', '').strip() if request.method == 'POST' else ''
    category_filter = request.form.get('category', '') if request.method == 'POST' else ''
    availability_filter = request.form.get('availability', '') if request.method == 'POST' else ''
    
    if request.method == 'POST':
        system_stats['search_queries'] += 1
        log_activity('catalog_search', details={'query': search_query, 'category': category_filter})
    
    filtered_books = book_catalog
    
    if search_query:
        filtered_books = [book for book in filtered_books 
                         if search_query.lower() in book['title'].lower() or 
                            search_query.lower() in book['author'].lower() or
                            search_query.lower() in book.get('category', '').lower()]
    
    if category_filter:
        filtered_books = [book for book in filtered_books 
                         if book.get('category', 'General') == category_filter]
    
    if availability_filter == 'available':
        filtered_books = [book for book in filtered_books if book['available']]
    elif availability_filter == 'borrowed':
        filtered_books = [book for book in filtered_books if not book['available']]
    
    categories = sorted(list(set(book.get('category', 'General') for book in book_catalog)))
    
    return render_template('catalog.html', 
                         books=filtered_books, 
                         search_query=search_query,
                         categories=categories,
                         selected_category=category_filter,
                         selected_availability=availability_filter)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Enhanced contact system with priority handling"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        inquiry_type = request.form.get('inquiry_type', '').strip()
        priority = request.form.get('priority', 'normal').strip()
        message = request.form.get('message', '').strip()
        
        system_stats['form_submissions'] += 1
        
        errors = []
        
        if not name or len(name) < 2:
            errors.append('Full name must be at least 2 characters.')
        
        if not email or '@' not in email or '.' not in email:
            errors.append('Please enter a valid email address.')
        
        if not inquiry_type:
            errors.append('Please select an inquiry type.')
        
        if not message or len(message) < 15:
            errors.append('Message must be at least 15 characters long.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            # Enhanced inquiry data
            inquiry_data = {
                'id': len(transaction_history) + 1,
                'name': name,
                'email': email,
                'inquiry_type': inquiry_type,
                'priority': priority,
                'message': message,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'user': session.get('username', 'Anonymous'),
                'status': 'new',
                'response_time': '12-24 hours' if priority == 'high' else '24-48 hours'
            }
            transaction_history.append(inquiry_data)
            
            log_activity('contact_form_submission', details={'inquiry_type': inquiry_type, 'priority': priority})
            
            flash(f'Thank you {name}! Your {inquiry_type.lower()} inquiry (Priority: {priority.title()}) has been received. Response expected within {inquiry_data["response_time"]}.', 'success')
            return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/about')
def about():
    """Enhanced about page with system information"""
    log_activity('about_page_visit')
    
    system_info = {
        'version': '2.0.0',
        'build_date': '2025-10-15',
        'features_count': 12,
        'supported_formats': ['PDF', 'EPUB', 'MOBI', 'HTML'],
        'security_level': 'Enterprise Grade'
    }
    
    return render_template('about.html', system_info=system_info)

@app.route('/profile')
def profile():
    """Enhanced user profile with activity tracking"""
    if 'username' not in session:
        flash('Authentication required to view profile.', 'warning')
        return redirect(url_for('login'))
    
    username = session['username']
    user_data = library_users[username]
    
    # User activity summary
    user_activities = [log for log in activity_log if log['user'] == username]
    profile_stats = {
        'total_activities': len(user_activities),
        'login_count': len([log for log in user_activities if log['action'] == 'successful_login']),
        'search_count': len([log for log in user_activities if log['action'] == 'catalog_search']),
        'last_activity': user_activities[-1]['timestamp'] if user_activities else 'No activity'
    }
    
    log_activity('profile_access', username)
    
    return render_template('profile.html', 
                         username=username, 
                         user_data=user_data,
                         profile_stats=profile_stats)

@app.route('/api/system-status')
def api_system_status():
    """Enhanced API endpoint with comprehensive system status"""
    return jsonify({
        'status': 'operational',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'system_health': 'optimal',
        'database': {
            'total_books': len(book_catalog),
            'available_books': len([book for book in book_catalog if book['available']]),
            'total_categories': len(set(book.get('category', 'General') for book in book_catalog))
        },
        'users': {
            'total_members': len(library_users),
            'active_members': len([u for u in library_users if library_users[u].get('last_login')]),
            'access_levels': list(set(user['access_level'] for user in library_users.values()))
        },
        'activity': {
            'total_visits': system_stats['total_visits'],
            'successful_logins': system_stats['successful_logins'],
            'search_queries': system_stats['search_queries'],
            'form_submissions': system_stats['form_submissions']
        }
    })

@app.route('/api/books')
def api_books():
    """API endpoint for book data"""
    return jsonify({
        'books': book_catalog,
        'total_count': len(book_catalog),
        'available_count': len([book for book in book_catalog if book['available']]),
        'categories': list(set(book.get('category', 'General') for book in book_catalog))
    })

@app.errorhandler(404)
def page_not_found(e):
    """Enhanced 404 error page"""
    log_activity('page_not_found', details={'url': request.url})
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Enhanced 500 error page"""
    log_activity('internal_error', details={'error': str(e)})
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🔮 MODERN LIBRARY MANAGEMENT SYSTEM v2.0")
    print("=" * 60)
    print("🌐 URL: http://localhost:5000")
    print("🔐 Enhanced Authentication System")
    print("👥 System User Accounts:")
    print("   • admin / admin2025 (System Administrator)")
    print("   • librarian / lib123 (Senior Librarian)")
    print("   • student / student456 (Graduate Student)")
    print("   • faculty / faculty789 (Research Faculty)")
    print("   • researcher / research2024 (Research Scholar)")
    print("📚 Enhanced Features:")
    print("   • Advanced Book Catalog with Categories")
    print("   • Multi-level Access Control")
    print("   • Real-time Activity Tracking")
    print("   • Enhanced Search & Filtering")
    print("   • Priority-based Contact System")
    print("   • Comprehensive Analytics")
    print("   • API Endpoints")
    print("   • Admin Dashboard")
    print("🎨 Modern UI/UX Design:")
    print("   • Blue-Purple Color Scheme")
    print("   • Responsive Layout")
    print("   • Enhanced User Experience")
    print("🧪 Ready for comprehensive Modern Library testing!")
    print("=" * 60)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
