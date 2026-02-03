import pathlib

from PIL import Image

from unittest import mock
import tempfile
import pytest

from p import main, parse_args, rasterize


@pytest.mark.parametrize(
    'argv, error', (
        ('-m median', True),
        ('f.png -aaa', False),
        ('-m const -t 256 f.png', True),
        ('-m const -t 128 f.png', False),
        ('--thresh median f.png', True),
        ('--inv f.png', False),
        ('-m percentile -t 128 f.pn', True),
        ('-m local f.png', False),
        ('-m local -t fya f.png', True),
        ('--fit f.png', False),
        ('-z 2 -x f.png', True),
        ('-z -1.2 f.png', True),
        ('-z fya f.png', True),
        ('-z 1.2 f.png', False),
        ('--dither .5 f.png', False),
        ('--floyd -Datkinson f.png', True),
        ('-Dfloyd f.png', True),
        ('--fl f.png', False),
    )
)
def test_parse_args(argv: str, error: bool) -> None:
    if not error:
        assert parse_args(argv.split())
        return
    with pytest.raises(SystemExit):
        parse_args(argv.split())


def test_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        main(['fya.jpg'])


@pytest.mark.parametrize(
    'argv, phrase, expect', (
        ('-m percentile', 'mode "percentile"', True),
        ('-m percentile', '0 and 99', True),
        ('-m percentile', 'default: 50', True),
        ('-m local', 'allows values', True),
        ('-m local', '0 and 9999', True),
        ('-m median', 'allows values', False),
        ('-o fya.txt', 'output file (default: False', True),
        ('-o /dev/stdout', 'output file (default: True', True),
        ('', 'default: /dev/stdout', True),
        ('', 'output file (default: True', True),
    )
)
def test_cli_help(
    argv: str, phrase: str, expect: bool,
    capsys: pytest.CaptureFixture[str],
) -> None:
    try:
        main(argv.split() + ['-h'])
    except SystemExit:
        ...
    collapsed = ' '.join(
        ' '.join(
            capsys.readouterr().out.split('\n')
        ).split()
    )
    if expect:
        assert phrase in capsys.readouterr().out or phrase in collapsed
    else:
        assert (
            phrase not in capsys.readouterr().out and phrase not in collapsed
        )


def test_cli_debug_output(capsys: pytest.CaptureFixture[str]) -> None:
    main('eppels.png -z .5 -o /dev/null -f -d'.split())  # noqa: SIM905
    stderr = capsys.readouterr().err
    assert 'resize image to 50.0%' in stderr
    assert 'image dimensions: 202×151' in stderr


@mock.patch(
    'p.terminal_rcwh',
    side_effect=lambda: (44, 174, 1914, 1012),
)
def test_cli_creates_file(terminal_rcwh_mock: mock.MagicMock) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        outfile = pathlib.Path(tmp) / 'fya.txt'
        main(f'eppels.png -o {outfile}'.split())
        assert outfile.exists()
        with pytest.raises(SystemExit):
            main(f'irrelevant.jpg -o {outfile}'.split())
        assert main(f'shelly.jpg -fo {outfile}'.split()) == 0


@pytest.fixture(scope='module')
def image() -> Image.Image:
    return (image := Image.open('eppels.png')).resize(
        (
            int(image.width * 1.6),
            int(image.height * 1.6)
        ),
        resample=Image.Resampling.LANCZOS,
    )


@pytest.mark.parametrize(
    'method, pattern, expect', (
        ('atkinson', '⠳', True),
        ('atkinson', '⢕', False),
        ('atkinson', '⣺⡺', False),
        ('floyd-steinberg', '⢕', True),
        ('floyd-steinberg', '⣺⡺', True),
    )
)
def test_dither_method(
    image: Image.Image, method: str, pattern: str, expect: bool,
) -> None:
    result = ['']
    for line in rasterize(
        image, dither_method=method, dither=.7,
        rcwh_func=lambda: (44, 174, 1914, 1012),
    ):
        result.append(line)
        if pattern in line:
            break
    output = '\n'.join(result)
    assertion = pattern in output if expect else pattern not in output
    predicate = 'expected' if expect else 'not expected'
    assert assertion, f'"{pattern}" {predicate} in {output}'
