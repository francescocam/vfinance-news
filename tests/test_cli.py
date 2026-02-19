"""Smoke tests for the Python CLI entrypoint."""

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
    assert "--morning" in out
    assert "--evening" in out


def test_vfinance_news_setup_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["vfinance-news", "setup", "--help"])
    with pytest.raises(SystemExit):
        cli.main()
    out = capsys.readouterr().out
    assert "usage:" in out
