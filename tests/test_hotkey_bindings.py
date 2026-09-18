from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QKeyEvent
from pynput.keyboard import Key, KeyCode

from poemarcut import keyboard
from poemarcut_gui import HotkeyCaptureLineEdit, _hotkey_from_qt_key


def test_parse_and_match_ctrl_digit_combo() -> None:
    binding = keyboard.keyorkeycode_from_str("ctrl+1")

    assert keyboard.binding_matches(
        event_key=KeyCode.from_char("1"),
        binding=binding,
        modifiers=frozenset({"ctrl"}),
    )
    assert not keyboard.binding_matches(
        event_key=KeyCode.from_char("1"),
        binding=binding,
        modifiers=frozenset(),
    )
    assert not keyboard.binding_matches(
        event_key=KeyCode.from_char("1"),
        binding=binding,
        modifiers=frozenset({"ctrl", "shift"}),
    )


def test_plain_binding_does_not_fire_with_modifier() -> None:
    binding = keyboard.keyorkeycode_from_str("f1")

    assert keyboard.binding_matches(event_key=Key.f1, binding=binding)
    assert not keyboard.binding_matches(
        event_key=Key.f1,
        binding=binding,
        modifiers=frozenset({"ctrl"}),
    )


def test_multiple_modifiers_and_aliases() -> None:
    binding = keyboard.keyorkeycode_from_str("control+shift+f3")

    assert keyboard.binding_matches(
        event_key=Key.f3,
        binding=binding,
        modifiers=frozenset({"ctrl", "shift"}),
    )


def test_qt_hotkey_formatter() -> None:
    assert _hotkey_from_qt_key(
        Qt.Key.Key_1.value,
        Qt.KeyboardModifier.ControlModifier,
    ) == "ctrl+1"
    assert _hotkey_from_qt_key(
        Qt.Key.Key_F3.value,
        Qt.KeyboardModifier.NoModifier,
    ) == "f3"
    assert _hotkey_from_qt_key(
        Qt.Key.Key_A.value,
        Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier,
    ) == "ctrl+shift+a"
    assert _hotkey_from_qt_key(
        Qt.Key.Key_Control.value,
        Qt.KeyboardModifier.ControlModifier,
    ) is None


def test_hotkey_capture_lineedit_records_physical_combo(qapp) -> None:
    lineedit = HotkeyCaptureLineEdit("f1")
    event = QKeyEvent(
        QEvent.Type.KeyPress,
        Qt.Key.Key_3,
        Qt.KeyboardModifier.ControlModifier,
        "3",
    )

    lineedit.keyPressEvent(event)

    assert lineedit.text() == "ctrl+3"
