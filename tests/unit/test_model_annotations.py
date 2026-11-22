"""Python 3.14 evaluates annotations lazily, in the class namespace. A field written as
``ProductArray: Optional[ProductArray] = None`` then reads its own default (None) instead of the
ProductArray class, so pydantic types it as NoneType and rejects any real value ("Input should be None").
"""
import ast
import importlib
import inspect
import pathlib
import pkgutil
import types

import pytest
from pydantic import BaseModel

import psdomain.model

MODEL_DIR = pathlib.Path(psdomain.model.__file__).parent


def _shadowed_fields():
    """(file:line, Class.field) for every defaulted field whose name appears in its own annotation."""
    for path in sorted(MODEL_DIR.rglob('*.py')):
        tree = ast.parse(path.read_text())
        for cls in (n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)):
            for stmt in cls.body:
                if not (isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.value):
                    continue
                names = {n.id for n in ast.walk(stmt.annotation) if isinstance(n, ast.Name)}
                if stmt.target.id in names:
                    yield f'{path.relative_to(MODEL_DIR)}:{stmt.lineno} {cls.name}.{stmt.target.id}'


def test_no_defaulted_field_shares_its_name_with_a_type_in_its_annotation():
    """Static, so it fails on any Python version, including the 3.12 the CI may run."""
    assert list(_shadowed_fields()) == []


def _models():
    for info in pkgutil.walk_packages(psdomain.model.__path__, 'psdomain.model.'):
        module = importlib.import_module(info.name)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseModel) and obj.__module__ == module.__name__:
                yield obj


@pytest.mark.parametrize('model', list(_models()), ids=lambda m: f'{m.__module__}.{m.__name__}')
def test_no_model_field_resolves_to_none_type(model):
    """Runtime check: on Python 3.14 a shadowed annotation shows up here as NoneType."""
    none_fields = [name for name, field in model.model_fields.items() if field.annotation is types.NoneType]
    assert none_fields == []
