// UNIBITES - Custom JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize cart functionality
    initializeCart();

    // Initialize search functionality
    initializeSearch();

    // Initialize form validation
    initializeValidation();

    // Initialize loading states
    initializeLoadingStates();
});

// Cart Management
function initializeCart() {
    // Update cart item quantities
    document.querySelectorAll('.quantity-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const action = this.dataset.action;
            const productId = this.dataset.productId;
            const quantityInput = document.querySelector(`#quantity-${productId}`);
            let currentQuantity = parseInt(quantityInput.value) || 1;

            if (action === 'increase') {
                currentQuantity++;
            } else if (action === 'decrease' && currentQuantity > 1) {
                currentQuantity--;
            }

            quantityInput.value = currentQuantity;
            updateCartItem(productId, currentQuantity);
        });
    });

    // Remove cart items
    document.querySelectorAll('.remove-item').forEach(btn => {
        btn.addEventListener('click', function () {
            const productId = this.dataset.productId;
            removeCartItem(productId);
        });
    });
}

function updateCartItem(productId, quantity) {
    showLoading();

    fetch('/api/cart/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartTotal();
            showToast('Cart updated successfully!', 'success');
        } else {
            showToast('Error updating cart: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An error occurred while updating cart', 'error');
    })
    .finally(() => {
        hideLoading();
    });
}

function removeCartItem(productId) {
    if (confirm('Are you sure you want to remove this item from cart?')) {
        showLoading();

        fetch(`/api/cart/remove/${productId}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.querySelector(`#cart-item-${productId}`).remove();
                updateCartTotal();
                updateCartCount();
                showToast('Item removed from cart', 'success');
            } else {
                showToast('Error removing item: ' + data.error, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('An error occurred while removing item', 'error');
        })
        .finally(() => {
            hideLoading();
        });
    }
}

function updateCartTotal() {
    let total = 0;
    document.querySelectorAll('.cart-item').forEach(item => {
        const price = parseFloat(item.dataset.price);
        const quantity = parseInt(item.querySelector('.quantity-input').value);
        total += price * quantity;
    });

    document.querySelector('#cart-total').textContent = '₹' + total.toFixed(2);
}

function updateCartCount() {
    fetch('/api/cart/count')
    .then(response => response.json())
    .then(data => {
        document.querySelector('#cart-count').textContent = data.count;
    });
}

// Search Functionality
function initializeSearch() {
    const searchInput = document.querySelector('#search-input');
    const searchForm = document.querySelector('#search-form');

    if (searchInput && searchForm) {
        let searchTimeout;

        searchInput.addEventListener('input', function () {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(this.value);
            }, 300);
        });

        searchForm.addEventListener('submit', function (e) {
            e.preventDefault();
            performSearch(searchInput.value);
        });
    }
}

function performSearch(query) {
    if (query.length < 2) return;

    const searchResults = document.querySelector('#search-results');
    if (!searchResults) return;

    showLoading();

    fetch(`/api/search?q=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
        displaySearchResults(data.results);
    })
    .catch(error => {
        console.error('Search error:', error);
        showToast('Search failed', 'error');
    })
    .finally(() => {
        hideLoading();
    });
}

function displaySearchResults(results) {
    const container = document.querySelector('#search-results');
    container.innerHTML = '';

    if (results.length === 0) {
        container.innerHTML = '<p class="text-muted text-center">No results found</p>';
        return;
    }

    results.forEach(product => {
        const productCard = createProductCard(product);
        container.appendChild(productCard);
    });
}

function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'col-md-6 col-lg-4 mb-4';
    card.innerHTML = `
        <div class="card product-card h-100">
            <img src="${product.image_url || '/static/images/default-food.jpg'}" 
                 class="card-img-top" alt="${product.name}" 
                 style="height: 200px; object-fit: cover;">
            <div class="card-body">
                <h5 class="card-title">${product.name}</h5>
                <p class="card-text text-muted">${product.description}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <span class="h5 text-primary">₹${product.price}</span>
                    <button class="btn btn-primary btn-sm add-to-cart-btn" 
                            data-product-id="${product.id}">
                        <i class="fas fa-plus"></i> Add
                    </button>
                </div>
            </div>
        </div>
    `;

    // Add event listener for add to cart button
    card.querySelector('.add-to-cart-btn').addEventListener('click', function () {
        addToCart(product.id, 1);
    });

    return card;
}

// Form Validation
function initializeValidation() {
    const forms = document.querySelectorAll('.needs-validation');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Loading States
function initializeLoadingStates() {
    // Add loading state to all buttons with data-loading attribute
    document.querySelectorAll('[data-loading]').forEach(btn => {
        btn.addEventListener('click', function () {
            this.disabled = true;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        });
    });
}

function showLoading() {
    const loader = document.querySelector('#page-loader');
    if (loader) {
        loader.style.display = 'block';
    }
}

function hideLoading() {
    const loader = document.querySelector('#page-loader');
    if (loader) {
        loader.style.display = 'none';
    }
}

// Toast Notifications
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();

    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${getToastIcon(type)} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                    data-bs-dismiss="toast"></button>
        </div>
    `;

    toastContainer.appendChild(toast);

    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 5000
    });

    bsToast.show();

    toast.addEventListener('hidden.bs.toast', function () {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

function getToastIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Utility Functions
function getCSRFToken() {
    return document.querySelector('meta[name=csrf-token]')?.getAttribute('content') || '';
}

function addToCart(productId, quantity = 1) {
    showLoading();

    fetch(`/api/cart/add`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartCount();
            showToast('Item added to cart!', 'success');
        } else {
            showToast('Error adding item to cart: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An error occurred while adding item to cart', 'error');
    })
    .finally(() => {
        hideLoading();
    });
}

// Order Management
function updateOrderStatus(orderId, status) {
    showLoading();

    fetch(`/api/orders/${orderId}/status`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            status: status
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload(); // Refresh page to show updated status
        } else {
            showToast('Error updating order status: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An error occurred while updating order status', 'error');
    })
    .finally(() => {
        hideLoading();
    });
}

// Animation helpers
function fadeInElements() {
    const elements = document.querySelectorAll('.fade-in-up');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });

    elements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });
}

// Initialize animations
document.addEventListener('DOMContentLoaded', fadeInElements);
