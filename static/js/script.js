// 宠物电商网站 JavaScript 功能

// 购物车功能
class PetStoreCart {
    constructor() {
        this.items = [];
        this.loadCart();
    }
    
    // 添加商品到购物车
    addToCart(productId, quantity = 1) {
        // 检查商品是否已存在于购物车中
        const existingItem = this.items.find(item => item.productId === productId);
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.items.push({
                productId: productId,
                quantity: quantity
            });
        }
        
        this.saveCart();
        this.updateCartUI();
    }
    
    // 更新购物车中商品数量
    updateQuantity(productId, quantity) {
        if (quantity <= 0) {
            this.removeItem(productId);
            return;
        }
        
        const item = this.items.find(item => item.productId === productId);
        if (item) {
            item.quantity = quantity;
            this.saveCart();
            this.updateCartUI();
        }
    }
    
    // 从购物车移除商品
    removeItem(productId) {
        this.items = this.items.filter(item => item.productId !== productId);
        this.saveCart();
        this.updateCartUI();
    }
    
    // 保存购物车到本地存储
    saveCart() {
        localStorage.setItem('petStoreCart', JSON.stringify(this.items));
    }
    
    // 从本地存储加载购物车
    loadCart() {
        const cartData = localStorage.getItem('petStoreCart');
        if (cartData) {
            this.items = JSON.parse(cartData);
        } else {
            this.items = [];
        }
    }
    
    // 更新购物车UI
    updateCartUI() {
        // 更新购物车图标上的数量显示
        const cartCount = this.items.reduce((total, item) => total + item.quantity, 0);
        const cartBadge = document.querySelector('.cart-count');
        if (cartBadge) {
            cartBadge.textContent = cartCount;
        }
    }
    
    // 获取购物车商品总数
    getTotalItems() {
        return this.items.reduce((total, item) => total + item.quantity, 0);
    }
    
    // 清空购物车
    clearCart() {
        this.items = [];
        this.saveCart();
        this.updateCartUI();
    }
}

// 初始化购物车
const petStoreCart = new PetStoreCart();

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 为所有"加入购物车"按钮添加事件监听器
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const quantity = parseInt(this.getAttribute('data-quantity')) || 1;
            
            petStoreCart.addToCart(productId, quantity);
            
            // 显示添加成功的提示
            showAlert('商品已成功加入购物车！', 'success');
        });
    });
    
    // 为数量输入框添加实时更新功能
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const productId = this.getAttribute('data-product-id');
            const quantity = parseInt(this.value);
            
            if (!isNaN(quantity) && quantity > 0) {
                petStoreCart.updateQuantity(productId, quantity);
            } else {
                this.value = 1; // 重置为最小值
            }
        });
    });
    
    // 更新购物车UI
    petStoreCart.updateCartUI();
});

// 显示提示信息
function showAlert(message, type = 'info') {
    // 创建提示元素
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // 3秒后自动移除提示
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 3000);
}

// 格式化货币
function formatCurrency(amount) {
    return '¥' + parseFloat(amount).toFixed(2);
}