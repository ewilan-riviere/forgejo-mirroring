import pytest
from forgejo_mirroring.app import main


def test_main_runs(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Vérifie que la fonction main() s'exécute sans erreur
    et imprime le message attendu.
    """
    main()
    captured = capsys.readouterr()
    assert "Forgejo Mirroring app started!" in captured.out
