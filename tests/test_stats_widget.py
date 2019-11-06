from pytypist.ui.stats_widget import StatsWidget
from pytypist.ui.signals import signals


def test_typing_widget(qtbot):
    widget = StatsWidget(None)
    qtbot.addWidget(widget)

    countdown_lcd = widget.countdown_lcd
    timer_lcd = widget.timer_lcd
    wpm_lcd = widget.wpm_lcd
    accuracy_lcd = widget.accuracy_lcd

    assert countdown_lcd.intValue() == 3
    for lcd in [timer_lcd, wpm_lcd, accuracy_lcd]:
        assert lcd.intValue() == 0

    signals.update_countdown.emit(0)
    assert countdown_lcd.intValue() == 0

    signals.update_typing_time.emit(30)
    assert timer_lcd.intValue() == 30

    signals.update_wpm.emit(60)
    assert wpm_lcd.intValue() == 60

    signals.update_accuracy.emit(95)
    assert accuracy_lcd.intValue() == 95
