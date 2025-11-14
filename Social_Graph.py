import datetime

# =============================================================================
# SECTION 1: DIRECTED GRAPH CLASS - Handles follow relationships
# =============================================================================

class DirectedGraph:
    """Directed graph to represent follow relationships between users"""

    def __init__(self):
        # Dictionary to store adjacency list: {user: [followed_users]}
        self.graph = dict()

    def addVertex(self, vertex):
        """Add a new user vertex to the graph"""
        if vertex not in self.graph:
            self.graph[vertex] = []

    def addEdge(self, from_vertex, to_vertex):
        """Add follow relationship: from_vertex follows to_vertex"""
        if from_vertex in self.graph and to_vertex in self.graph:
            if to_vertex not in self.graph[from_vertex]:
                self.graph[from_vertex].append(to_vertex)
        else:
            raise ValueError("One or both vertices are not found in the graph")

    def listOutgoingAdjacentVertex(self, vertex):
        """Get list of users that the given user follows"""
        return self.graph.get(vertex, [])

    def has_vertex(self, vertex):
        """Check if user exists in graph"""
        return vertex in self.graph

    def has_edge(self, from_vertex, to_vertex):
        """Check if from_vertex follows to_vertex"""
        if from_vertex in self.graph:
            return to_vertex in self.graph[from_vertex]
        return False

    def get_all_vertices(self):
        """Get all users in the graph"""
        return list(self.graph.keys())

    def remove_edge(self, from_vertex, to_vertex):
        """Remove follow relationship"""
        if from_vertex in self.graph and to_vertex in self.graph:
            if to_vertex in self.graph[from_vertex]:
                self.graph[from_vertex].remove(to_vertex)
            else:
                print(f"Edge {from_vertex} -> {to_vertex} does not exist")
        else:
            print(f"Vertex does not exist.")

    def remove_vertex(self, vertex):
        """Remove user and all their relationships"""
        if vertex not in self.graph:
            print(f"Vertex {vertex} does not exist.")
        else:
            # Remove from other users' follow lists
            for neighbour in self.graph.values():
                if vertex in neighbour:
                    neighbour.remove(vertex)
            del self.graph[vertex]


# =============================================================================
# SECTION 2: PERSON CLASS - Represents user data and posts
# =============================================================================

class Person:
    """Represents a user in the social network"""

    def __init__(self, username, password, name, gender, biography, is_public=True):
        self.username = username
        self.password = password
        self.name = name
        self.gender = gender
        self.biography = biography
        self.is_public = is_public
        self.pending_followers = []  # Users who requested to follow (for private accounts)
        self.posts = []  # User's posts

    def __str__(self):
        return self.username

    def display_public_profile(self, followers_count, following_count):
        """Display public profile information"""
        return f"""📋 Public Profile
Name: {self.name}
Username: {self.username}
Followers: {followers_count}
Following: {following_count}
Account Type: {'🌐 Public' if self.is_public else '🔒 Private'}"""

    def display_private_profile(self, followers_count, following_count):
        """Display complete profile information"""
        return f"""📋 Profile
Name: {self.name}
Username: {self.username}
Gender: {self.gender}
Bio: {self.biography}
Followers: {followers_count}
Following: {following_count}
Account Type: {'🌐 Public' if self.is_public else '🔒 Private'}"""

    def display_basic_info(self):
        """Display basic info for private accounts (non-followers)"""
        return f"""📋 User Profile
Name: {self.name}
Username: {self.username}
🔒This is a private account. Follow to see full profile."""

    def add_pending_follower(self, username):
        """Add user to pending followers list"""
        if username not in self.pending_followers:
            self.pending_followers.append(username)

    def remove_pending_follower(self, username):
        """Remove user from pending followers list"""
        if username in self.pending_followers:
            self.pending_followers.remove(username)

    def get_pending_followers(self):
        """Get list of pending follower requests"""
        return self.pending_followers.copy()

    def add_post(self, content):
        """Add a new post with timestamp"""
        post = {
            'content': content,
            'timestamp': datetime.datetime.now(),
            'id': len(self.posts) + 1
        }
        self.posts.append(post)
        return post

    def get_posts(self):
        """Get all user posts"""
        return self.posts.copy()

    def delete_post(self, post_id):
        """Delete post by ID"""
        for i, post in enumerate(self.posts):
            if post['id'] == post_id:
                del self.posts[i]
                return True
        return False

    def display_posts_preview(self):
        """Display preview of recent posts"""
        if not self.posts:
            return "No posts yet"

        preview = f"📝 Recent Posts ({len(self.posts)}):\n"
        # Show latest 3 posts
        for post in self.posts[-3:][::-1]:
            time_str = post['timestamp'].strftime("%m/%d %H:%M")
            content_preview = post['content'][:30] + "..." if len(post['content']) > 30 else post['content']
            preview += f"  🕒 {time_str}: {content_preview}\n"
        return preview

# =============================================================================
# SECTION 3: SOCIAL MEDIA APP CLASS - Main application logic
# =============================================================================

class SocialMediaApp:
    """Main social media application controller"""

    def __init__(self):
        self.graph = DirectedGraph()
        self.people = {}  # username -> Person object
        self.current_user = None

    def register_user(self, username, password, name, gender, biography, is_public=True):
        """Register a new user"""
        if username in self.people:
            return False, "Username already exists"

        new_person = Person(username, password, name, gender, biography, is_public)
        self.people[username] = new_person
        self.graph.addVertex(username)
        return True, "Registration successful"

    def login(self, username, password):
        """User login"""
        if username not in self.people:
            return False, "User not found"

        if self.people[username].password == password:
            self.current_user = username
            return True, f"Welcome back, {self.people[username].name}!"
        else:
            return False, "Incorrect password"

    def admin_login(self, password):
        """Admin login"""
        if password == "1234":
            return True, "Admin login successful"
        return False, "Admin password incorrect"

    def logout(self):
        """User logout"""
        self.current_user = None
        return "Logged out successfully"

    def send_follow_request(self, target_username):
        """Send follow request to another user"""
        if not self.current_user:
            return "Please login first"

        if target_username == self.current_user:
            return "Cannot follow yourself"

        if target_username not in self.people:
            return "User not found"

        if self.graph.has_edge(self.current_user, target_username):
            return "Already following this user"

        target_person = self.people[target_username]

        # Public accounts: follow directly
        if target_person.is_public:
            self.graph.addEdge(self.current_user, target_username)
            return f"✅ Now following {target_username}"
        else:
            # Private accounts: send follow request
            if self.current_user in target_person.pending_followers:
                return "Follow request already sent, waiting for approval"
            else:
                target_person.add_pending_follower(self.current_user)
                return f"📨 Follow request sent to {target_username}, waiting for approval"

    def unfollow(self, target_username):
        """Unfollow user or cancel follow request"""
        if not self.current_user:
            return "Please login first"

        if target_username not in self.people:
            return "User not found"

        target_person = self.people[target_username]

        # If already following, unfollow
        if self.graph.has_edge(self.current_user, target_username):
            self.graph.remove_edge(self.current_user, target_username)
            return f"✅ Unfollowed {target_username}"

        # If pending request, cancel it
        elif self.current_user in target_person.pending_followers:
            target_person.remove_pending_follower(self.current_user)
            return f"✅ Cancelled follow request to {target_username}"
        else:
            return "Not following this user"

    def approve_follower(self, requester_username):
        """Approve a follow request"""
        if not self.current_user:
            return "Please login first"

        current_person = self.people[self.current_user]

        if requester_username not in current_person.pending_followers:
            return "This user hasn't sent a follow request"

        # Approve request and create follow relationship
        current_person.remove_pending_follower(requester_username)
        self.graph.addEdge(requester_username, self.current_user)
        return f"✅ Approved {requester_username}'s follow request"

    def reject_follower(self, requester_username):
        """Reject a follow request"""
        if not self.current_user:
            return "Please login first"

        current_person = self.people[self.current_user]

        if requester_username not in current_person.pending_followers:
            return "This user hasn't sent a follow request"

        current_person.remove_pending_follower(requester_username)
        return f"✅ Rejected {requester_username}'s follow request"

    def get_following_count(self, username):
        """Get number of users followed by username"""
        return len(self.graph.listOutgoingAdjacentVertex(username))

    def get_followers_count(self, username):
        """Get number of followers for username"""
        count = 0
        for user in self.people:
            if self.graph.has_edge(user, username):
                count += 1
        return count

    def get_following(self, username=None):
        """Get list of users followed by username"""
        target = username or self.current_user
        if not target:
            return []
        return self.graph.listOutgoingAdjacentVertex(target)

    def get_followers(self, username):
        """Get list of followers for username"""
        followers = []
        for user in self.people:
            if self.graph.has_edge(user, username):
                followers.append(user)
        return followers

    def is_mutual_follow(self, user1, user2):
        """Check if two users follow each other"""
        return (self.graph.has_edge(user1, user2) and
                self.graph.has_edge(user2, user1))

    def get_follow_status(self, target_username):
        """Get follow relationship status for current user"""
        if not self.current_user or target_username not in self.people:
            return "Not Follow"

        if self.graph.has_edge(self.current_user, target_username):
            if self.graph.has_edge(target_username, self.current_user):
                return "Mutual"
            else:
                return "Following"

        target_person = self.people[target_username]
        if self.current_user in target_person.pending_followers:
            return "Requested"

        return "Not Follow"

    def can_view_private_content(self, target_username):
        """Check if current user can view private account content"""
        if not self.current_user:
            return False

        target_person = self.people[target_username]

        # Public accounts: anyone can view
        if target_person.is_public:
            return True

        # Private accounts: only if current user follows them
        return self.graph.has_edge(self.current_user, target_username)

    def view_profile(self, target_username, ignore_privacy=False, is_admin=False):
        """View user profile with appropriate privacy controls"""
        if target_username not in self.people:
            return None, "User not found"

        target_person = self.people[target_username]
        followers_count = self.get_followers_count(target_username)
        following_count = self.get_following_count(target_username)

        # Admin mode or ignore privacy
        if ignore_privacy or is_admin:
            profile = target_person.display_private_profile(followers_count, following_count)
            posts_preview = target_person.display_posts_preview()
            return target_person, f"{profile}\n\n{posts_preview}"

        # Normal user view
        is_own_profile = self.current_user == target_username
        can_view_private = self.can_view_private_content(target_username)

        if is_own_profile or can_view_private:
            profile = target_person.display_private_profile(followers_count, following_count)
            posts_preview = target_person.display_posts_preview()
            return target_person, f"{profile}\n\n{posts_preview}"
        elif target_person.is_public:
            profile = target_person.display_public_profile(followers_count, following_count)
            posts_preview = target_person.display_posts_preview()
            return target_person, f"{profile}\n\n{posts_preview}"
        else:
            return target_person, target_person.display_basic_info()

    def get_all_users(self):
        """Get all registered usernames"""
        return list(self.people.keys())

    def get_recommendations(self):
        """Get recommended users (not followed yet)"""
        if not self.current_user:
            return []

        following = set(self.get_following())
        all_users = set(self.get_all_users())
        recommendations = all_users - following - {self.current_user}
        return list(recommendations)

    def update_profile(self, new_name, new_gender, new_bio, new_privacy):
        """Update current user's profile"""
        if not self.current_user:
            return "Please login first"

        person = self.people[self.current_user]
        person.name = new_name
        person.gender = new_gender
        person.biography = new_bio
        person.is_public = new_privacy
        return "✅ Profile updated successfully"

    def get_pending_requests(self):
        """Get pending follow requests for current user"""
        if not self.current_user:
            return []
        current_person = self.people[self.current_user]
        return current_person.get_pending_followers()


# =============================================================================
# SECTION 4: POST MANAGEMENT FLOW
# =============================================================================

def manage_posts_flow(app):
    current_person = app.people[app.current_user]
    choice = None

    while choice != '0':
        print(f"\n📝 MY POSTS ({len(current_person.posts)})")

        if current_person.posts:
            headers = ["ID", "Time", "Content"]
            data = []
            for post in current_person.posts[::-1]:
                time_str = post['timestamp'].strftime("%Y/%m/%d %H:%M")
                content = post['content']
                if len(content) > 50:
                    content = content[:50] + "..."
                data.append([post['id'], time_str, content])

            print_table(headers, data)
        else:
            print("No posts yet")

        print("\nAction:")
        print("-" * 30)
        print("1. ➕ Create New Post")
        if current_person.posts:
            print("2. 🗑️ Delete Post")
        print("0. ↩️ Back")
        print("-" * 30)

        choice = get_input_with_retry("* Enter your action choice (0 to go back): ", allow_zero=True)
        if choice is None:
            break

        if choice == '1':
            post_content = get_input_with_retry("* Enter post content: ", allow_zero=True)
            if post_content is not None:
                post = current_person.add_post(post_content)
                time_str = post['timestamp'].strftime("%Y/%m/%d %H:%M")
                print_success(f"✅ Post published successfully! ({time_str})")

        elif choice == '2' and current_person.posts:
            post_id_input = get_input_with_retry("* Enter post ID to delete: ", allow_zero=True)
            if post_id_input:
                try:
                    post_id = int(post_id_input)
                    if current_person.delete_post(post_id):
                        print_success("✅ Post deleted successfully!")
                    else:
                        print_error("❌ Post ID not found")
                except ValueError:
                    print_error("❌ Invalid ID")
        elif choice != '0':
            print_error("❌ Invalid choice")

# =============================================================================
# SECTION 5: DATA INITIALIZATION
# =============================================================================

def create_sample_data(app):
    """Create sample users and relationships for testing"""
    sample_users = [
        ("alice", "pass123", "Alice Smith", "🚹 Male", "Love traveling and photography", True),
        ("bob", "pass123", "Bob Johnson", "🚹 Male", "Software developer, love open source projects", True),
        ("charlie", "pass123", "Charlie Brown", "🚹 Male", "Private space, please don't disturb", False),
        ("diana", "pass123", "Diana Prince", "🚺 Female", "Food blogger, share daily life", True),
        ("eve", "pass123", "Eve Wilson", "🚺 Female", "Fitness coach", True)
    ]

    for username, password, name, gender, bio, is_public in sample_users:
        app.register_user(username, password, name, gender, bio, is_public)

    # Create follow relationships
    follow_relationships = [
        ("alice", "bob"), ("alice", "diana"),
        ("bob", "alice"), ("bob", "eve"),
        ("charlie", "alice"),
        ("diana", "alice"), ("diana", "eve"),
        ("eve", "bob")
    ]

    for follower, followed in follow_relationships:
        app.graph.addEdge(follower, followed)

    # Add some pending requests
    app.people["charlie"].add_pending_follower("bob")
    app.people["charlie"].add_pending_follower("eve")

    # Add sample posts
    app.people["alice"].add_post("Went to the beach today, beautiful scenery! 🌊")
    app.people["alice"].add_post("Sharing some travel photos with everyone")
    app.people["bob"].add_post("Just completed a new project, feeling accomplished!")
    app.people["diana"].add_post("Tried a new recipe, tastes great!~")


# =============================================================================
# SECTION 6: UI UTILITIES (Print formatting and input handling)
# =============================================================================

def print_success(message):
    """Print success message in green"""
    print(f"\033[92m{message}\033[0m")

def print_error(message):
    """Print error message in red"""
    print(f"\033[91m{message}\033[0m")

def print_table(headers, data):
    """Print data in table format"""
    # Calculate column widths
    col_widths = [len(str(header)) for header in headers]
    for row in data:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    # Create separator line
    separator = "+" + "+".join("-" * (width + 2) for width in col_widths) + "+"

    # Print header
    print(separator)
    header_row = "| " + " | ".join(str(headers[i]).ljust(col_widths[i]) for i in range(len(headers))) + " |"
    print(header_row)
    print(separator)

    # Print data rows
    for row in data:
        data_row = "| " + " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row))) + " |"
        print(data_row)

    print(separator)

def get_input_with_retry(prompt, allow_zero=True):
    user_input = input(prompt)

    if allow_zero and user_input == '0':
        return None

    if user_input.strip():
        return user_input

    print_error("❌ Input cannot be empty. Please try again or enter 0 to go back.")
    return get_input_with_retry(prompt, allow_zero)

# =============================================================================
# SECTION 7: DISPLAY FUNCTIONS (Table and menu displays)
# =============================================================================

def display_all_users_table(app, is_admin=False):
    """Display all users in table format"""
    headers = ["Username", "Name", "Followers", "Following", "Type"]
    data = []

    users = app.get_all_users()
    for username in users:
        person = app.people[username]
        followers_count = app.get_followers_count(username)
        following_count = app.get_following_count(username)
        account_type = '🌐 Public' if person.is_public else '🔒 Private'

        data.append([username, person.name, followers_count, following_count, account_type])

    print_table(headers, data)
    return users

def display_all_users_detailed_table_with_posts(app):
    """Display all users with detailed info including post count"""
    headers = ["Username", "Name", "Gender", "Bio", "Followers", "Following", "Posts", "Type"]
    data = []

    users = app.get_all_users()
    for username in users:
        person = app.people[username]
        followers_count = app.get_followers_count(username)
        following_count = app.get_following_count(username)
        posts_count = len(person.posts)
        account_type = '🌐 Public' if person.is_public else '🔒 Private'

        # Truncate long bio
        bio = person.biography
        if len(bio) > 15:
            bio = bio[:15] + "..."

        data.append([
            username, person.name, person.gender, bio,
            followers_count, following_count, posts_count, account_type
        ])

    print_table(headers, data)
    return users

def display_user_selection(app, users, current_user=None):
    """Display user selection table (exclude current user)"""
    headers = ["No", "Username", "Name", "Status", "Type"]
    data = []

    filtered_users = [u for u in users if u != current_user] if current_user else users
    for i, username in enumerate(filtered_users, 1):
        person = app.people[username]
        follow_status = app.get_follow_status(username) if current_user else "Not Follow"
        account_type = '🌐 Public' if person.is_public else '🔒 Private'

        data.append([i, username, person.name, follow_status, account_type])

    print_table(headers, data)
    return filtered_users

# =============================================================================
# SECTION 8: PROFILE AND FOLLOW OPTIONS
# =============================================================================

def show_profile_and_follow_options(app, target_user):
    """Display user profile and follow/unfollow options"""
    person, profile = app.view_profile(target_user)
    print(f"\n{profile}")

    if target_user == app.current_user:
        show_own_profile_options(app, target_user)
        return

    is_following = app.graph.has_edge(app.current_user, target_user)
    has_pending_request = app.current_user in app.people[target_user].pending_followers
    can_view_private = app.can_view_private_content(target_user)
    target_is_public = app.people[target_user].is_public

    choice = None

    while choice != '0':   # user enters '0' → exit
        print(f"\n👤 User: @{target_user}")

        # Show followers/following options only if permitted
        if target_is_public or can_view_private:
            print("1. 👀 View Followers")
            print("2. ❤️ View Following")
            option_offset = 2
        else:
            option_offset = 0

        # Follow/unfollow option
        if is_following:
            print(f"{option_offset + 1}. ❌ Unfollow")
        elif has_pending_request:
            print(f"{option_offset + 1}. ❌ Cancel Follow Request")
        else:
            print(f"{option_offset + 1}. ➕ Follow")

        print(f"{option_offset + 2}. ↩️ Back (0 also works)")

        choice = get_input_with_retry("* Enter your choice (0 to go back): ", allow_zero=True)

        if choice is None:   # user pressed 0
            break

        if choice == '1' and option_offset >= 2:
            view_followers_flow(app, target_user)

        elif choice == '2' and option_offset >= 2:
            view_following_flow(app, target_user)

        elif choice == str(option_offset + 1):
            # Follow / unfollow logic
            if is_following:
                result = app.unfollow(target_user)
                print_success(result)
                is_following = False
                has_pending_request = False
                can_view_private = app.can_view_private_content(target_user)

            elif has_pending_request:
                result = app.unfollow(target_user)
                print_success(result)
                has_pending_request = False

            else:
                result = app.send_follow_request(target_user)
                print_success(result)
                if "request" in result.lower():
                    has_pending_request = True
                else:
                    is_following = True
                    can_view_private = app.can_view_private_content(target_user)

        elif choice == str(option_offset + 2):
            break

        else:
            print_error("❌ Invalid choice, please try again")

def show_own_profile_options(app, target_user):
    """Show profile editing options for own profile"""
    person, profile = app.view_profile(target_user)
    print(f"\n{profile}")

    edit = input("\n* Edit profile? (y/n): ").lower()
    if edit == 'y':
        new_name = input(f"* Enter name ({person.name}): ") or person.name

        print("* Select gender:")
        print("   1. 🚹 Male")
        print("   2. 🚺 Female")
        print("   3. ⚧️ Other")
        gender_choice = input(f"* Enter your choice (1-3) [{person.gender}]: ")
        if gender_choice == '1':
            new_gender = "🚹 Male"
        elif gender_choice == '2':
            new_gender = "🚺 Female"
        elif gender_choice == '3':
            new_gender = "⚧️ Other"
        else:
            new_gender = person.gender

        new_bio = input(f"* Enter bio ({person.biography}): ") or person.biography

        print("* Account type:")
        print("   1. 🌐 Public")
        print("   2. 🔒 Private")
        new_privacy = input(f"* Enter your choice (1-2) [{'1' if person.is_public else '2'}]: ")
        is_public = new_privacy == '1' if new_privacy else person.is_public

        result = app.update_profile(new_name, new_gender, new_bio, is_public)
        print_success(result)

# =============================================================================
# SECTION 9: FOLLOW REQUEST MANAGEMENT
# =============================================================================

def manage_follow_requests_flow(app):
    """Handle follow request approvals/rejections"""

    choice = None

    while choice != '3':
        pending_requests = app.get_pending_requests()

        if not pending_requests:
            print("\n📭 No pending follow requests")
            return

        print(f"\n📭 PENDING FOLLOW REQUESTS ({len(pending_requests)})")
        headers = ["No", "Username", "Name"]
        data = []
        for i, username in enumerate(pending_requests, 1):
            person = app.people[username]
            data.append([i, username, person.name])

        print_table(headers, data)

        print("\nAction：")
        print("-" * 30)
        print("1. ✅ Approve Request")
        print("2. ❌ Reject Request")
        print("3. ↩️ Back")
        print("-" * 30)

        choice = get_input_with_retry("* Enter your action choice (0 to go back): ", allow_zero=True)

        if choice is None:
            break

        if choice in ['1', '2']:
            req_choice = get_input_with_retry("* Select username's number: ", allow_zero=True)
            if req_choice is None:
                continue

            try:
                idx = int(req_choice) - 1
                if 0 <= idx < len(pending_requests):
                    requester = pending_requests[idx]
                    if choice == '1':
                        print_success(app.approve_follower(requester))
                    else:
                        print_success(app.reject_follower(requester))
                else:
                    print_error("❌ Invalid selection")
            except ValueError:
                print_error("❌ Please enter a valid number")
        elif choice != '3':
            print_error("❌ Invalid choice, please try again")

# =============================================================================
# SECTION 10: FOLLOWERS/FOLLOWING VIEW FLOWS
# =============================================================================

def view_following_flow(app, target_user):
    """View and interact with users followed by a user"""

    print(f"\n❤️ @{target_user}'s FOLLOWING")
    following = app.get_following(target_user)

    if not following:
        print("📭 Not following anyone yet")
        return

    headers = ["No", "Username", "Name", "Status"]
    data = []
    for i, user in enumerate(following, 1):
        person = app.people[user]
        if user == app.current_user:
            data.append([i, user, person.name, ""])
        else:
            follow_status = app.get_follow_status(user)
            data.append([i, user, person.name, follow_status])

    print_table(headers, data)

    view_choice = get_input_with_retry(
        "* Select No of username to view profile (0 to go back): ",
        allow_zero=True
    )

    if view_choice is None:
        return

    try:
        idx = int(view_choice) - 1
        if 0 <= idx < len(following):
            selected_user = following[idx]

            if selected_user == app.current_user:
                print("👤 This is your own account")
                return view_following_flow(app, target_user)

            show_profile_and_follow_options(app, selected_user)
            return view_following_flow(app, target_user)

        else:
            print_error("❌ Invalid selection")
            return view_following_flow(app, target_user)

    except ValueError:
        print_error("❌ Please enter a valid number")
        return view_following_flow(app, target_user)


def view_followers_flow(app, target_user):
    """View and interact with followers of a user"""

    print(f"\n👥 @{target_user}'s FOLLOWERS")
    followers = app.get_followers(target_user)

    if not followers:
        print("📭 No followers yet")
        return

    headers = ["No", "Username", "Name", "Status"]
    data = []
    for i, user in enumerate(followers, 1):
        person = app.people[user]
        if user == app.current_user:
            data.append([i, user, person.name, ""])
        else:
            follow_status = app.get_follow_status(user)
            data.append([i, user, person.name, follow_status])

    print_table(headers, data)

    view_choice = get_input_with_retry(
        "* Select No of username to view profile (0 to go back): ",
        allow_zero=True
    )

    if view_choice is None:
        return

    try:
        idx = int(view_choice) - 1
        if 0 <= idx < len(followers):
            selected_user = followers[idx]

            if selected_user == app.current_user:
                print("👤 This is your own account")
                return view_followers_flow(app, target_user)

            show_profile_and_follow_options(app, selected_user)
            return view_followers_flow(app, target_user)

        else:
            print_error("❌ Invalid selection")
            return view_followers_flow(app, target_user)

    except ValueError:
        print_error("❌ Please enter a valid number")
        return view_followers_flow(app, target_user)

# =============================================================================
# SECTION 11: MENU DISPLAYS
# =============================================================================

def main_menu():
    """Display main menu"""
    print("\n" + "=" * 50)
    print("🌟 SOCIAL NETWORK SYSTEM 🌟")
    print("=" * 50)
    print("1. 🔐 Login")
    print("2. 📝 Register New User")
    print("3. ⚙️ Admin Login")
    print("4. 🚪 Exit System")
    print("=" * 50)


def user_menu(current_user_name, current_username):
    """Display user menu"""
    current_person = app.people[current_username]
    pending_count = len(current_person.pending_followers)

    print("\n" + "=" * 50)
    print(f"👤 USER MENU - @{current_username}")
    print("=" * 50)
    print(f"Name: {current_user_name} ")
    if not current_person.is_public and pending_count > 0:
        print(f"📭 Pending Requests: {pending_count}")
    print("1. 👀 Browse Users")
    print("2. ❤️ My Following")
    print("3. 👥 My Followers")
    if not current_person.is_public:
        print(f"4. 📭 Manage Follow Requests ({pending_count})")
    else:
        print("4. 💡 Recommended Users")
    print("5. 📊 View/Edit My Profile")
    print("6. 📝 Manage My Posts")
    print("7. 🔓 Logout")
    print("8. 🚪 Exit System")
    print("=" * 50)


def admin_menu():
    """Display admin menu"""
    print("\n" + "=" * 50)
    print("⚙️ ADMIN MENU")
    print("=" * 50)
    print("1. 📋 View All Users")
    print("2. 📊 View User Details")
    print("3. ↩️ Back to Main Menu")
    print("4. 🚪 Exit System")
    print("=" * 50)

# =============================================================================
# SECTION 12: FLOW CONTROLLERS (Login, register, admin flows)
# =============================================================================

def login_flow(app):
    """Handle user login flow"""
    username = get_input_with_retry("* Enter username (0 to go back): ")
    if username is None:
        return False

    password = get_input_with_retry("* Enter password (0 to go back): ")
    if password is None:
        return False

    success, message = app.login(username, password)
    if success:
        print_success(f"✅ {message}")
        return True
    else:
        print_error(f"❌ {message}")
        return False

def register_flow(app):
    """Handle new user registration flow"""
    print("\n🎯 REGISTER NEW USER")
    print("─" * 30)

    username = get_input_with_retry("* Enter username: ")
    if username is None:
        return

    if username in app.people:
        print_error("❌ Username already exists!")
        return

    password = get_input_with_retry("* Enter password: ")
    if password is None:
        return

    name = get_input_with_retry("* Enter name: ")
    if name is None:
        return

    print("* Select gender:")
    print("   1. 🚹 Male")
    print("   2. 🚺 Female")
    print("   3. ⚧️ Other")
    gender_choice = get_input_with_retry("* Enter your choice (1-3): ")
    if gender_choice is None:
        return

    if gender_choice == '1':
        gender = "🚹 Male"
    elif gender_choice == '2':
        gender = "🚺 Female"
    elif gender_choice == '3':
        gender = "⚧️ Other"
    else:
        print_error("❌ Invalid choice, using default: Male")
        gender = "🚹 Male"

    bio = get_input_with_retry("* Enter bio: ")
    if bio is None:
        return

    print("* Account type:")
    print("   1. 🌐 Public")
    print("   2. 🔒 Private")
    privacy = get_input_with_retry("* Enter your choice (1-2): ")
    if privacy is None:
        return

    is_public = privacy == '1'

    success, message = app.register_user(username, password, name, gender, bio, is_public)
    if success:
        print_success(f"✅ {message}")
    else:
        print_error(f"❌ {message}")

def admin_flow(app):
    """Handle admin login flow"""
    password = get_input_with_retry("* Enter admin password (0 to go back): ")
    if password is None:
        return False

    success, message = app.admin_login(password)
    if success:
        print_success(f"✅ {message}")
        return True
    else:
        print_error(f"❌ {message}")
        return False

# =============================================================================
# SECTION 13: USER FLOW CONTROLLERS
# =============================================================================

def user_browse_flow(app):
    """Handle user browsing flow"""
    all_users = app.get_all_users()
    filtered_users = display_user_selection(app, all_users, app.current_user)

    if not filtered_users:
        print("📭 No other users to browse")
        return

    user_choice = get_input_with_retry("\n* Select user number to view profile (0 to go back): ", allow_zero=True)
    if user_choice is None:
        return

    try:
        choice_idx = int(user_choice) - 1
        if 0 <= choice_idx < len(filtered_users):
            target_user = filtered_users[choice_idx]
            show_profile_and_follow_options(app, target_user)
        else:
            print_error("❌ Invalid selection")
    except ValueError:
        print_error("❌ Please enter a valid number")

def user_following_flow(app):
    """Handle viewing followed users"""
    print("\n❤️ MY FOLLOWING")
    following = app.get_following()
    if following:
        headers = ["No", "Username", "Name", "Status"]
        data = []
        for i, user in enumerate(following, 1):
            person = app.people[user]
            is_mutual = app.is_mutual_follow(app.current_user, user)
            mutual_status = "🤝 Mutual" if is_mutual else "✅ Following"
            data.append([i, user, person.name, mutual_status])

        print_table(headers, data)

        view_choice = get_input_with_retry("\n* Select No of username to view profile (0 to go back): ", allow_zero=True)
        if view_choice is None:
            return

        try:
            choice_idx = int(view_choice) - 1
            if 0 <= choice_idx < len(following):
                target_user = following[choice_idx]
                show_profile_and_follow_options(app, target_user)
            else:
                print_error("❌ Invalid selection")
        except ValueError:
            print_error("❌ Please enter a valid number")
    else:
        print("📭 Not following anyone yet")

def user_followers_flow(app):
    """Handle viewing followers"""
    print("\n👥 MY FOLLOWERS")
    followers = app.get_followers(app.current_user)
    if followers:
        headers = ["No", "Username", "Name", "Status"]
        data = []
        for i, user in enumerate(followers, 1):
            person = app.people[user]
            if user == app.current_user:
                # Don't show status for own account
                data.append([i, user, person.name, ""])
            else:
                follow_status = app.get_follow_status(user)
                data.append([i, user, person.name, follow_status])

        print_table(headers, data)

        view_choice = get_input_with_retry("\n* Select No of username to view profile (0 to go back): ", allow_zero=True)
        if view_choice is None:
            return

        try:
            choice_idx = int(view_choice) - 1
            if 0 <= choice_idx < len(followers):
                target_user = followers[choice_idx]
                if target_user == app.current_user:
                    print("👤 This is your own account")
                else:
                    show_profile_and_follow_options(app, target_user)
            else:
                print_error("❌ Invalid selection")
        except ValueError:
            print_error("❌ Please enter a valid number")
    else:
        print("📭 No followers yet")

def user_recommendations_flow(app):
    """Handle viewing recommended users"""
    print("\n💡 RECOMMENDED USERS")
    recommendations = app.get_recommendations()
    if recommendations:
        headers = ["No", "Username", "Name", "Type"]
        data = []
        for i, user in enumerate(recommendations, 1):
            person = app.people[user]
            account_type = '🌐 Public' if person.is_public else '🔒 Private'
            data.append([i, user, person.name, account_type])

        print_table(headers, data)

        view_choice = get_input_with_retry("\n* Select No of username to view profile (0 to go back): ", allow_zero=True)
        if view_choice is None:
            return

        try:
            choice_idx = int(view_choice) - 1
            if 0 <= choice_idx < len(recommendations):
                target_user = recommendations[choice_idx]
                show_profile_and_follow_options(app, target_user)
            else:
                print_error("❌ Invalid selection")
        except ValueError:
            print_error("❌ Please enter a valid number")
    else:
        print("📭 No recommended users")

# =============================================================================
# SECTION 14: ADMIN FLOW CONTROLLERS
# =============================================================================

def admin_view_user_details_flow(app):
    """Handle admin viewing user details"""
    users = display_all_users_detailed_table_with_posts(app)

    username_choice = get_input_with_retry("\n* Enter username to view details (0 to go back): ", allow_zero=True)
    if username_choice is None:
        return

    if username_choice in users:
        show_user_complete_details(app, username_choice)
    else:
        print_error("❌ Username not found")

def show_user_complete_details(app, username):
    """Display complete user details for admin"""
    person = app.people[username]
    followers_count = app.get_followers_count(username)
    following_count = app.get_following_count(username)
    posts_count = len(person.posts)

    print(f"\n{'=' * 60}")
    print(f"📊 USER DETAILS - @{username}")
    print(f"{'=' * 60}")
    print(f"👤 BASIC INFORMATION:")
    print(f"  Username: {username}")
    print(f"  Name: {person.name}")
    print(f"  Gender: {person.gender}")
    print(f"  Bio: {person.biography}")
    print(f"  Account Type: {'🌐 Public' if person.is_public else '🔒 Private'}")

    print(f"\n📊 STATISTICS:")
    print(f"  Followers: {followers_count}")
    print(f"  Following: {following_count}")
    print(f"  Posts: {posts_count}")

    print(f"\n📝 FOLLOW RELATIONS:")
    followers = app.get_followers(username)
    following = app.get_following(username)
    pending_requests = len(person.pending_followers)

    print(f"  Followers: {', '.join(followers) if followers else 'None'}")
    print(f"  Following: {', '.join(following) if following else 'None'}")
    print(f"  Pending Requests: {pending_requests}")

    print(f"\n📄 POSTS ({posts_count}):")
    if person.posts:
        for i, post in enumerate(person.posts[::-1], 1):
            time_str = post['timestamp'].strftime("%Y/%m/%d %H:%M")
            print(f"  {i}. [{time_str}] {post['content']}")
    else:
        print("  No posts yet")

    print(f"{'=' * 60}")

# =============================================================================
# SECTION 15: MAIN APPLICATION CONTROLLER
# =============================================================================

def main():
    """Main application controller"""
    global app
    app = SocialMediaApp()
    create_sample_data(app)
    is_admin_mode = False
    running = True

    while running:
        if not app.current_user and not is_admin_mode:
            # Main menu for logged out users
            main_menu()
            choice = get_input_with_retry("* Enter your choice (0 to Exit): ", allow_zero=True)

            if choice == '1':
                login_flow(app)
            elif choice == '2':
                register_flow(app)
            elif choice == '3':
                if admin_flow(app):
                    is_admin_mode = True
            elif choice == '4':
                print("👋 Thank you for using Social Network System!")
                break
            elif choice:
                print_error("❌ Invalid choice, please try again")

        elif is_admin_mode:
            # Admin menu
            admin_menu()
            choice = get_input_with_retry("* Enter your choice (0 to Exit): ", allow_zero=True)

            if choice == '1':
                display_all_users_table(app, True)
            elif choice == '2':
                admin_view_user_details_flow(app)
            elif choice == '3':
                is_admin_mode = False
            elif choice == '4':
                print("👋 Thank you for using Social Network System!")
                running = False
            elif choice:
                print_error("❌ Invalid choice, please try again")

        else:
            # User menu for logged in users
            current_user_name = app.people[app.current_user].name
            current_person = app.people[app.current_user]
            user_menu(current_user_name, app.current_user)
            choice = get_input_with_retry("* Enter your choice (0 to Exit): ", allow_zero=True)

            if choice == '1':
                user_browse_flow(app)
            elif choice == '2':
                user_following_flow(app)
            elif choice == '3':
                user_followers_flow(app)
            elif choice == '4':
                if not current_person.is_public:
                    manage_follow_requests_flow(app)
                else:
                    user_recommendations_flow(app)
            elif choice == '5':
                show_own_profile_options(app, app.current_user)
            elif choice == '6':
                manage_posts_flow(app)
            elif choice == '7':
                print_success(f"✅ {app.logout()}")
            elif choice == '8':
                print("👋 Thank you for using Social Network System!")
                running = False
            elif choice:
                print_error("❌ Invalid choice, please try again")

if __name__ == "__main__":
    main()
