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
    
    # Create DataFrame
    df = pd.DataFrame(comments_data)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reddit_comments_{timestamp}.csv"
    
    # Save to CSV
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ Success!")
    print(f"📊 Total comments extracted: {len(comments_data)}")
    print(f"💾 Saved to: {filename}")
    
    return filename

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


def main():
    """
    Main function - prompts user for post URL and extracts comments.
    """
    print("=" * 60)
    print("        REDDIT COMMENT EXTRACTOR")
    print("=" * 60)
    print()
    
    # Ask user for post URL
    post_url = input("Enter Reddit post URL: ").strip()
    
    if not post_url:
        print("❌ Error: URL cannot be empty")
        return
    
    try:
        comments = extract_comments_from_url(post_url)
        # Imprimir cuántos se extrajeron
        save_to_csv(comments)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  - The URL is valid")
        print("  - Your config.py has correct credentials")
        print("  - You have internet connection")


if __name__ == "__main__":
    main()