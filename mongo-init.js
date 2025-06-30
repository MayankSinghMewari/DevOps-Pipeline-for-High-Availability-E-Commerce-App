// MongoDB initialization script
// This script will run when the MongoDB container starts

db = db.getSiblingDB('ecommerce_db');

// Create collections
db.createCollection('users');
db.createCollection('products');
db.createCollection('orders');

// Insert sample products
db.products.insertMany([
    {
        name: "MacBook Pro 14-inch",
        price: 199900,
        description: "Apple MacBook Pro with M2 Pro chip, 16GB RAM, 512GB SSD. Perfect for professionals and creatives.",
        image: "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=300&fit=crop",
        category: "Electronics",
        stock: 15,
        featured: true
    },
    {
        name: "iPhone 15 Pro",
        price: 134900,
        description: "Latest iPhone with A17 Pro chip, 128GB storage, and advanced camera system.",
        image: "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=300&fit=crop",
        category: "Electronics",
        stock: 25,
        featured: true
    },
    {
        name: "Sony WH-1000XM5",
        price: 29990,
        description: "Industry-leading noise canceling wireless headphones with 30-hour battery life.",
        image: "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400&h=300&fit=crop",
        category: "Electronics",
        stock: 30,
        featured: false
    },
    {
        name: "Dell XPS 13",
        price: 89990,
        description: "Ultra-thin laptop with Intel Core i7, 16GB RAM, and stunning InfinityEdge display.",
        image: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop",
        category: "Electronics",
        stock: 12,
        featured: false
    },
    {
        name: "Samsung Galaxy Tab S9",
        price: 72999,
        description: "Premium Android tablet with S Pen, perfect for productivity and entertainment.",
        image: "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=300&fit=crop",
        category: "Electronics",
        stock: 20,
        featured: true
    },
    {
        name: "Canon EOS R6 Mark II",
        price: 239999,
        description: "Professional mirrorless camera with 24.2MP sensor and 4K video recording.",
        image: "https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=400&h=300&fit=crop",
        category: "Electronics",
        stock: 8,
        featured: false
    },
    {
        name: "Gaming Chair Pro",
        price: 24999,
        description: "Ergonomic gaming chair with lumbar support, adjustable armrests, and premium materials.",
        image: "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop",
        category: "Furniture",
        stock: 18,
        featured: false
    },
    {
        name: "Mechanical Keyboard RGB",
        price: 8999,
        description: "Premium mechanical keyboard with RGB backlighting and tactile switches.",
        image: "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=300&fit=crop",
        category: "Electronics",
        stock: 35,
        featured: false
    },
    {
        name: "4K Webcam",
        price: 12999,
        description: "Ultra HD webcam with auto-focus and noise-canceling microphone for streaming.",
        image: "https://images.unsplash.com/photo-1587614382346-4ec70e388b28?w=400&h=300&fit=crop",
        category: "Electronics",
        stock: 22,
        featured: false
    }
]);

// Create indexes for better performance
db.products.createIndex({ "name": "text", "description": "text" });
db.products.createIndex({ "category": 1 });
db.products.createIndex({ "featured": 1 });
db.users.createIndex({ "email": 1 }, { unique: true });
db.orders.createIndex({ "user_id": 1 });

print("Database initialized with sample data!");
print("Products inserted:", db.products.countDocuments());
print("Collections created:", db.getCollectionNames());