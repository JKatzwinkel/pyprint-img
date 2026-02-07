from abc import ABC, abstractmethod
from dataclasses import dataclass
import pathlib
import subprocess
import tempfile
import sys
from typing import Literal, cast
from textwrap import dedent


type Blocktype = Literal['bash', 'output', 'text', None]


@dataclass
class Block(ABC):
    lines: list[str]
    start: int

    @abstractmethod
    def print(self) -> str:
        ...


class Textblock(Block):
    def print(self) -> str:
        return '\n'.join(self.lines)


@dataclass
class Codeblock(Block):
    blocktype: Blocktype

    def print(self) -> str:
        return '\n'.join(
            [f'```{self.blocktype}'] + self.lines + ['```']
        )

    def overwrite(self, lines: list[str]) -> None:
        self.lines.clear()
        self.lines.extend(lines)


def execute(block: Block) -> list[str]:
    assert isinstance(block, Codeblock)
    if block.blocktype != 'bash':
        return []
    with tempfile.NamedTemporaryFile(suffix='.sh') as tmp:
        pathlib.Path(tmp.name).write_text(
            '\n'.join(
                ['#!/usr/bin/env bash'] + block.lines
            )
        )
        try:
            out = subprocess.check_output(
                f'bash {tmp.name}', shell=True, encoding='utf-8',
            ).strip()
        except subprocess.CalledProcessError as e:
            out = f'{e.output}<exit code {e.returncode}>'
    return out.split('\n')


def makeblock(blocktype: Blocktype, lines: list[str], start: int) -> Block:
    if blocktype == 'text':
        return Textblock(lines.copy(), start)
    return Codeblock(lines.copy(), start, blocktype)


def process(doc: list[str]) -> list[Block]:
    lines: list[str] = []
    blocks: list[Block] = []
    block_type: Blocktype = 'text'
    start: int = 0
    for lineno, line in enumerate(doc):
        if line.startswith('```'):
            syntax = line.split('```')[-1]
            blocks.append(
                makeblock(block_type, lines, start)
            )
            if not syntax:
                block_type = 'text'
            else:
                block_type = cast(Blocktype, syntax)
                start = lineno
            lines.clear()
        else:
            lines.append(line)
    blocks.append(
        makeblock(block_type, lines[:-1], start)
    )
    return blocks


def test_process_input() -> None:
    doc = dedent('''
    intro
    ```bash
    export VAR=fya
    printenv VAR
    ```

    hence:

    ```output
    fya
    ```

    end
    ''').split('\n')
    blocks = process(doc)
    assert blocks[0].print() == dedent('''
    intro''')
    assert blocks[1].print() == dedent('''\
    ```bash
    export VAR=fya
    printenv VAR
    ```''')
    assert blocks[-1].print() == dedent('''
    end''')


def test_execute() -> None:
    blocks = process(dedent('''
    ```bash
    echo fya | cat
    ```
    ''').split('\n'))
    assert execute(blocks[1]) == ['fya']


def test_execute_error() -> None:
    blocks = process(dedent('''
    ```bash
    ls fya 2>&1 && echo ok
    ```
    ''').split('\n'))
    assert execute(blocks[1]) == [
        "ls: cannot access 'fya': No such file or directory",
        '<exit code 2>'
    ]


def test_use_output_only_once() -> None:
    blocks = run(process(dedent('''
    ```bash
    echo fya
    ```

    ```output
    ```

    something unrelated:

    ```output
    ```
    ''').split('\n')))
    assert blocks[3].blocktype == 'output'  # type: ignore[attr-defined]
    assert blocks[3].lines == ['fya']
    assert blocks[-2].blocktype == 'output'  # type: ignore[attr-defined]
    assert blocks[-2].lines == []


def run(blocks: list[Block]) -> list[Block]:
    output: list[str] = []
    for block in blocks:
        if not isinstance(block, Codeblock):
            continue
        if block.blocktype == 'bash':
            output = execute(block)
        elif block.blocktype == 'output':
            block.overwrite(output)
            output.clear()
    return blocks


def update_blocks(blocks: list[Block]) -> str:
    return '\n'.join(
        block.print() for block in run(blocks)
    )


def main(outfile: str = '/dev/stdout') -> None:
    blocks = process(
        pathlib.Path('readme.md').read_text().split('\n')
    )
    with pathlib.Path(outfile).open('w') as f:
        print(update_blocks(blocks), file=f)


if __name__ == '__main__':
    main('/dev/stdout' if len(sys.argv) < 2 else sys.argv[-1])
