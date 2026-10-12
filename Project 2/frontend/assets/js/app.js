/**
 * SmartCart Global Application Scripts
 * Manages toast notifications, navbar active states, cart badge counters, and formatters.
 */

// Toast notification helper
function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `sc-toast ${type}`;
  toast.innerHTML = `
    <i class="bi ${type === 'success' ? 'bi-check-circle-fill text-success' : 'bi-exclamation-triangle-fill text-danger'}"></i>
    <span>${message}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Currency Formatter for Indian Rupee
function formatINR(amount) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 2
  }).format(amount || 0);
}

// Update Navbar Authentication State and Cart Count
async function updateNavState() {
  const user = api.getCurrentUser();
  const token = api.getToken();

  const authSection = document.getElementById('nav-auth-section');
  const cartBadge = document.getElementById('nav-cart-badge');
  const wishlistBadge = document.getElementById('nav-wishlist-badge');

  if (authSection) {
    if (token && user) {
      authSection.innerHTML = `
        <div class="dropdown">
          <button class="btn btn-sm btn-outline-secondary dropdown-toggle d-flex align-items-center gap-1" type="button" data-bs-toggle="dropdown">
            <i class="bi bi-person-circle"></i>
            <span>${user.full_name || 'My Account'}</span>
          </button>
          <ul class="dropdown-menu dropdown-menu-end shadow-sm">
            <li><a class="dropdown-item" href="/account.html"><i class="bi bi-person me-2"></i>Profile</a></li>
            <li><a class="dropdown-item" href="/orders.html"><i class="bi bi-box-seam me-2"></i>My Orders</a></li>
            <li><a class="dropdown-item" href="/wishlist.html"><i class="bi bi-heart me-2"></i>Wishlist</a></li>
            ${user.is_admin ? '<li><hr class="dropdown-divider"></li><li><a class="dropdown-item text-primary fw-semibold" href="/admin/index.html"><i class="bi bi-speedometer2 me-2"></i>Admin Dashboard</a></li>' : ''}
            <li><hr class="dropdown-divider"></li>
            <li><button class="dropdown-item text-danger" id="nav-logout-btn"><i class="bi bi-box-arrow-right me-2"></i>Logout</button></li>
          </ul>
        </div>
      `;

      const logoutBtn = document.getElementById('nav-logout-btn');
      if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
          api.setToken(null);
          api.setCurrentUser(null);
          showToast('Logged out successfully');
          setTimeout(() => window.location.href = '/index.html', 500);
        });
      }
    } else {
      authSection.innerHTML = `
        <a href="/login.html" class="btn btn-sm btn-outline-primary">Sign In</a>
        <a href="/register.html" class="btn btn-sm btn-primary">Sign Up</a>
      `;
    }
  }

  // Update Cart badge if token present
  if (token && cartBadge) {
    try {
      const cart = await api.getCart();
      if (cart && cart.items) {
        const totalItems = cart.items.reduce((acc, item) => acc + item.quantity, 0);
        cartBadge.textContent = totalItems;
        cartBadge.classList.toggle('d-none', totalItems === 0);
      }
    } catch (e) {
      // Ignored
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  updateNavState();
});
