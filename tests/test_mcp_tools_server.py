from pathlib import Path

from mcp_servers import mcp_tools_server


def test_read_local_file_returns_content(tmp_path):
    file_path = tmp_path / "example.txt"
    file_path.write_text("hello from tests", encoding="utf-8")

    assert mcp_tools_server.read_local_file(str(file_path)) == "hello from tests"


def test_read_local_file_missing_file_returns_error(tmp_path):
    missing = tmp_path / "missing.txt"

    result = mcp_tools_server.read_local_file(str(missing))

    assert result == f"Error: File at {missing} not found."


def test_search_web_formats_results_with_separator(monkeypatch):
    class FakeDDGS:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def text(self, query, max_results):
            assert query == "model context protocol"
            assert max_results == 3
            return [
                {"body": "First result"},
                {"body": "Second result"},
            ]

    monkeypatch.setattr(mcp_tools_server, "DDGS", FakeDDGS)

    assert mcp_tools_server.search_web("model context protocol") == "First result\n---\nSecond result"


def test_search_web_handles_empty_result_set(monkeypatch):
    class EmptyDDGS:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def text(self, query, max_results):
            return []

    monkeypatch.setattr(mcp_tools_server, "DDGS", EmptyDDGS)

    assert mcp_tools_server.search_web("no hits") == "No results found."
