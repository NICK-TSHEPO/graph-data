import pandas as pd
import random
import re
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
random.seed(42)

# Output directory for CSVs
output_dir = "C:/Users/S_CSIS-PostGrad/Desktop/graph-data/neo4j_imports"
os.makedirs(output_dir, exist_ok=True)

# 1. Generate Users (50 unique users)
names = list(set([
    "Beyoncé Knowles", "Elon Musk", "Burna Boy", "Taylor Swift", "Serena Williams", 
    "Chimamanda Adichie", "Drake", "Greta Thunberg", "Trevor Noah", "Adele", 
    "Sundar Pichai", "Rihanna", "Kanye West", "Naledi Pandor", "Davido", 
    "Oprah Winfrey", "Bill Gates", "Tems", "Cristiano Ronaldo", "Lupita Nyong'o", 
    "Jeff Bezos", "Wizkid", "Angelique Kidjo", "Malala Yousafzai", "Kendrick Lamar",
    "Jack Ma", "Tiwa Savage", "Usain Bolt", "Shonda Rhimes", "Mark Zuckerberg",
    "Ayra Starr", "Lionel Messi", "Mindy Kaling", "Snoop Dogg", "Ngozi Okonjo-Iweala",
    "Chris Hemsworth", "Femi Otedola", "Cardi B", "Tim Cook", "Rema", 
    "Denzel Washington", "Alicia Keys", "Pharrell Williams", "Safarina Nkoana", 
    "Jay-Z", "Ellen DeGeneres", "Yemi Alade", "Ryan Reynolds", "Akon", 
    "Zozibini Tunzi", "Post Malone", "Lizzo", "Satya Nadella", "Kehinde Wiley"
]))
random.shuffle(names)
names = names[:50]
users = []
for i, name in enumerate(names):
    users.append({
        "userId": f"u{i+1}",
        "name": name,
        "displayName": name,  # Added for visualization
        "joinedAt": (datetime(2025, 1, 1) + timedelta(days=random.randint(0, 200))).strftime("%Y-%m-%d")
    })
users_df = pd.DataFrame(users)
users_df.to_csv(os.path.join(output_dir, "users.csv"), index=False)

# 2. Generate Hashtags (30 realistic 2025 trending hashtags)
hashtags = [
    "love", "instagood", "fashion", "photography", "viral", "reels", "explore", "fyp", "travel", "music",
    "AI", "ClimateAction", "Afrobeats", "TechTrends", "Sustainability", 
    "Metaverse", "Crypto", "Springboks", "DataScience", "Innovation",
    "MentalHealth", "Gaming", "FashionWeek", "RenewableEnergy", "Blockchain",
    "AfricanTech", "MusicFest", "DigitalNomad", "Cybersecurity", "HealthTech"
]
hashtags_df = pd.DataFrame({"tag": [tag.lower() for tag in hashtags], "displayTag": [tag.lower() for tag in hashtags]})
hashtags_df.to_csv(os.path.join(output_dir, "hashtags.csv"), index=False)

# 3. Generate Posts (200 posts with natural text)
post_templates = [
    "Just discovered something amazing! {mention} {hashtag} 🔥",
    "What do you think about this? {mention} Check out {url} {hashtag}",
    "Loving the vibes today! {hashtag} 😍",
    "Big news everyone! {mention} {hashtag} 🎉",
    "Excited for the future of {hashtag}! {mention} 🚀",
    "Can't stop thinking about {hashtag}. Share your thoughts! {url} 👇",
    "Incredible performance by {mention}! #Afrobeats 🎤",
    "Why is {hashtag} trending? {mention} {url}"
]
posts = []
post_texts = {}
popular_posts = random.sample(range(1, 201), 10)  # For viral posts
post_weights = [10 if i in popular_posts else 1 for i in range(1, 201)]
for i in range(200):
    user_id = f"u{random.randint(1, 50)}"
    user_name = next(u['name'] for u in users if u['userId'] == user_id)
    created_at = datetime(2025, 3, 1) + timedelta(days=random.randint(0, 150), hours=random.randint(0, 23))
    num_mentions = random.randint(0, 2)
    try:
        mentions = " ".join([f"@{random.choice([n for n in names if n != user_name]).split()[0]}" for _ in range(num_mentions)])
    except IndexError:
        mentions = ""
    num_tags = random.randint(1, 3)
    tags = " ".join([f"#{random.choice(hashtags)}" for _ in range(num_tags)])
    has_url = random.random() < 0.2
    url = f"https://news.example.com/article{random.randint(1, 100)}" if has_url else ""
    has_media = random.random() < 0.3
    media_indicator = random.choice([" [image]", " [video]"]) if has_media else ""
    template = random.choice(post_templates).format(mention=mentions, hashtag=tags, url=url)
    text = f"{template}{media_indicator}".strip()
    display_text = (text[:20] + "...") if len(text) > 20 else text  # Truncated for visualization
    post_id = f"p{i+1}"
    post_texts[post_id] = text
    posts.append({
        "postId": post_id,
        "userId": user_id,
        "text": text,
        "displayText": display_text,  # Added for visualization
        "createdAt": created_at.strftime("%Y-%m-%dT%H:%M:%S"),
        "likesCount": 0
    })
posts_df = pd.DataFrame(posts)
posts_df.to_csv(os.path.join(output_dir, "posts.csv"), index=False)

# 4. Generate Media (100 media nodes: 70 images, 30 videos)
media = []
for i in range(100):
    media_type = "image" if i < 70 else "video"
    url = f"https://picsum.photos/seed/m{i+1}/400/300" if media_type == "image" else f"https://youtube.com/watch?v=v{i+1}"
    media.append({
        "mediaId": f"m{i+1}",
        "type": media_type,
        "url": url,
        "displayUrl": media_type  # Added for visualization (e.g., "image" or "video")
    })
media_df = pd.DataFrame(media)
media_df.to_csv(os.path.join(output_dir, "media.csv"), index=False)

# 5. Generate URLs (50 URL nodes)
urls = []
for i in range(50):
    url = f"https://www.example-news.com/article/{i+1}?topic={random.choice(hashtags)}"
    urls.append({
        "urlId": f"l{i+1}",
        "url": url,
        "displayUrl": f"article/{i+1}"  # Added for visualization
    })
urls_df = pd.DataFrame(urls)
urls_df.to_csv(os.path.join(output_dir, "urls.csv"), index=False)

# 6. Generate Comments (300 comments: 240 on posts, 60 on comments)
comment_templates = [
    "Totally agree! {mention} {hashtag} 🙌",
    "This is hilarious! {url} {hashtag} 😂",
    "Not sure about that... {mention} 🤔",
    "Love this! {hashtag} [image] 😍",
    "Great point! Check my take: {url} 👀",
    "Replying to {mention}: Yes! {hashtag} 💪"
]
comments = []
comment_texts = {}
comment_parents = []
post_created_times = {p['postId']: datetime.strptime(p['createdAt'], "%Y-%m-%dT%H:%M:%S") for p in posts}
comment_created_times = {}
for i in range(240):  # First pass: comments on posts
    parent_post_id = f"p{random.choices(range(1, 201), weights=post_weights)[0]}"
    parent_time = post_created_times[parent_post_id]
    created_at = parent_time + timedelta(minutes=random.randint(1, 1440))
    user_id = f"u{random.randint(1, 50)}"
    user_name = next(u['name'] for u in users if u['userId'] == user_id)
    num_mentions = random.randint(0, 1)
    try:
        mentions = " ".join([f"@{random.choice([n for n in names if n != user_name]).split()[0]}" for _ in range(num_mentions)])
    except IndexError:
        mentions = ""
    num_tags = random.randint(0, 2)
    tags = " ".join([f"#{random.choice(hashtags)}" for _ in range(num_tags)])
    has_url = random.random() < 0.1
    url = f"https://blog.example.com/reply{random.randint(1, 100)}" if has_url else ""
    has_media = random.random() < 0.15
    media_indicator = random.choice([" [image]", " [video]"]) if has_media else ""
    template = random.choice(comment_templates).format(mention=mentions, hashtag=tags, url=url)
    text = f"{template}{media_indicator}".strip()
    display_text = (text[:20] + "...") if len(text) > 20 else text  # Truncated for visualization
    comment_id = f"c{i+1}"
    comment_texts[comment_id] = text
    comments.append({
        "commentId": comment_id,
        "userId": user_id,
        "text": text,
        "displayText": display_text,  # Added for visualization
        "createdAt": created_at.strftime("%Y-%m-%dT%H:%M:%S"),
        "likesCount": 0
    })
    comment_parents.append({"commentId": comment_id, "parentId": parent_post_id, "parentType": "Post"})
    comment_created_times[comment_id] = created_at

# Second pass: comments on comments
for i in range(240, 300):
    parent_comment_id = f"c{random.randint(1, i)}"
    parent_time = comment_created_times[parent_comment_id]
    created_at = parent_time + timedelta(minutes=random.randint(1, 1440))
    user_id = f"u{random.randint(1, 50)}"
    user_name = next(u['name'] for u in users if u['userId'] == user_id)
    num_mentions = random.randint(0, 1)
    try:
        mentions = " ".join([f"@{random.choice([n for n in names if n != user_name]).split()[0]}" for _ in range(num_mentions)])
    except IndexError:
        mentions = ""
    num_tags = random.randint(0, 2)
    tags = " ".join([f"#{random.choice(hashtags)}" for _ in range(num_tags)])
    has_url = random.random() < 0.1
    url = f"https://blog.example.com/reply{random.randint(1, 100)}" if has_url else ""
    has_media = random.random() < 0.15
    media_indicator = random.choice([" [image]", " [video]"]) if has_media else ""
    template = random.choice(comment_templates).format(mention=mentions, hashtag=tags, url=url)
    text = f"{template}{media_indicator}".strip()
    display_text = (text[:20] + "...") if len(text) > 20 else text
    comment_id = f"c{i+1}"
    comment_texts[comment_id] = text
    comments.append({
        "commentId": comment_id,
        "userId": user_id,
        "text": text,
        "displayText": display_text,
        "createdAt": created_at.strftime("%Y-%m-%dT%H:%M:%S"),
        "likesCount": 0
    })
    comment_parents.append({"commentId": comment_id, "parentId": parent_comment_id, "parentType": "Comment"})
    comment_created_times[comment_id] = created_at

comments_df = pd.DataFrame(comments)
comments_df.to_csv(os.path.join(output_dir, "comments.csv"), index=False)

# 7. Generate FOLLOWS (150 relationships)
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

# 8. Generate LIKED (400 for posts + 200 for comments)
likes = []
used_likes = set()
while len(likes) < 400:
    user_id = f"u{random.randint(1, 50)}"
    post_id = f"p{random.choices(range(1, 201), weights=post_weights)[0]}"
    parent_time = post_created_times[post_id]
    timestamp = parent_time + timedelta(minutes=random.randint(1, 2880))
    key = (user_id, post_id, "Post")
    if key not in used_likes:
        likes.append({
            "userId": user_id,
            "targetId": post_id,
            "targetType": "Post",
            "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S")
        })
        used_likes.add(key)
while len(likes) < 600:
    user_id = f"u{random.randint(1, 50)}"
    comment_id = f"c{random.randint(1, 300)}"
    parent_time = comment_created_times[comment_id]
    timestamp = parent_time + timedelta(minutes=random.randint(1, 2880))
    key = (user_id, comment_id, "Comment")
    if key not in used_likes:
        likes.append({
            "userId": user_id,
            "targetId": comment_id,
            "targetType": "Comment",
            "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S")
        })
        used_likes.add(key)
likes_df = pd.DataFrame(likes)
likes_df.to_csv(os.path.join(output_dir, "likes.csv"), index=False)

# Update likesCount
post_likes_count = likes_df[likes_df['targetType'] == 'Post']['targetId'].value_counts().to_dict()
for post in posts:
    post['likesCount'] = post_likes_count.get(post['postId'], 0)
posts_df = pd.DataFrame(posts)
posts_df.to_csv(os.path.join(output_dir, "posts.csv"), index=False)
comment_likes_count = likes_df[likes_df['targetType'] == 'Comment']['targetId'].value_counts().to_dict()
for comment in comments:
    comment['likesCount'] = comment_likes_count.get(comment['commentId'], 0)
comments_df = pd.DataFrame(comments)
comments_df.to_csv(os.path.join(output_dir, "comments.csv"), index=False)

# 9. Generate TAGGED_WITH (250 relationships)
tagged_with = []
for post_id, text in post_texts.items():
    found_tags = re.findall(r'#(\w+)', text)
    for tag in set(found_tags):
        if tag.lower() in hashtags_df['tag'].values:
            tagged_with.append({"postId": post_id, "tag": tag.lower()})
for comment_id, text in comment_texts.items():
    found_tags = re.findall(r'#(\w+)', text)
    for tag in set(found_tags):
        if tag.lower() in hashtags_df['tag'].values:
            tagged_with.append({"commentId": comment_id, "tag": tag.lower()})
while len(tagged_with) < 250:
    if random.random() < 0.7:
        tagged_with.append({"postId": f"p{random.choices(range(1, 201), weights=post_weights)[0]}", "tag": random.choice(hashtags)})
    else:
        tagged_with.append({"commentId": f"c{random.randint(1, 300)}", "tag": random.choice(hashtags)})
tagged_with_df = pd.DataFrame(tagged_with)
tagged_with_df.to_csv(os.path.join(output_dir, "tagged_with.csv"), index=False)

# 10. Generate MENTIONS (100 relationships)
mentions = []
for post_id, text in post_texts.items():
    found_mentions = re.findall(r'@(\w+)', text)
    post_user_id = posts_df[posts_df['postId'] == post_id]['userId'].iloc[0]
    post_user_name = next(u['name'] for u in users if u['userId'] == post_user_id)
    for mention_name in set(found_mentions):
        matching_users = [u['userId'] for u in users if mention_name.lower() in u['name'].lower().split()[0] and u['name'] != post_user_name]
        if matching_users:
            mentions.append({"postId": post_id, "userId": random.choice(matching_users)})
for comment_id, text in comment_texts.items():
    found_mentions = re.findall(r'@(\w+)', text)
    comment_user_id = comments_df[comments_df['commentId'] == comment_id]['userId'].iloc[0]
    comment_user_name = next(u['name'] for u in users if u['userId'] == comment_user_id)
    for mention_name in set(found_mentions):
        matching_users = [u['userId'] for u in users if mention_name.lower() in u['name'].lower().split()[0] and u['name'] != comment_user_name]
        if matching_users:
            mentions.append({"commentId": comment_id, "userId": random.choice(matching_users)})
mentions = mentions[:100]
if len(mentions) < 100:
    for _ in range(100 - len(mentions)):
        if random.random() < 0.7:
            mentions.append({"postId": f"p{random.choices(range(1, 201), weights=post_weights)[0]}", "userId": f"u{random.randint(1, 50)}"})
        else:
            mentions.append({"commentId": f"c{random.randint(1, 300)}", "userId": f"u{random.randint(1, 50)}"})
mentions_df = pd.DataFrame(mentions)
mentions_df.to_csv(os.path.join(output_dir, "mentions.csv"), index=False)

# 11. Generate REPLIES_TO (300 relationships)
replies_to = []
for parent in comment_parents:
    replies_to.append({
        "commentId": parent['commentId'],
        "parentId": parent['parentId'],
        "parentType": parent['parentType']
    })
replies_to_df = pd.DataFrame(replies_to)
replies_to_df.to_csv(os.path.join(output_dir, "replies_to.csv"), index=False)

# 12. Generate SHARES (100 relationships)
shares = []
used_shares = set()
while len(shares) < 100:
    user_id = f"u{random.randint(1, 50)}"
    post_id = f"p{random.choices(range(1, 201), weights=post_weights)[0]}"
    parent_time = post_created_times[post_id]
    timestamp = parent_time + timedelta(days=random.randint(0, 7))
    key = (user_id, post_id)
    if key not in used_shares:
        shares.append({
            "userId": user_id,
            "postId": post_id,
            "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S")
        })
        used_shares.add(key)
shares_df = pd.DataFrame(shares)
shares_df.to_csv(os.path.join(output_dir, "shares.csv"), index=False)

# 13. Generate CONTAINS (150 relationships)
contains = []
for post_id, text in post_texts.items():
    found_urls = re.findall(r'https?://\S+', text)
    for url in set(found_urls):
        matching_url_ids = [u['urlId'] for u in urls if u['url'] == url]
        url_id = matching_url_ids[0] if matching_url_ids else f"l{random.randint(1, 50)}"
        contains.append({"parentId": post_id, "parentType": "Post", "childId": url_id, "childType": "URL"})
for comment_id, text in comment_texts.items():
    found_urls = re.findall(r'https?://\S+', text)
    for url in set(found_urls):
        url_id = f"l{random.randint(1, 50)}"
        contains.append({"parentId": comment_id, "parentType": "Comment", "childId": url_id, "childType": "URL"})
while len(contains) < 150:
    if random.random() < 0.7:
        parent_id = f"p{random.choices(range(1, 201), weights=post_weights)[0]}"
        parent_type = "Post"
    else:
        parent_id = f"c{random.randint(1, 300)}"
        parent_type = "Comment"
    if random.random() < 0.6:
        child_id = f"m{random.randint(1, 100)}"
        child_type = "Media"
    else:
        child_id = f"l{random.randint(1, 50)}"
        child_type = "URL"
    contains.append({"parentId": parent_id, "parentType": parent_type, "childId": child_id, "childType": child_type})
contains = list({(c['parentId'], c['childId']): c for c in contains}.values())
contains_df = pd.DataFrame(contains)
contains_df.to_csv(os.path.join(output_dir, "contains.csv"), index=False)

print(f"CSVs generated in {output_dir}")
print(f"Generated: {len(users)} Users, {len(hashtags_df)} Hashtags, {len(posts)} Posts, {len(media)} Media, {len(urls)} URLs, {len(comments)} Comments")
print(f"Relationships: {len(follows)} FOLLOWS, {len(likes)} LIKED, {len(tagged_with)} TAGGED_WITH, {len(mentions)} MENTIONS, {len(replies_to)} REPLIES_TO, {len(shares)} SHARES, {len(contains)} CONTAINS")