import pytest
from unittest.mock import patch, MagicMock
from yacamim.client import GeminiClient


@pytest.fixture
def client():
    return GeminiClient()


def test_absolutise_url(client):
    assert (
        client.absolutise_url("gemini://example.com/", "page")
        == "gemini://example.com/page"
    )
    assert (
        client.absolutise_url("gemini://example.com/dir/", "/page")
        == "gemini://example.com/page"
    )
    assert (
        client.absolutise_url(
            "gemini://example.com/", "gemini://other.com/page"
        )
        == "gemini://other.com/page"
    )


def test_get_url(client):
    client.menu = ["gemini://example.com"]
    assert client.get_url("1") == "gemini://example.com"
    assert client.get_url("gemini://example.com") == "gemini://example.com"
    assert client.get_url("example.com") == "gemini://example.com"


@patch("socket.create_connection")
@patch("ssl.create_default_context")
def test_create_ssl_socket(
    mock_create_context, mock_create_connection, client
):
    mock_socket = MagicMock()
    mock_create_connection.return_value = mock_socket
    mock_context = MagicMock()
    mock_create_context.return_value = mock_context

    parsed_url = MagicMock()
    parsed_url.netloc = "example.com"
    client.create_ssl_socket(parsed_url)

    mock_create_connection.assert_called_once_with(("example.com", 1965))
    mock_context.wrap_socket.assert_called_once_with(
        mock_socket, server_hostname="example.com"
    )


def test_send_request(client):
    mock_socket = MagicMock()
    url = "gemini://example.com"
    client.send_request(mock_socket, url)
    mock_socket.sendall.assert_called_once_with(b"gemini://example.com\r\n")


@patch("builtins.input", return_value="query")
def test_handle_input_request(mock_input, client):
    result = client.handle_input_request("text/plain", "gemini://example.com")
    assert result == "gemini://example.com?query"


def test_handle_redirect(client):
    assert (
        client.handle_redirect("gemini://example.com/old", "/new")
        == "gemini://example.com/new"
    )


def test_handle_gemini_link(client, capsys):
    client.handle_gemini_link("=> /page Page Title", "gemini://example.com")
    captured = capsys.readouterr()
    assert captured.out == "[1] Page Title\n"
    assert client.menu == ["gemini://example.com/page"]


@patch("builtins.input", side_effect=["1", "b", "q"])
def test_handle_user_input(mock_input, client):
    client.menu = ["gemini://example.com"]
    client.hist = ["gemini://history.com"]

    assert client.handle_user_input() == "gemini://example.com"
    assert client.handle_user_input() == "gemini://history.com"
    assert client.handle_user_input() is None


@patch("yacamim.main.GeminiClient.create_ssl_socket")
@patch("yacamim.main.GeminiClient.send_request")
@patch("yacamim.main.GeminiClient.process_gemini_response")
def test_gemini_transaction(
    mock_process_response, mock_send_request, mock_create_socket, client
):
    mock_socket = MagicMock()
    mock_create_socket.return_value.__enter__.return_value = mock_socket
    mock_fp = MagicMock()
    mock_fp.readline.return_value = b"20 text/gemini\r\n"
    mock_send_request.return_value = mock_fp

    result = client.gemini_transaction("gemini://example.com")

    assert result == "gemini://example.com"
    mock_create_socket.assert_called_once()
    mock_send_request.assert_called_once_with(
        mock_socket, "gemini://example.com"
    )
    mock_process_response.assert_called_once()


if __name__ == "__main__":
    pytest.main()
