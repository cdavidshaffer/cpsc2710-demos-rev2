from issue_tracker.issue import Issue, Priority, Status


def get_samples():
    return [
        Issue(
            "Login page crashes on empty password",
            Status.NEW,
            Priority.URGENT,
            "Alice",
            "Users see a traceback when submitting a blank password field.",
        ),
        Issue(
            "Dashboard loads slowly with large datasets",
            Status.IN_PROGRESS,
            Priority.HIGH,
            "Bob",
            "Page takes over 10 seconds when the user has more than 500 records.",
        ),
        Issue(
            "Typo on the About page",
            Status.NEW,
            Priority.LOW,
            "Carol",
            "The word 'recieve' should be 'receive'.",
        ),
        Issue(
            "Email notifications not sent for new comments",
            Status.IN_PROGRESS,
            Priority.HIGH,
            "Dave",
            "Notification emails stopped going out after the last deploy.",
        ),
        Issue(
            "Search returns duplicate results",
            Status.NEW,
            Priority.MEDIUM,
            "Eve",
            "Searching by keyword sometimes shows the same item twice.",
        ),
        Issue(
            "Dark mode toggle does not persist",
            Status.CLOSED,
            Priority.MEDIUM,
            "Frank",
            "Refreshing the page resets the theme to light mode. Fixed in v2.3.",
        ),
        Issue(
            "CSV export missing header row",
            Status.NEW,
            Priority.HIGH,
            "Alice",
            "Exported CSV files have no column headers.",
        ),
        Issue(
            "Mobile layout overlaps on small screens",
            Status.IN_PROGRESS,
            Priority.MEDIUM,
            "Grace",
            "Buttons overlap the navigation bar on screens under 360px wide.",
        ),
        Issue(
            "Add bulk-delete option for archived items",
            Status.NEW,
            Priority.LOW,
            "Bob",
            "Feature request: let admins delete archived items in batch.",
        ),
        Issue(
            "API rate limiter blocks legitimate users",
            Status.IN_PROGRESS,
            Priority.URGENT,
            "Dave",
            "The 100 req/min limit is too aggressive for power users.",
        ),
        Issue(
            "Unit tests fail on Windows due to path separators",
            Status.CLOSED,
            Priority.MEDIUM,
            "Carol",
            "Replaced hardcoded '/' with os.path.join. Resolved.",
        ),
        Issue(
            "Profile picture upload accepts invalid formats",
            Status.NEW,
            Priority.LOW,
            "Eve",
            "Users can upload .bmp files but the viewer only supports PNG and JPEG.",
        ),
    ]
