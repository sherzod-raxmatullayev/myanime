# ============================================================
# DB BACKUP (dumpdata -> ZIP) FUNKSIYALARI
# ============================================================
import io
import zipfile

from asgiref.sync import sync_to_async
from django.core.management import call_command


@sync_to_async
def make_full_dump_json_bytes() -> bytes:
    """Django dumpdata -> JSON bytes (butun baza data)."""
    buf = io.StringIO()
    call_command(
        "dumpdata",
        "--natural-foreign",
        "--natural-primary",
        "--indent",
        "2",
        exclude=["contenttypes", "auth.permission"],
        stdout=buf
    )
    return buf.getvalue().encode("utf-8")


def zip_bytes(filename: str, data: bytes) -> bytes:
    """JSON bytes -> ZIP bytes."""
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(filename, data)
    return out.getvalue()
