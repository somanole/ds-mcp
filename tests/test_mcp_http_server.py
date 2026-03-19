from pathlib import Path

from mcp_servers import mcp_http_server


def test_read_local_file_returns_content(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("sample content", encoding="utf-8")

    assert mcp_http_server.read_local_file(str(file_path)) == "sample content"


def test_execute_python_code_requires_input():
    assert (
        mcp_http_server.execute_python_code()
        == "Error: No code or filename provided. Please provide the 'code' parameter."
    )


def test_execute_python_code_runs_inline_code(monkeypatch, tmp_path):
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()

    monkeypatch.setattr(mcp_http_server.os.path, "abspath", lambda _: str(scripts_dir))

    result = mcp_http_server.execute_python_code(code="print(2 + 3)")

    assert result == "Output:\n5\n"


def test_execute_python_code_runs_script_from_scripts_dir(monkeypatch, tmp_path):
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    script = scripts_dir / "hello.py"
    script.write_text("print('hello from script')", encoding="utf-8")

    monkeypatch.setattr(mcp_http_server.os.path, "abspath", lambda _: str(scripts_dir))

    result = mcp_http_server.execute_python_code(script_name="hello.py")

    assert result == "Output:\nhello from script\n"
