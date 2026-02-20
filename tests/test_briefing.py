import sys
import json
import pytest
from unittest.mock import Mock, patch

from vfinance_news.briefing import generate_and_send
LANG_FLAG = "--" + "lang"

def test_generate_and_send_success():
    # Mock subprocess.run for summarize.py
    mock_briefing_data = {
        "macro_message": "Macro Summary",
        "portfolio_message": "Portfolio Summary",
        "summary": "Full Summary"
    }
    
    with patch("vfinance_news.briefing.subprocess.run") as mock_run:
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps(mock_briefing_data)
        mock_run.return_value = mock_result
        
        args = Mock()
        args.style = "briefing"
        args.deadline = 300
        args.fast = False
        args.llm = False
        args.debug = False
        args.json = True
        
        result = generate_and_send(args)
        
        assert result == "Macro Summary"
        assert mock_run.called
        # Check if vfinance_news.summarize module was called with correct args
        call_args = mock_run.call_args[0][0]
        assert call_args[1] == "-m"
        assert call_args[2] == "vfinance_news.summarize"
        assert "--style" in call_args
        assert LANG_FLAG not in call_args

def test_generate_and_send_llm_forwards_only_llm_flag():
    mock_briefing_data = {
        "macro_message": "Macro Summary",
        "portfolio_message": ""
    }

    with patch("vfinance_news.briefing.subprocess.run") as mock_run:
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps(mock_briefing_data)
        mock_run.return_value = mock_result

        args = Mock()
        args.style = "briefing"
        args.deadline = None
        args.fast = False
        args.llm = True
        args.debug = False
        args.json = True

        generate_and_send(args)

        call_args = mock_run.call_args[0][0]
        assert "--llm" in call_args
        assert "--model" not in call_args


def test_generate_and_send_failure():
    with patch("vfinance_news.briefing.subprocess.run") as mock_run:
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Error occurred"
        mock_run.return_value = mock_result
        
        args = Mock()
        args.style = "briefing"
        args.deadline = None
        args.fast = False
        args.llm = False
        args.json = False
        args.debug = False
        
        with pytest.raises(SystemExit):
            generate_and_send(args)


def test_briefing_cli_rejects_model_flag(monkeypatch):
    from vfinance_news import briefing

    monkeypatch.setattr("sys.argv", ["vfinance-news briefing", "--llm", "--model", "minimax"])
    with pytest.raises(SystemExit):
        briefing.main()


def test_briefing_cli_rejects_send_flag(monkeypatch):
    from vfinance_news import briefing

    monkeypatch.setattr("sys.argv", ["vfinance-news briefing", "--send"])
    with pytest.raises(SystemExit):
        briefing.main()


def test_briefing_cli_rejects_group_flag(monkeypatch):
    from vfinance_news import briefing

    monkeypatch.setattr("sys.argv", ["vfinance-news briefing", "--group", "my-target"])
    with pytest.raises(SystemExit):
        briefing.main()


def test_briefing_cli_rejects_lang_flag(monkeypatch):
    from vfinance_news import briefing

    monkeypatch.setattr("sys.argv", ["vfinance-news briefing", LANG_FLAG, "de"])
    with pytest.raises(SystemExit):
        briefing.main()
