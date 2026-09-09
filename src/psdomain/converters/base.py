"""
Base converter utilities for Pydantic <-> Proto conversion.
"""
from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import TypeVar, Callable, Any

T = TypeVar('T')


def snake_to_camel(s: str) -> str:
    """Convert snake_case to camelCase.

    Examples:
        >>> snake_to_camel('part_id')
        'partId'
        >>> snake_to_camel('inventory_location_id')
        'inventoryLocationId'
    """
    components = s.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def camel_to_snake(s: str) -> str:
    """Convert camelCase to snake_case.

    Examples:
        >>> camel_to_snake('partId')
        'part_id'
        >>> camel_to_snake('inventoryLocationId')
        'inventory_location_id'
    """
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()


def convert_list(items: list[T] | None, converter_func: Callable[[T], Any]) -> list:
    """Convert a list of items using the given converter function.

    Args:
        items: List of items to convert, or None
        converter_func: Function to apply to each item

    Returns:
        List of converted items, or empty list if items is None/empty
    """
    return [converter_func(item) for item in items] if items else []


def proto_str_or_none(value: str) -> str | None:
    """Convert proto string to Python string or None if empty.

    Proto uses empty strings for unset optional string fields.
    """
    return value if value else None


def pydantic_str_or_empty(value: str | None) -> str:
    """Convert Python string or None to proto-compatible string.

    Proto requires strings, not None, for string fields.
    """
    return value if value is not None else ""


def quantity_to_int(value) -> int:
    """Whole-number quantity for an int64 proto field.

    Suppliers occasionally report fractional quantities (67279 sent
    quantityAvailable '283.5' for TFLP48). ``int('283.5')`` raises, which failed
    the protobuf cache write and every protobuf response for the product
    (psrestful-api Sentry PSRESTFUL-API-8). Go through Decimal and truncate
    toward zero; None and '' count as 0. Non-numeric text still raises
    ValueError so genuinely bad data is not silently zeroed.
    """
    if value is None or value == '':
        return 0
    try:
        return int(Decimal(str(value).strip()))
    except InvalidOperation as e:
        raise ValueError(f'quantity is not numeric: {value!r}') from e
