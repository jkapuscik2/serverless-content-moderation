REJECTED_CATEGORIES = [
    "Explicit Nudity",
    "Violence",
    "Visually Disturbing"
]


def has_unsafe_label(labels):
    for label in labels:
        if label["Name"] in REJECTED_CATEGORIES:
            return True
    return False
