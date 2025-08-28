import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
random.seed(42)

# Output directory for CSVs (update if needed)
output_dir = "C:/Users/S_CSIS-PostGrad/Desktop/graph-data/neo4j_imports"
os.makedirs(output_dir, exist_ok=True)

# 1. Generate Users (50 users with realistic names)
names = [
    "Beyoncé Knowles", "Elon Musk", "Burna Boy", "Taylor Swift", "Serena Williams", 
    "Chimamanda Adichie", "Drake", "Greta Thunberg", "Trevor Noah", "Adele", 
    "Sundar Pichai", "Rihanna", "Kanye West", "Naledi Pandor", "Davido", 
    "Oprah Winfrey", "Bill Gates", "Tems", "Cristiano Ronaldo", "Lupita Nyong'o", 
    "Jeff Bezos", "Wizkid", "Angelique Kidjo", "Malala Yousafzai", "Kendrick Lamar",
    "Jack Ma", "Tiwa Savage", "Usain Bolt", "Shonda Rhimes", "Mark Zuckerberg",
    "Ayra Starr", "Lionel Messi", "Mindy Kaling", "Snoop Dogg", "Ngozi Okonjo-Iweala",
    "Chris Hemsworth", "Femi Otedola", "Cardi B", "Tim Cook", "Remge", 
    "Denzel Washington", "Alicia Keys", "Pharrell Williams", "Safarina Nkoana", 
    "Jay-Z", "Ellen DeGeneres", "Yemi Alade", "Ryan Reynolds", "Akon", 
    "Zozibini Tunzi", "Post Malone", "Lizzo", "Satya Nadella", "Davido", 
    "Kehinde Wiley", "Lady Gaga", "Stormzy", "Charlize Theron", "Asake"
]  # Diverse names (celebrities, innovators, musicians)
users = []
for i in range(50):
    users.append({
        "userId": f"u{i+1}",
        "name": random.choice(names),  # Every user gets a name
        "joinedAt": (datetime(2025, 1, 1) + timedelta(days=random.randint(0, 200))).strftime("%Y-%m-%d")
    })
users_df = pd.DataFrame(users)
users_df.to_csv(os.path.join(output_dir, "users.csv"), index=False)

# 2. Generate Hashtags (30 realistic hashtags based on 2025 trends)
hashtags = [
    "AI", "ClimateAction", "Afrobeats", "TechTrends", "Sustainability", 
    "Metaverse", "Crypto", "Springboks", "DataScience", "Innovation",
    "MentalHealth", "Gaming", "FashionWeek", "RenewableEnergy", "Blockchain",
    "AfricanTech", "MusicFest", "DigitalNomad", "Cybersecurity", "HealthTech",
    "Pride2025", "GenZFashion", "VirtualReality", "EcoFriendly", "StartupLife",
    "BigData", "WomenInTech", "GlobalGoals", "AugmentedReality", "SocialImpact"
]  # Trending topics for 2025[](https://www.buzz-music.com/post/the-perfect-hashtags-for-indie-musicians-in-2025)[](https://growthoid.com/trending-hashtags/)[](https://podcastle.ai/blog/trending-tiktok-hashtags/)
hashtags_df = pd.DataFrame({"tag": hashtags})
hashtags_df.to_csv(os.path.join(output_dir, "hashtags.csv"), index=False)

# 3. Generate Posts (200 posts with natural text)
posts = []
for i in range(200):
    user_id = f"u{random.randint(1, 50)}"
    hashtag = random.choice(hashtags)
    mention = f"@{random.choice(names).split()[0]}" if random.random() < 0.3 else ""  # 30% chance of mention
    text = f"{random.choice(['Loving', 'Excited about', 'Just saw', 'Can’t wait for', 'Big news!'])} {mention} #{hashtag}".strip()
    posts.append({
        "postId": f"p{i+1}",
        "userId": user_id,
        "text": text,
        "createdAt": (datetime(2025, 3, 1) + timedelta(days=random.randint(0, 150), hours=random.randint(0, 23))).strftime("%Y-%m-%dT%H:%M:%S"),
        "likesCount": 0  # Will update after LIKED relationships
    })
posts_df = pd.DataFrame(posts)
posts_df.to_csv(os.path.join(output_dir, "posts.csv"), index=False)

# 4. Generate FOLLOWS (150 relationships)
follows = []
used_pairs = set()
while len(follows) < 150:
    u1, u2 = f"u{random.randint(1, 50)}", f"u{random.randint(1, 50)}"
    if u1 != u2 and (u1, u2) not in used_pairs:
        follows.append({
            "userId1": u1,
            "userId2": u2,
            "since": (datetime(2025, 2, 1) + timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d")
        })
        used_pairs.add((u1, u2))
follows_df = pd.DataFrame(follows)
follows_df.to_csv(os.path.join(output_dir, "follows.csv"), index=False)

# 5. Generate LIKED (400 relationships)
likes = []
used_likes = set()
while len(likes) < 400:
    user_id, post_id = f"u{random.randint(1, 50)}", f"p{random.randint(1, 200)}"
    if (user_id, post_id) not in used_likes:
        likes.append({
            "userId": user_id,
            "postId": post_id,
            "timestamp": (datetime(2025, 3, 1) + timedelta(days=random.randint(0, 150), hours=random.randint(0, 23))).strftime("%Y-%m-%dT%H:%M:%S")
        })
        used_likes.add((user_id, post_id))
likes_df = pd.DataFrame(likes)
likes_df.to_csv(os.path.join(output_dir, "likes.csv"), index=False)

# 6. Generate TAGGED_WITH (250 relationships)
tagged_with = []
for i in range(200):
    post_id = f"p{i+1}"
    num_tags = random.randint(1, 3)  # 1-3 hashtags per post
    selected_tags = random.sample(hashtags, min(num_tags, len(hashtags)))
    for tag in selected_tags:
        tagged_with.append({"postId": post_id, "tag": tag})
while len(tagged_with) < 250:  # Add more to reach ~250
    tagged_with.append({"postId": f"p{random.randint(1, 200)}", "tag": random.choice(hashtags)})
tagged_with_df = pd.DataFrame(tagged_with)
tagged_with_df.to_csv(os.path.join(output_dir, "tagged_with.csv"), index=False)

# 7. Generate MENTIONS (100 relationships)
mentions = []
for i in range(200):
    post_id = f"p{i+1}"
    if random.random() < 0.5:  # 50% chance of a mention
        mentions.append({"postId": post_id, "userId": f"u{random.randint(1, 50)}"})
mentions = mentions[:100]  # Limit to 100
mentions_df = pd.DataFrame(mentions)
mentions_df.to_csv(os.path.join(output_dir, "mentions.csv"), index=False)

print(f"CSVs generated in {output_dir}")