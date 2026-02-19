"""Python CLI entrypoint for finance-news."""

import argparse
import sys

def _news_command(symbol: str) -> int:
    from finance_news import fetch_news

    articles = fetch_news.fetch_ticker_news(symbol, 10)
    print(f"\n📰 News for {symbol}\n")
    for article in articles:
        print(f"• {article['title']}")
        print(f"  {article['link']}\n")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Finance News CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("setup", help="Interactive setup wizard")
    subparsers.add_parser("config", help="Show current configuration")

    briefing_parser = subparsers.add_parser("briefing", help="Generate market briefing")
    briefing_parser.add_argument("--morning", action="store_true", help="Shortcut for --time morning")
    briefing_parser.add_argument("--evening", action="store_true", help="Shortcut for --time evening")

    subparsers.add_parser("market", help="Market overview")
    subparsers.add_parser("portfolio", help="News for portfolio stocks")
    subparsers.add_parser("portfolio-only", help="Top gainers/losers from portfolio")

    news_parser = subparsers.add_parser("news", help="News for specific ticker")
    news_parser.add_argument("symbol", help="Ticker symbol")

    subparsers.add_parser("alerts", help="Price target alerts")
    subparsers.add_parser("earnings", help="Earnings calendar")

    subparsers.add_parser("portfolio-list", help="List portfolio stocks")
    subparsers.add_parser("portfolio-add", help="Add stock to portfolio")
    subparsers.add_parser("portfolio-remove", help="Remove stock from portfolio")
    subparsers.add_parser("portfolio-import", help="Import portfolio from CSV")
    subparsers.add_parser("portfolio-create", help="Interactive portfolio creation")

    return parser


def main() -> None:
    parser = _build_parser()
    args, remaining = parser.parse_known_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "setup":
        from finance_news import setup

        sys.argv = ["finance-news setup"] + ["wizard"] + remaining
        setup.main()
        return
    if args.command == "config":
        from finance_news import setup

        sys.argv = ["finance-news config", "show"] + remaining
        setup.main()
        return

    if args.command == "briefing":
        from finance_news import briefing

        forwarded = list(remaining)
        if args.morning and "--time" not in forwarded:
            forwarded = ["--time", "morning"] + forwarded
        if args.evening and "--time" not in forwarded:
            forwarded = ["--time", "evening"] + forwarded
        sys.argv = ["finance-news briefing"] + forwarded
        briefing.main()
        return

    if args.command == "market":
        from finance_news import fetch_news

        sys.argv = ["finance-news market", "market"] + remaining
        fetch_news.main()
        return
    if args.command == "portfolio":
        from finance_news import fetch_news

        sys.argv = ["finance-news portfolio", "portfolio"] + remaining
        fetch_news.main()
        return
    if args.command == "portfolio-only":
        from finance_news import fetch_news

        sys.argv = ["finance-news portfolio-only", "portfolio-only"] + remaining
        fetch_news.main()
        return
    if args.command == "news":
        _news_command(args.symbol)
        return

    if args.command == "alerts":
        from finance_news import alerts

        sys.argv = ["finance-news alerts"] + remaining
        alerts.main()
        return
    if args.command == "earnings":
        from finance_news import earnings

        sys.argv = ["finance-news earnings"] + remaining
        earnings.main()
        return

    if args.command == "portfolio-list":
        from finance_news import portfolio

        sys.argv = ["finance-news portfolio-list", "list"] + remaining
        portfolio.main()
        return
    if args.command == "portfolio-add":
        from finance_news import portfolio

        sys.argv = ["finance-news portfolio-add", "add"] + remaining
        portfolio.main()
        return
    if args.command == "portfolio-remove":
        from finance_news import portfolio

        sys.argv = ["finance-news portfolio-remove", "remove"] + remaining
        portfolio.main()
        return
    if args.command == "portfolio-import":
        from finance_news import portfolio

        sys.argv = ["finance-news portfolio-import", "import"] + remaining
        portfolio.main()
        return
    if args.command == "portfolio-create":
        from finance_news import portfolio

        sys.argv = ["finance-news portfolio-create", "create"] + remaining
        portfolio.main()
        return

    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
