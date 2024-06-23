from __future__ import annotations

import dataclasses
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve(strict=True).parent


@dataclasses.dataclass(frozen=True)
class Policy:
    name: str
    aliases: list[str]
    priority: int
    symbol_versions: dict[str, dict[str, list[str]]]
    lib_whitelist: list[str]
    blacklist: dict[str, list[str]]


def _validation(policies: list[Policy]) -> None:
    symbol_versions: dict[str, dict[str, set[str]]] = {}
    lib_whitelist: set[str] = set()
    for policy in sorted(policies, key=lambda x: x.priority, reverse=True):
        if policy.name == "linux":
            continue
        if not lib_whitelist.issubset(set(policy.lib_whitelist)):
            diff = lib_whitelist - set(policy.lib_whitelist)
            msg = f"Invalid policies: missing whitelist libraries in {policy.name!r} compared to previous policies: {diff}"
            raise ValueError(msg)
        lib_whitelist.update(policy.lib_whitelist)
        known_arch = set(symbol_versions.keys())
        known_arch.discard("ppc64")  # manylinux2014 initial commit
        current_arch = set(policy.symbol_versions.keys())
        if not known_arch.issubset(current_arch):
            diff = known_arch - current_arch
            msg = f"Invalid policies: missing architecture in {policy.name!r} compared to previous policies: {diff}"
            raise ValueError(msg)
        for arch in policy.symbol_versions.keys():
            symbol_versions_arch = symbol_versions.get(arch, defaultdict(set))
            for prefix in policy.symbol_versions[arch].keys():
                policy_symbol_versions = set(policy.symbol_versions[arch][prefix])
                if not symbol_versions_arch[prefix].issubset(policy_symbol_versions):
                    diff = symbol_versions_arch[prefix] - policy_symbol_versions
                    msg = f"Invalid policies: missing symbol versions in '{policy.name}_{arch}' for {prefix} compared to previous policies: {diff}"
                    raise ValueError(msg)
                symbol_versions_arch[prefix].update(policy.symbol_versions[arch][prefix])
            symbol_versions[arch] = symbol_versions_arch


def load_policies(path: Path) -> list[Policy]:
    data = json.loads(path.read_text())
    policies = list(Policy(**policy) for policy in data)
    _validation(policies)
    return policies


class _PoliciesJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_indent = 0

    def encode(self, o):
        if isinstance(o, (list, tuple)):
            last_level = True
            for item in o:
                if not isinstance(item, (str, int)):
                    last_level = False
                    break
            if last_level:
                return json.dumps(o)
            output = []
            self.current_indent += self.indent
            indent_str = " " * self.current_indent
            for item in o:
                output.append(f"{indent_str}{self.encode(item)}")
            self.current_indent -= self.indent
            indent_str = " " * self.current_indent
            return f"[\n{',\n'.join(output)}\n{indent_str}]"

        if isinstance(o, (dict, Policy)):
            if not o:
                return "{}"
            if isinstance(o, Policy):
                o = dataclasses.asdict(o)
            output = []
            self.current_indent += self.indent
            indent_str = " " * self.current_indent
            for key, value in o.items():
                output.append(f"{indent_str}{json.dumps(key)}: {self.encode(value)}")
            self.current_indent -= self.indent
            indent_str = " " * self.current_indent
            return f"{{\n{',\n'.join(output)}\n{indent_str}}}"

        return json.dumps(o)


OFFICIAL_POLICIES = load_policies(HERE / "manylinux-policy.json")


def dump(policies: list[Policy] | None = None, path: Path | None = None) -> None:
    if policies is None:
        policies = OFFICIAL_POLICIES
    if path is None:
        path = HERE / "tools" / "manylinux-policy.json"
    path.write_text(json.dumps(policies, cls=_PoliciesJSONEncoder, indent=2) + "\n")
