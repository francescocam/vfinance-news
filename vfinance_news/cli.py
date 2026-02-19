"""Python CLI entrypoint for vfinance-news."""

import argparse
import sys

def _news_command(symbol: str) -> int:
    from vfinance_news import fetch_news

    articles = fetch_news.fetch_ticker_news(symbol, 10)
    print(f"\n📰 News for {symbol}\n")
    for article in articles:
        print(f"• {article['title']}")
        print(f"  {article['link']}\n")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="vfinance-news CLI")
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

    return parser


PORTFOLIO_MANAGER_SUBCOMMANDS = {"list", "add", "remove", "import", "create", "symbols"}


def main() -> None:
    parser = _build_parser()
    args, remaining = parser.parse_known_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "setup":
        from vfinance_news import setup

        sys.argv = ["vfinance-news setup"] + ["wizard"] + remaining
        setup.main()
        return
    if args.command == "config":
        from vfinance_news import setup

        sys.argv = ["vfinance-news config", "show"] + remaining
        setup.main()
        return

    if args.command == "briefing":
        from vfinance_news import briefing

        forwarded = list(remaining)
        if args.morning and "--time" not in forwarded:
            forwarded = ["--time", "morning"] + forwarded
        if args.evening and "--time" not in forwarded:
            forwarded = ["--time", "evening"] + forwarded
        sys.argv = ["vfinance-news briefing"] + forwarded
        briefing.main()
        return

    if args.command == "market":
        from vfinance_news import fetch_news

        sys.argv = ["vfinance-news market", "market"] + remaining
        fetch_news.main()
        return
    if args.command == "portfolio":
        # Route explicit portfolio management subcommands.
        if remaining and remaining[0] in PORTFOLIO_MANAGER_SUBCOMMANDS:
            from vfinance_news import portfolio

            sys.argv = ["vfinance-news portfolio"] + remaining
            portfolio.main()
            return

        from vfinance_news import fetch_news

        sys.argv = ["vfinance-news portfolio", "portfolio"] + remaining
        fetch_news.main()
        return
    if args.command == "portfolio-only":
        from vfinance_news import fetch_news

        sys.argv = ["vfinance-news portfolio-only", "portfolio-only"] + remaining
        fetch_news.main()
        return
    if args.command == "news":
        _news_command(args.symbol)
        return

    if args.command == "alerts":
        from vfinance_news import alerts

        sys.argv = ["vfinance-news alerts"] + remaining
        alerts.main()
        return
    if args.command == "earnings":
        from vfinance_news import earnings

        sys.argv = ["vfinance-news earnings"] + remaining
        earnings.main()
        return

    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
