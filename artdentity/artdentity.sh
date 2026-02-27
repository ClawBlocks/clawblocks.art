#!/bin/bash
# Artdentity Card Generator
# Usage: artdentity.sh <moltbook-username> <api-key>
# Fetches a user's posts and outputs their content for analysis

set -euo pipefail

USERNAME="${1:?Usage: artdentity.sh <username> <api-key>}"
API_KEY="${2:?Usage: artdentity.sh <username> <api-key>}"
BASE_URL="https://www.moltbook.com/api/v1"

# Fetch user profile
echo "=== PROFILE ==="
curl -sf -H "X-API-Key: $API_KEY" "$BASE_URL/users/${USERNAME}" 2>/dev/null | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    u = data.get('user', data)
    print(f\"Name: {u.get('name', 'unknown')}\")
    print(f\"Bio: {u.get('description', 'none')}\")
    print(f\"Karma: {u.get('karma', 0)}\")
    print(f\"Followers: {u.get('followerCount', 0)}\")
except:
    print('Profile not found')
" 2>/dev/null || echo "Profile not found"

echo ""
echo "=== POSTS ==="
curl -sf -H "X-API-Key: $API_KEY" "$BASE_URL/posts?author=${USERNAME}&limit=50" 2>/dev/null | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    posts = data.get('posts', data if isinstance(data, list) else [])
    for p in posts[:50]:
        title = p.get('title', '')
        body = p.get('content', p.get('body', ''))
        score = p.get('score', p.get('upvotes', 0))
        print(f'[{score}↑] {title}')
        if body:
            print(body[:500])
        print('---')
    if not posts:
        print('No posts found')
except:
    print('No posts found')
" 2>/dev/null || echo "No posts found"
