from datetime import datetime
from collections import defaultdict

# ============================================================================
# 1. DATA STRUCTURES - Initialize the library system
# ============================================================================

# Global dictionaries to store data
books = {}  # {book_id: {'title', 'author', 'genre', 'availability'}}
members = {}  # {member_id: {'name', 'age', 'contact'}}
borrow_log = []  # List of borrowing transactions
member_borrowed_books = {}  # {member_id: [list of book_ids]}

# For auto-generating IDs
next_book_id = 1001
next_member_id = 20013


# ============================================================================
# 2. BOOK MANAGEMENT FUNCTIONS
# ============================================================================

################################################
def add_book(title, author, genre):
    """
    Add a new book to the library.    
    Args:
        title (str): Book title
        author (str): Author name
        genre (str): Book genre    
    Returns:
        int: Book ID of the newly added book
    """
    global next_book_id
    book_id = next_book_id
    books[book_id] = {
        'title': title,
        'author': author,
        'genre': genre,
        'availability': 'Available'
    }
    next_book_id += 1
    print(f"✓ Book added successfully! Book ID: {book_id}")
    return book_id
###################################################################

def search_book_by_title(title):
    """
    Search for books by title   
    Args:
        title (str): Title or partial title to search    
    Returns:
        list: List of tuples (book_id, book_info)
    """
    results = []
    title_lower = title.lower()
    for book_id, book in books.items():
        if title_lower in book['title'].lower():
            results.append((book_id, book))
    return results

###################################################################
def search_book_by_author(author):
    """
    Search for books by author (case-insensitive).
    
    Args:
        author (str): Author name or partial name to search
    
    Returns:
        list: List of tuples (book_id, book_info)
    """
    results = []
    author_lower = author.lower()
    for book_id, book in books.items():
        if author_lower in book['author'].lower():
            results.append((book_id, book))
    return results


def update_book_availability(book_id, status):
    """
    Update book availability status.
    
    Args:
        book_id (int): Book ID
        status (str): 'Available' or 'Issued'
    
    Returns:
        bool: True if update successful, False otherwise
    """
    if book_id not in books:
        print(f"✗ Book ID {book_id} not found!")
        return False
    books[book_id]['availability'] = status
    return True


def display_all_books():
    """Display all books in the library in a formatted table."""
    if not books:
        print("No books in the library yet.")
        return
    
    print("\n" + "="*80)
    print(f"{'Book ID':<12} {'Title':<30} {'Author':<20} {'Genre':<12} {'Status':<10}")
    print("="*80)
    for book_id, book in sorted(books.items()):
        print(f"{book_id:<12} {book['title']:<30} {book['author']:<20} {book['genre']:<12} {book['availability']:<10}")
    print("="*80)


# ============================================================================
# 3. MEMBER MANAGEMENT FUNCTIONS
# ============================================================================

def add_member(name, age, contact):
    """
    Add a new member to the library.
    
    Args:
        name (str): Member name
        age (int): Member age
        contact (str): Contact information (email/phone)
    
    Returns:
        int: Member ID of the newly added member
    """
    global next_member_id
    member_id = next_member_id
    members[member_id] = {
        'name': name,
        'age': age,
        'contact': contact
    }
    member_borrowed_books[member_id] = []
    next_member_id += 1
    print(f"✓ Member added successfully! Member ID: {member_id}")
    return member_id


def search_member_by_name(name):
    """
    Search for members by name (case-insensitive).
    
    Args:
        name (str): Member name or partial name to search
    
    Returns:
        list: List of tuples (member_id, member_info)
    """
    results = []
    name_lower = name.lower()
    for member_id, member in members.items():
        if name_lower in member['name'].lower():
            results.append((member_id, member))
    return results


def get_member_info(member_id):
    """
    Get information about a specific member.
    
    Args:
        member_id (int): Member ID
    
    Returns:
        dict: Member information or None if not found
    """
    if member_id not in members:
        print(f"✗ Member ID {member_id} not found!")
        return None
    return members[member_id]


def display_all_members():
    """Display all registered members in a formatted table."""
    if not members:
        print("No members registered yet.")
        return
    
    print("\n" + "="*70)
    print(f"{'Member ID':<12} {'Name':<20} {'Age':<8} {'Contact':<25}")
    print("="*70)
    for member_id, member in sorted(members.items()):
        print(f"{member_id:<12} {member['name']:<20} {member['age']:<8} {member['contact']:<25}")
    print("="*70)


# ============================================================================
# 4. BORROW & RETURN SYSTEM
# ============================================================================

def borrow_book(member_id, book_id):
    """
    Member borrows a book from the library.
    
    Conditions:
    - Member must exist
    - Book must exist
    - Book must be available (not already borrowed)
    
    Args:
        member_id (int): Member ID
        book_id (int): Book ID
    
    Returns:
        bool: True if borrowing successful, False otherwise
    """
    # Validate member
    if member_id not in members:
        print(f"✗ Member ID {member_id} not found!")
        return False
    
    # Validate book
    if book_id not in books:
        print(f"✗ Book ID {book_id} not found!")
        return False
    
    # Check if book is available
    if books[book_id]['availability'] != 'Available':
        print(f"✗ Book '{books[book_id]['title']}' is not available (already issued)!")
        return False
    
    # Process borrow
    books[book_id]['availability'] = 'Issued'
    member_borrowed_books[member_id].append(book_id)
    
    # Record transaction
    borrow_log.append({
        'member_id': member_id,
        'book_id': book_id,
        'action': 'Borrowed',
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    print(f"✓ Book '{books[book_id]['title']}' successfully borrowed by {members[member_id]['name']}")
    return True


def return_book(member_id, book_id):
    """
    Member returns a borrowed book to the library.
    
    Conditions:
    - Member must exist
    - Book must exist
    - Member must have borrowed this book
    
    Args:
        member_id (int): Member ID
        book_id (int): Book ID
    
    Returns:
        bool: True if return successful, False otherwise
    """
    # Validate member
    if member_id not in members:
        print(f"✗ Member ID {member_id} not found!")
        return False
    
    # Validate book
    if book_id not in books:
        print(f"✗ Book ID {book_id} not found!")
        return False
    
    # Check if member actually borrowed this book
    if book_id not in member_borrowed_books[member_id]:
        print(f"✗ {members[member_id]['name']} did not borrow '{books[book_id]['title']}'!")
        return False
    
    # Process return
    books[book_id]['availability'] = 'Available'
    member_borrowed_books[member_id].remove(book_id)
    
    # Record transaction
    borrow_log.append({
        'member_id': member_id,
        'book_id': book_id,
        'action': 'Returned',
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    print(f"✓ Book '{books[book_id]['title']}' successfully returned by {members[member_id]['name']}")
    return True


def display_borrow_log():
    """Display the complete transaction log."""
    if not borrow_log:
        print("No transactions yet.")
        return
    
    print("\n" + "="*100)
    print(f"{'Date/Time':<20} {'Member ID':<12} {'Book ID':<12} {'Action':<12} {'Member Name':<20} {'Book Title':<30}")
    print("="*100)
    for log in borrow_log:
        member_name = members[log['member_id']]['name']
        book_title = books[log['book_id']]['title']
        print(f"{log['date']:<20} {log['member_id']:<12} {log['book_id']:<12} {log['action']:<12} {member_name:<20} {book_title:<30}")
    print("="*100)


# ============================================================================
# 5. REPORTS & QUERIES
# ============================================================================

def get_available_books_by_genre(genre):
    """
    Show all available books in a given genre.
    
    Args:
        genre (str): Genre name
    """
    results = get_books_by_genre(genre)
    if not results:
        print(f"No available books found in genre: {genre}")
        return
    
    print(f"\n{'='*70}")
    print(f"Available Books in Genre: {genre}")
    print(f"{'='*70}")
    print(f"{'Book ID':<12} {'Title':<30} {'Author':<20}")
    print(f"{'='*70}")
    for book_id, book in results:
        print(f"{book_id:<12} {book['title']:<30} {book['author']:<20}")
    print(f"{'='*70}")


def get_members_who_borrowed():
    """List of members who have borrowed at least one book."""
    members_borrowed = set()
    for member_id in member_borrowed_books:
        if member_borrowed_books[member_id]:  # If member has borrowed books
            members_borrowed.add(member_id)
    
    if not members_borrowed:
        print("No members have borrowed books yet.")
        return
    
    print(f"\n{'='*70}")
    print(f"Members Who Have Borrowed Books")
    print(f"{'='*70}")
    print(f"{'Member ID':<12} {'Name':<25} {'Books Borrowed':<20}")
    print(f"{'='*70}")
    for member_id in sorted(members_borrowed):
        num_books = len(member_borrowed_books[member_id])
        print(f"{member_id:<12} {members[member_id]['name']:<25} {num_books:<20}")
    print(f"{'='*70}")


def search_book(query):
    """
    Search for a book by title or author.
    
    Args:
        query (str): Search query
    """
    print(f"\nSearching for: '{query}'")
    
    # Search by title
    title_results = search_book_by_title(query)
    # Search by author
    author_results = search_book_by_author(query)
    
    all_results = set()
    for book_id, _ in title_results + author_results:
        all_results.add(book_id)
    
    if not all_results:
        print(f"No books found matching '{query}'")
        return
    
    print(f"\n{'='*80}")
    print(f"Search Results for: '{query}'")
    print(f"{'='*80}")
    print(f"{'Book ID':<12} {'Title':<30} {'Author':<20} {'Genre':<12} {'Status':<10}")
    print(f"{'='*80}")
    for book_id in sorted(all_results):
        book = books[book_id]
        print(f"{book_id:<12} {book['title']:<30} {book['author']:<20} {book['genre']:<12} {book['availability']:<10}")
    print(f"{'='*80}")


def get_member_borrowed_history(member_id):
    """
    Show books borrowed by a specific member.
    
    Args:
        member_id (int): Member ID
    """
    if member_id not in members:
        print(f"✗ Member ID {member_id} not found!")
        return
    
    borrowed = member_borrowed_books.get(member_id, [])
    
    print(f"\n{'='*70}")
    print(f"Borrowed Books by {members[member_id]['name']}")
    print(f"{'='*70}")
    
    if not borrowed:
        print("No books currently borrowed.")
    else:
        print(f"{'Book ID':<12} {'Title':<30} {'Author':<20}")
        print(f"{'-'*70}")
        for book_id in borrowed:
            book = books[book_id]
            print(f"{book_id:<12} {book['title']:<30} {book['author']:<20}")
    print(f"{'='*70}")


# ============================================================================
# 6. MAIN MENU & USER INTERACTION
# ============================================================================

def display_menu():
    """Display the main menu options."""
    print("\n" + "="*60)
    print("LIBRARY MANAGEMENT SYSTEM - MAIN MENU")
    print("="*60)
    print("1. Add Book")
    print("2. Add Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Search Book (by title or author)")
    print("6. View Books by Genre")
    print("7. View All Books")
    print("8. View All Members")
    print("9. View Members Who Borrowed Books")
    print("10. View Member Borrowed History")
    print("11. View Transaction Log")
    print("12. Exit")
    print("="*60)


def main_menu():
    """Main menu loop for user interaction."""
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-13): ").strip()
        
        if choice == '1':  # Add Book            
            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()
            genre = input("Enter genre: ").strip()
            if title and author and genre:
                add_book(title, author, genre)
            else:
                print("✗ Please fill in all fields!")
        
        elif choice == '2':# Add Member            
            name = input("Enter member name: ").strip()
            try:
                age = int(input("Enter member age: ").strip())
                contact = input("Enter contact info (email/phone): ").strip()
                if name and age > 0 and contact:
                    add_member(name, age, contact)
                else:
                    print("✗ Please fill in all fields correctly!")
            except ValueError:
                print("✗ Age must be a valid number!")
        
        elif choice == '3':
            # Borrow Book
            try:
                member_id = int(input("Enter member ID: ").strip())
                book_id = int(input("Enter book ID: ").strip())
                borrow_book(member_id, book_id)
            except ValueError:
                print("✗ Please enter valid member ID and book ID!")
        
        elif choice == '4':
            # Return Book
            try:
                member_id = int(input("Enter member ID: ").strip())
                book_id = int(input("Enter book ID: ").strip())
                return_book(member_id, book_id)
            except ValueError:
                print("✗ Please enter valid member ID and book ID!")
        
        elif choice == '5':
            # Search Book
            query = input("Enter book title or author name to search: ").strip()
            if query:
                search_book(query)
            else:
                print("✗ Please enter a search query!")
        
        elif choice == '6':
            # View Books by Genre
            genre = input("Enter genre name: ").strip()
            if genre:
                get_available_books_by_genre(genre)
            else:
                print("✗ Please enter a genre name!")
        
        elif choice == '7':
            # View All Books
            display_all_books()
        
        elif choice == '8':
            # View All Members
            display_all_members()
        
        elif choice == '9':
            # View Members Who Borrowed Books
            get_members_who_borrowed()
        
        elif choice == '10':
            # View Member Borrowed History
            try:
                member_id = int(input("Enter member ID: ").strip())
                get_member_borrowed_history(member_id)
            except ValueError:
                print("✗ Please enter a valid member ID!")       
        
        
        elif choice == '11':
            # View Transaction Log
            display_borrow_log()
        
        elif choice == '12':
            # Exit
            print("\n✓ Thank you for using Library Management System! Goodbye!")
            break
        
        else:
            print("✗ Invalid choice! Please enter a number between 1 and 13.")
        
        # Pause and wait for user to acknowledge before showing menu again
        if choice != '12':
            input("\nPress Enter to continue and return to menu...")


# ============================================================================
# 7. ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("\nLibrary Management System")
    print("1. Run Demo (with sample data)")
    print("2. Interactive Menu")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == '1':
        run_demo()
    elif choice == '2':
        main_menu()
    else:
        print("Invalid choice!")
