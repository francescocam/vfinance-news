"""Smoke tests for the Python CLI entrypoint."""

import sys
import types

import pytest

from vfinance_news import cli


def test_vfinance_news_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["vfinance-news", "--help"])
    with pytest.raises(SystemExit):
        cli.main()
    out = capsys.readouterr().out
    assert "vfinance-news CLI" in out
    assert "briefing" in out


def test_vfinance_news_briefing_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["vfinance-news", "briefing", "--help"])
    with pytest.raises(SystemExit):
        cli.main()
    out = capsys.readouterr().out
    assert "usage: vfinance-news briefing" in out


def test_vfinance_news_setup_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["vfinance-news", "setup", "--help"])
    with pytest.raises(SystemExit):
        cli.main()
    out = capsys.readouterr().out
    assert "usage:" in out
    assert "delivery" not in out


def test_vfinance_news_portfolio_add_routes_to_portfolio_manager(monkeypatch):
    captured: dict[str, list[str] | None] = {"argv": None}

    def fake_portfolio_main():
        captured["argv"] = list(sys.argv)

    fake_module = types.SimpleNamespace(main=fake_portfolio_main)
    monkeypatch.setitem(sys.modules, "vfinance_news.portfolio", fake_module)
    import vfinance_news
    monkeypatch.setattr(vfinance_news, "portfolio", fake_module, raising=False)
    monkeypatch.setattr("sys.argv", ["vfinance-news", "portfolio", "add", "CSU.TO"])

    cli.main()

    assert captured["argv"] == ["vfinance-news portfolio", "add", "CSU.TO"]


def test_vfinance_news_portfolio_routes_to_news_fetcher(monkeypatch):
    called = {"fetch_news": False}

    def fake_fetch_news_main():
        called["fetch_news"] = True

    fake_module = types.SimpleNamespace(main=fake_fetch_news_main)
    monkeypatch.setitem(sys.modules, "vfinance_news.fetch_news", fake_module)
    import vfinance_news
    monkeypatch.setattr(vfinance_news, "fetch_news", fake_module, raising=False)
    monkeypatch.setattr("sys.argv", ["vfinance-news", "portfolio"])

    cli.main()

    assert called["fetch_news"] is True


def test_vfinance_news_legacy_portfolio_alias_rejected(monkeypatch):
    monkeypatch.setattr("sys.argv", ["vfinance-news", "portfolio-add", "NVDA"])
    with pytest.raises(SystemExit):
        cli.main()
