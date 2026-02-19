"""Smoke tests for the Python CLI entrypoint."""

import pytest

from finance_news import cli


def test_finance_news_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["finance-news", "--help"])
    with pytest.raises(SystemExit):
        cli.main()
    out = capsys.readouterr().out
    assert "Finance News CLI" in out
    assert "briefing" in out


def test_finance_news_briefing_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["finance-news", "briefing", "--help"])
    with pytest.raises(SystemExit):
        cli.main()
    out = capsys.readouterr().out
    assert "--morning" in out
    assert "--evening" in out


def test_finance_news_setup_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["finance-news", "setup", "--help"])
    with pytest.raises(SystemExit):
        cli.main()
    out = capsys.readouterr().out
    assert "usage:" in out
