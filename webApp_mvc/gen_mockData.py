import random
import faker
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime, date  # Import date explicitly

# Initialize Faker to generate fake data
fake = faker.Faker()

def convert_to_datetime(date_obj):
    if isinstance(date_obj, date):  # Check if it's a datetime.date object (now imported correctly)
        return datetime.combine(date_obj, datetime.min.time())  # Convert to datetime.datetime
    return date_obj

# Helper function to generate mock users
def generate_user():
    Users = {
        "username": fake.user_name(),
        "name_surname": fake.name(),
        "password": fake.password(),
        "profile_pic": "https://www.example.com/default-avatar.png",  # You might replace this with a simpler URL or remove it
        "gender": random.choice(["ชาย", "หญิง", "ไม่ระบุ"]),
        "age": random.randint(18, 60),
        "contact": {
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address()
        },
        "description": fake.text(),
        "red_flags": [fake.word() for _ in range(random.randint(1, 5))],
        "green_flags": [fake.word() for _ in range(random.randint(1, 5))],
        "class_list": [fake.word() for _ in range(random.randint(1, 5))],
        "created_posts": [],
        "joined_posts": []
    }
    return Users

# Helper function to generate mock posts
def generate_post(user):
    # Convert dates to datetime.datetime objects
    date_start = datetime.combine(fake.date_this_year(), datetime.min.time())
    date_end = datetime.combine(fake.date_this_year(), datetime.min.time())
    date_close = datetime.combine(fake.date_this_year(), datetime.min.time())

    Posts = {
        "_id": ObjectId(),  # Let MongoDB handle the post_id automatically
        "title": fake.sentence(),
        "date_start": date_start,
        "date_end": date_end,
        "date_close": date_close,
        "author": user["username"],
        "category": random.choice(["Technology", "Business", "Health", "Education"]),
        "status": random.choice(["Open", "Closed", "In Progress"]),
        "attendant": random.randint(1, 100),
        "costs": random.randint(100, 10000),
        "comments": []
    }
    return Posts

# Helper function to generate mock comments
def generate_comment(user, post_id):
    comment = {
        "_id": ObjectId(),  # Let MongoDB handle the comment_id automatically
        "author": user["username"],
        "data": fake.text(),
        "date": convert_to_datetime(fake.date_this_year()),  # Convert to datetime
        "class_comments": [fake.word() for _ in range(random.randint(1, 5))]
    }
    return comment

# Generate mock data
users = [generate_user() for _ in range(30)]
posts = []
comments = []

# Generating posts and comments
for user in users:
    # Randomly generate 1 to 3 posts for each user
    post_count = random.randint(1, 3)
    for _ in range(post_count):
        post = generate_post(user)
        posts.append(post)
        
        # Randomly generate comments for each post (0-20 comments)
        num_comments = random.randint(0, 20)
        for _ in range(num_comments):
            comment = generate_comment(user, post["_id"])  # Use _id here
            comments.append(comment)
            post["comments"].append(comment["_id"])  # Reference by _id
        
        # Update user's created posts
        user["created_posts"].append(post["_id"])

# Randomly add posts to user's joined_posts
for user in users:
    user["joined_posts"] = random.sample([post["_id"] for post in posts], random.randint(0, 5))

# MongoDB Atlas connection string
connection_string = "mongodb+srv://Parada:nN1hsdpkjc@webappcluster.et68e.mongodb.net/?retryWrites=true&w=majority&appName=webappCluster"

# Create a MongoDB client
client = MongoClient(connection_string)

# Select the database and collections
db = client["webApp2"]
print(db.list_collection_names())  # Print the collection names
users_collection = db["Users"]
posts_collection = db["Posts"]
comments_collection = db["Comments"]

# Insert mock data into MongoDB collections
try:
    user_insert_result = users_collection.insert_many(users)
    post_insert_result = posts_collection.insert_many(posts)
    comment_insert_result = comments_collection.insert_many(comments)
    
    print(f"Inserted {len(user_insert_result.inserted_ids)} users")
    print(f"Inserted {len(post_insert_result.inserted_ids)} posts")
    print(f"Inserted {len(comment_insert_result.inserted_ids)} comments")
except Exception as e:
    print(f"Error occurred during insert: {e}")
# tm