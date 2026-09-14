from .base import Theme

DarkTerminal = Theme(
    name="DarkTerminal",
    bg_color="#0E1015",
    surface_color="#181B22",
    border_color="#333842",
    text_color="#FFFFFF",
    text_muted="#7D8590",
    accent_color="#F59E0B",
    alert_color="#EF4444",
    success_color="#10B981",
    font_mono="IBM Plex Mono",
    font_sans="IBM Plex Sans",
)

MidnightCyber = Theme(
    name="MidnightCyber",
    bg_color="#090D16",
    surface_color="#111827",
    border_color="#1F2937",
    text_color="#F9FAFB",
    text_muted="#6B7280",
    accent_color="#06B6D4", # Cyan
    alert_color="#F43F5E", # Rose
    success_color="#10B981",
    font_mono="JetBrains Mono",
    font_sans="Inter",
)

CleanLight = Theme(
    name="CleanLight",
    bg_color="#F8FAFC",
    surface_color="#FFFFFF",
    border_color="#E2E8F0",
    text_color="#0F172A",
    text_muted="#64748B",
    accent_color="#2563EB", # Blue
    alert_color="#DC2626",
    success_color="#059669",
    font_mono="SF Mono",
    font_sans="Inter",
)

__all__ = ["Theme", "DarkTerminal", "MidnightCyber", "CleanLight"]
