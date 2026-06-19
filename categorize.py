def categorize_email(subject, sender):
    subject = subject.lower()
    sender = sender.lower()

    if any(keyword in subject for keyword in ['interview', 'job', 'opening']):
        return 'Job'
    elif any(keyword in subject for keyword in ['invoice', 'payment', 'due']):
        return 'Bills'
    elif any(keyword in subject for keyword in ['congratulations', 'you won']):
        return 'Spam'
    elif any(keyword in subject for keyword in ['amazon', 'flipkart', 'order']):
        return 'Orders'
    else:
        return 'Others'


def build_summary(categorized_list):
    from collections import Counter

    counts = Counter(categorized_list)
    category_emojis = {
        'Job': '',
        'Bills': '',
        'Spam': '',
        'Orders': '',
        'Others': ''
    }

    lines = [f"You have {len(categorized_list)} unread emails:"]
    for category, count in counts.items():
        emoji = category_emojis.get(category, '')
        lines.append(f"• {emoji} {count} {category} mail{'s' if count > 1 else ''}")

    return '\n'.join(lines)
