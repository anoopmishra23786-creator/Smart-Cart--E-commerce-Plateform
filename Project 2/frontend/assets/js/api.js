/**
 * SmartCart Centralized Frontend API Client
 * Seamlessly manages authentication tokens, backend API requests, and responsive error handling.
 */
const API_BASE_URL = window.location.origin.includes('8000') 
  ? '/api' 
  : 'http://127.0.0.1:8000/api';

const api = {
  getToken() {
    return localStorage.getItem('smartcart_token') || '';
  },

  setToken(token) {
    if (token) {
      localStorage.setItem('smartcart_token', token);
    } else {
      localStorage.removeItem('smartcart_token');
    }
  },

  getCurrentUser() {
    try {
      const u = localStorage.getItem('smartcart_user');
      return u ? JSON.parse(u) : null;
    } catch (e) {
      return null;
    }
  },

  setCurrentUser(user) {
    if (user) {
      localStorage.setItem('smartcart_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('smartcart_user');
    }
  },

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, { ...options, headers });
      
      // Auto-handle 401 Unauthorized
      if (response.status === 401 && !url.includes('/auth/login')) {
        this.setToken(null);
        this.setCurrentUser(null);
        if (window.location.pathname.includes('/account.html') || 
            window.location.pathname.includes('/checkout.html') ||
            window.location.pathname.includes('/admin/')) {
          window.location.href = '/login.html?redirect=' + encodeURIComponent(window.location.pathname);
          return null;
        }
      }

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        const errorMsg = data.detail || (data.message || `Request failed with status ${response.status}`);
        throw new Error(errorMsg);
      }

      return data;
    } catch (err) {
      console.error(`API Error on ${endpoint}:`, err);
      throw err;
    }
  },

  // Products & Categories
  async getProducts(params = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, val]) => {
      if (val !== undefined && val !== null && val !== '') {
        query.append(key, val);
      }
    });
    return this.request(`/products?${query.toString()}`);
  },

  async getProduct(idOrSlug) {
    return this.request(`/products/${idOrSlug}`);
  },

  async getCategories() {
    return this.request('/categories');
  },

  // Cart
  async getCart() {
    return this.request('/cart');
  },

  async addToCart(productId, quantity = 1) {
    return this.request('/cart/items', {
      method: 'POST',
      body: JSON.stringify({ product_id: productId, quantity })
    });
  },

  async updateCartItem(itemId, quantity) {
    return this.request(`/cart/items/${itemId}`, {
      method: 'PATCH',
      body: JSON.stringify({ quantity })
    });
  },

  async removeFromCart(itemId) {
    return this.request(`/cart/items/${itemId}`, {
      method: 'DELETE'
    });
  },

  // Wishlist
  async getWishlist() {
    return this.request('/wishlist');
  },

  async addToWishlist(productId) {
    return this.request('/wishlist/items', {
      method: 'POST',
      body: JSON.stringify({ product_id: productId })
    });
  },

  async removeFromWishlist(itemId) {
    return this.request(`/wishlist/items/${itemId}`, {
      method: 'DELETE'
    });
  },

  // Orders
  async createOrder(address, paymentMethod = 'cod') {
    return this.request('/orders', {
      method: 'POST',
      body: JSON.stringify({ address, payment_method: paymentMethod })
    });
  },

  async getOrders() {
    return this.request('/orders');
  },

  async getOrder(orderId) {
    return this.request(`/orders/${orderId}`);
  },

  // Reviews
  async getProductReviews(productId) {
    return this.request(`/products/${productId}/reviews`);
  },

  async submitReview(productId, rating, reviewText) {
    return this.request(`/products/${productId}/reviews`, {
      method: 'POST',
      body: JSON.stringify({ rating, review_text: reviewText })
    });
  },

  // Admin
  async getAdminDashboard() {
    return this.request('/admin/dashboard');
  },

  async getAdminOrders() {
    return this.request('/admin/orders');
  },

  async updateOrderStatus(orderId, orderStatus, paymentStatus) {
    return this.request(`/admin/orders/${orderId}`, {
      method: 'PATCH',
      body: JSON.stringify({ order_status: orderStatus, payment_status: paymentStatus })
    });
  },

  async createAdminProduct(productData) {
    return this.request('/admin/products', {
      method: 'POST',
      body: JSON.stringify(productData)
    });
  },

  async updateAdminProduct(productId, productData) {
    return this.request(`/admin/products/${productId}`, {
      method: 'PATCH',
      body: JSON.stringify(productData)
    });
  },

  async deleteAdminProduct(productId) {
    return this.request(`/admin/products/${productId}`, {
      method: 'DELETE'
    });
  }
};
