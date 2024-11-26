import traceback

try:
    from .tree.models import Tree  # noqa
except Exception:
    traceback.print_exc()
