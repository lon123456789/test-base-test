from typing import Any


def safe_get(d: dict, key: str, default: Any = None) -> Any:
    return d[key] if key in d else default


def pct(value: float, total: float) -> float:
    if total == 0:
        return 0.0
    return (value / total) * 100.0


def clamp(value: float, min_value: float = 0.0, max_value: float = 100.0) -> float:
    return max(min_value, min(value, max_value))


if __name__ == "__main__":
    print("utils ready.")
