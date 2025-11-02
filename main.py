import praw
import pandas as pd
import config
from datetime import datetime

def extract_comments_from_url(post_url):
    """
    Extract all comments from a Reddit post and save to CSV.
    
    Args:
        post_url (str): URL of the Reddit post
    
    Returns:
        str: Filename of the generated CSV
    """
    
    # Initialize Reddit instance
    print("Connecting to Reddit...")
    reddit = praw.Reddit(
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        user_agent=config.USER_AGENT
    )
    
    # Get the submission (post)
    print(f"Fetching post: {post_url}")
    submission = reddit.submission(url=post_url)
    
    # Load all comments (including nested replies)
    print("Loading all comments (this may take a while)...")
    submission.comments.replace_more(limit=None)
    
    # Extract comment data
    comments_data = []
    
    print("Extracting comment data...")
    for comment in submission.comments.list():
        comments_data.append({
            'author': str(comment.author) if comment.author else '[deleted]',
            'body': comment.body,
            'score': comment.score,
            'created_utc': datetime.fromtimestamp(comment.created_utc),
            'parent_id': comment.parent_id,
            'comment_id': comment.id,
            'is_submitter': comment.is_submitter,
            'permalink': f"https://reddit.com{comment.permalink}"
        })

    return comments_data

def save_to_csv(all_comments, filename=None):
    """
    Save comments to CSV file.
    
    Args:
        all_comments (list): List of comment dictionaries
        filename (str): Optional custom filename
    
    Returns:
        str: Filename of the saved CSV
    """
    if not all_comments:
        print("⚠️  No comments to save")
        return None
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reddit_comments_{timestamp}.csv"
    
    # Create DataFrame and save
    df = pd.DataFrame(all_comments)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ Success!")
    print(f"📊 Total comments: {len(all_comments)}")
    print(f"💾 Saved to: {filename}")
    
    return filename

def show_menu():
    """
    Display menu and get user choice.
    
    Returns:
        str: User's choice ('1', '2', or '3')
    """
    print("\n" + "=" * 60)
    print("        REDDIT COMMENT EXTRACTOR")
    print("=" * 60)
    print("\nHow do you want to provide URLs?")
    print("  1. Enter URLs manually (one by one)")
    print("  2. Load URLs from a text file")
    print("  3. Exit")
    print()
    
    choice = input("Enter your choice (1-3): ").strip()
    return choice

def get_urls_from_console():
    """
    Get URLs from user input (console).
    
    Returns:
        list: List of URLs
    """
    print("\nEnter Reddit post URLs (one per line)")
    print("Press Enter on empty line when done")
    print("-" * 60)
    
    urls = []
    while True:
        url = input("URL: ").strip()
        
        if not url:  # Empty line = done
            break
        
        urls.append(url)
        print(f"  ✓ Added ({len(urls)} total)")
    
    return urls


def get_urls_from_file():
    """
    Get URLs from a text file.
    
    Returns:
        list: List of URLs
    """
    filename = input("\nEnter filename (e.g., urls.txt): ").strip()
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # Leer líneas, quitar espacios y líneas vacías
            urls = []
            for line in f:
                stripped = line.strip()
                if stripped:
                    urls.append(stripped)
        
        print(f"✓ Loaded {len(urls)} URL(s) from {filename}")
        return urls
        
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found")
        return []
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return []


def main():
    """
    Main function - prompts user for post URL and extracts comments.
    """
    choice = show_menu()
    
    if choice == '1':
        print("\n📝 Manual input mode")
        urls = get_urls_from_console()

        if not urls:
            print("❌ No URLs provided")
            return
        
        print(f"\n🔄 Processing {len(urls)} URL(s)...")

        all_comments = []
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Processing: {url}")
            try:
                comments = extract_comments_from_url(url)
                all_comments.extend(comments)
            except Exception as e:
                print(f"  ❌ Error: {e}")
                continue
        
        save_to_csv(all_comments)
        
    elif choice == '2':
        print("\n📁 File input mode")
        urls = get_urls_from_file()
        
        if not urls:
            print("❌ No URLs loaded")
            return
        
        print(f"\n🔄 Processing {len(urls)} URL(s)...")
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Processing: {url}")
            try:
                comments = extract_comments_from_url(url)
                save_to_csv(comments, datetime.now().strftime("%Y%m%d_%H%M%S")+"_"+str(i))
            except Exception as e:
                print(f"  ❌ Error: {e}")
                continue
        
    elif choice == '3':
        print("\n👋 Goodbye!")
        return
        
    else:
        print("\n❌ Invalid choice. Please run again.")
        return

if __name__ == "__main__":
    main()