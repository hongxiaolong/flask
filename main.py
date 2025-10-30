from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///petstore.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 宠物商品模型
class PetProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    stock = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'image_url': self.image_url,
            'stock': self.stock
        }

# 购物车项目模型
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    session_id = db.Column(db.String(100), nullable=False)  # 使用session ID来标识用户

# 创建数据库表
@app.before_first_request
def create_tables():
    db.create_all()
    
    # 添加一些默认的宠物商品
    if PetProduct.query.count() == 0:
        sample_products = [
            PetProduct(
                name="宠物狗粮",
                description="高品质天然狗粮，营养均衡，适合各种体型犬只",
                price=89.99,
                category="食品",
                image_url="/static/images/dog-food.jpg",
                stock=50
            ),
            PetProduct(
                name="猫砂",
                description="结团性好，除臭效果佳的豆腐猫砂",
                price=24.99,
                category="用品",
                image_url="/static/images/cat-litter.jpg",
                stock=100
            ),
            PetProduct(
                name="宠物玩具球",
                description="耐咬橡胶球，适合狗狗玩耍，促进运动",
                price=12.99,
                category="玩具",
                image_url="/static/images/pet-toy-ball.jpg",
                stock=75
            ),
            PetProduct(
                name="猫抓板",
                description="环保瓦楞纸材质，保护家具，满足猫咪磨爪天性",
                price=19.99,
                category="用品",
                image_url="/static/images/cat-scratcher.jpg",
                stock=40
            ),
            PetProduct(
                name="宠物梳子",
                description="专业宠物美容梳，去毛结，按摩皮肤",
                price=15.99,
                category="美容",
                image_url="/static/images/pet-brush.jpg",
                stock=60
            ),
            PetProduct(
                name="宠物牵引绳",
                description="舒适胸背带设计，安全可靠的遛狗装备",
                price=29.99,
                category="用品",
                image_url="/static/images/pet-harness.jpg",
                stock=30
            )
        ]
        
        for product in sample_products:
            db.session.add(product)
        db.session.commit()

# 路由定义
@app.route('/')
def index():
    products = PetProduct.query.all()
    categories = db.session.query(PetProduct.category).distinct().all()
    categories = [cat[0] for cat in categories]
    return render_template('index.html', products=products, categories=categories)

@app.route('/category/<category>')
def category(category):
    products = PetProduct.query.filter_by(category=category).all()
    categories = db.session.query(PetProduct.category).distinct().all()
    categories = [cat[0] for cat in categories]
    return render_template('index.html', products=products, categories=categories, selected_category=category)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = PetProduct.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/api/products')
def api_products():
    products = PetProduct.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/api/products/<int:product_id>')
def api_product_detail(product_id):
    product = PetProduct.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@app.route('/api/cart', methods=['GET'])
def api_cart():
    # 在实际应用中，应该使用session或用户认证来标识用户
    # 这里简化处理，返回空购物车
    return jsonify([])

@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    # 在实际应用中，应该使用session或用户认证来标识用户
    # 这里简化处理，创建购物车项目
    cart_item = CartItem(
        product_id=product_id,
        quantity=quantity,
        session_id='default_session'  # 简化处理
    )
    db.session.add(cart_item)
    db.session.commit()
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
