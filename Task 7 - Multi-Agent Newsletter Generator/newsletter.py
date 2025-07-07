NEWSLETTER_FOOTER = (
    "_Curated automatically by LangNewsAgent._\n"
    "Feedback? Reply to this group or email feedback@example.com\n"
    "To unsubscribe, remove yourself from this Telegram group."
)

def compose_newsletter(date_str, summaries):
    header = (
        f"📰 *Web3 Daily Newsletter*\n"
        f"_Date: {date_str}_\n"
        f"Top Stories from CoinDesk, CoinTelegraph, Decrypt, Bankless\n\n"
    )
    body = ""
    for idx, art in enumerate(summaries, 1):
        body += (
            f"*{idx}. {art.title}* [{art.source}]\n"
            f"{art.summary}\n"
            f"[Read more]({art.url})\n\n"
        )
    return header + body + NEWSLETTER_FOOTER