from enum import IntEnum

import serial.tools.list_ports
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QGroupBox,
    QRadioButton,
    QPushButton,
    QButtonGroup,
    QCheckBox,
    QLabel,
    QMainWindow,
    QTabWidget,
    QComboBox,
    QToolButton,
    QLayout,
    QAction,
)

from src.PulsePal import PulsePalObject
from src.scientific_spinbox import ScienDSpinBox

N_OUTPUT_CHANNELS = 4


def constrain_value(value, min_value, max_value):
    if value > max_value:
        return max_value
    elif value < min_value:
        return min_value
    else:
        return value


class PulsePalTriggerMode(IntEnum):
    NORMAL = 0
    TOGGLE = 1
    GATED = 2


class PulsePalTriggerChannel(IntEnum):
    TRIGGER1 = 1
    TRIGGER2 = 2


class PulsePalCustomTrainID(IntEnum):
    NONE = 0
    TRAIN1 = 1
    TRAIN2 = 2


class PulsePalCustomTrainTarget(IntEnum):
    PULSES = 0
    BURSTS = 1


class PulsePalCustomTrainLoop(IntEnum):
    ONE_SHOT = 0
    LOOP = 1


class PulsePalOutputChannel(object):
    MIN_DURATION = 0.0001
    MAX_DURATION = 3600
    MIN_VOLTAGE = -10.0
    MAX_VOLTAGE = 10.0

    def __init__(self, channel_id, pulsepal: PulsePalObject):
        self.channel_id = channel_id
        self.pulsepal = pulsepal
        self.__biphasic = False
        self.__baseline_voltage = 0.0
        self.__phase1_voltage = 5.0
        self.__phase1_duration = 0.001
        self.__phase2_voltage = -5.0
        self.__phase2_duration = 0.001
        self.__interphase_interval = 0.0001
        self.__interpulse_interval = 0.1
        self.__burst_mode = False
        self.__interburst_interval = 0.0
        self.__burst_duration = 0.0
        self.__train_delay = 0.0
        self.__train_duration = 1.0
        self.__trigger_source = set()
        self.__custom_train_id = PulsePalCustomTrainID.NONE
        self.__custom_train_target = PulsePalCustomTrainTarget.PULSES
        self.__custom_train_loop = PulsePalCustomTrainLoop.ONE_SHOT

    @property
    def is_biphasic(self) -> bool:
        return self.__biphasic

    @is_biphasic.setter
    def is_biphasic(self, value: bool):
        self.__biphasic = value
        self.pulsepal.programOutputChannelParam(
            "isBiphasic", self.channel_id, int(value)
        )

    @property
    def baseline_voltage(self) -> float:
        return self.__baseline_voltage

    @baseline_voltage.setter
    def baseline_voltage(self, value: float):
        self.__baseline_voltage = constrain_value(
            value, self.MIN_VOLTAGE, self.MAX_VOLTAGE
        )
        self.pulsepal.programOutputChannelParam(
            "restingVoltage", self.channel_id, self.__baseline_voltage
        )

    @property
    def phase1_duration(self) -> float:
        return self.__phase1_duration

    @phase1_duration.setter
    def phase1_duration(self, value: float):
        self.__phase1_duration = constrain_value(
            value, self.MIN_DURATION, self.MAX_DURATION
        )
        self.pulsepal.programOutputChannelParam(
            "phase1Duration", self.channel_id, self.__phase1_duration
        )

    @property
    def phase1_voltage(self) -> float:
        return self.__phase1_voltage

    @phase1_voltage.setter
    def phase1_voltage(self, value: float):
        self.__phase1_voltage = constrain_value(
            value, self.MIN_VOLTAGE, self.MAX_VOLTAGE
        )
        self.pulsepal.programOutputChannelParam(
            "phase1Voltage", self.channel_id, self.__phase1_voltage
        )

    @property
    def phase2_voltage(self) -> float:
        return self.__phase2_voltage

    @phase2_voltage.setter
    def phase2_voltage(self, value: float):
        self.__phase2_voltage = constrain_value(
            value, self.MIN_VOLTAGE, self.MAX_VOLTAGE
        )
        self.pulsepal.programOutputChannelParam(
            "phase2Voltage", self.channel_id, self.__phase2_voltage
        )

    @property
    def phase2_duration(self) -> float:
        return self.__phase2_duration

    @phase2_duration.setter
    def phase2_duration(self, value: float):
        self.__phase2_duration = constrain_value(
            value, self.MIN_DURATION, self.MAX_DURATION
        )
        self.pulsepal.programOutputChannelParam(
            "phase2Duration", self.channel_id, self.__phase2_duration
        )

    @property
    def interphase_interval(self) -> float:
        return self.__interphase_interval

    @interphase_interval.setter
    def interphase_interval(self, value):
        self.__interphase_interval = constrain_value(
            value, self.MIN_DURATION, self.MAX_DURATION
        )
        self.pulsepal.programOutputChannelParam(
            "interPhaseInterval", self.channel_id, self.__interphase_interval
        )

    @property
    def interpulse_interval(self) -> float:
        return self.__interpulse_interval

    @interpulse_interval.setter
    def interpulse_interval(self, value):
        self.__interpulse_interval = constrain_value(
            value, self.MIN_DURATION, self.MAX_DURATION
        )
        self.pulsepal.programOutputChannelParam(
            "interPulseInterval", self.channel_id, self.__interpulse_interval
        )

    @property
    def interburst_interval(self) -> float:
        return self.__interburst_interval

    @interburst_interval.setter
    def interburst_interval(self, value):
        self.__interburst_interval = constrain_value(
            value, self.MIN_DURATION, self.MAX_DURATION
        )
        self.pulsepal.programOutputChannelParam(
            "interBurstInterval", self.channel_id, self.interburst_interval
        )

    @property
    def is_burst(self) -> bool:
        return self.__burst_mode

    @is_burst.setter
    def is_burst(self, value: bool):
        self.__burst_mode = value
        if self.is_burst:
            self.pulsepal.programOutputChannelParam(
                "burstDuration", self.channel_id, self.__burst_duration
            )
        else:
            self.pulsepal.programOutputChannelParam(
                "burstDuration", self.channel_id, 0.0
            )

    @property
    def burst_duration(self):
        return self.__burst_duration

    @burst_duration.setter
    def burst_duration(self, value):
        self.__burst_duration = constrain_value(
            value, self.MIN_DURATION, self.MAX_DURATION
        )
        self.pulsepal.programOutputChannelParam(
            "burstDuration", self.channel_id, self.__burst_duration
        )

    @property
    def train_delay(self) -> float:
        return self.__train_delay

    @train_delay.setter
    def train_delay(self, value: float):
        self.__train_delay = constrain_value(value, 0.0, self.MAX_DURATION)
        self.pulsepal.programOutputChannelParam(
            "pulseTrainDelay", self.channel_id, self.__train_delay
        )

    @property
    def train_duration(self) -> float:
        return self.__train_duration

    @train_duration.setter
    def train_duration(self, value: float):
        self.__train_duration = constrain_value(
            value, self.MIN_DURATION, self.MAX_DURATION
        )
        self.pulsepal.programOutputChannelParam(
            "pulseTrainDuration", self.channel_id, self.__train_duration
        )

    @property
    def trigger_source(self):
        return self.__trigger_source

    def enable_trigger_source(self, value: PulsePalTriggerChannel):
        self.__trigger_source.add(value)
        self.__update_trigger_source()

    def disable_trigger_source(self, value: PulsePalTriggerChannel):
        self.__trigger_source.discard(value)
        self.__update_trigger_source()

    def __update_trigger_source(self):
        self.pulsepal.programOutputChannelParam(
            "linkTriggerChannel1",
            self.channel_id,
            PulsePalTriggerChannel.TRIGGER1 in self.__trigger_source,
        )
        self.pulsepal.programOutputChannelParam(
            "linkTriggerChannel2",
            self.channel_id,
            PulsePalTriggerChannel.TRIGGER2 in self.__trigger_source,
        )

    @property
    def custom_train_id(self) -> PulsePalCustomTrainID:
        return self.__custom_train_id

    @custom_train_id.setter
    def custom_train_id(self, value: PulsePalCustomTrainID):
        self.__custom_train_id = value
        # self.pulsepal.programOutputChannelParam('', self.channel_id, )  # FIXME

    @property
    def custom_train_target(self) -> PulsePalCustomTrainTarget:
        return self.__custom_train_target

    @custom_train_target.setter
    def custom_train_target(self, value: PulsePalCustomTrainTarget):
        self.__custom_train_target = value
        # self.pulsepal.programOutputChannelParam('', self.channel_id, )  # FIXME

    @property
    def custom_train_loop(self) -> PulsePalCustomTrainLoop:
        return self.__custom_train_loop

    @custom_train_loop.setter
    def custom_train_loop(self, value: PulsePalCustomTrainLoop):
        self.__custom_train_loop = value
        # self.pulsepal.programOutputChannelParam('', self.channel_id, )  # FIXME

    def do_soft_trigger(self):
        channels = [0] * 4
        channels[self.channel_id - 1] = 1
        self.pulsepal.triggerOutputChannels(*channels)


# noinspection PyPep8Naming
class DummyPulsePalObject(PulsePalObject):
    # noinspection PyMissingConstructor,PyUnusedLocal
    def __init__(self, PortName):
        print(f"__init__({PortName})")

    def setFixedVoltage(self, channel, voltage):
        print(f"setFixedVoltage({channel}, {voltage})")

    def programOutputChannelParam(self, paramName, channel, value):
        print(f"programOutputChannelParam(self, {paramName}, {channel}, {value})")

    def programTriggerChannelParam(self, paramName, channel, value):
        print(f"programTriggerChannelParam(self, {paramName}, {channel}, {value})")

    def syncAllParams(self):
        print(f"syncAllParams(self)")

    def sendCustomPulseTrain(self, customTrainID, pulseTimes, pulseVoltages):
        print(
            f"sendCustomPulseTrain(self, {customTrainID}, {pulseTimes}, {pulseVoltages})"
        )

    def sendCustomWaveform(self, customTrainID, pulseWidth, pulseVoltages):
        print(
            f"sendCustomWaveform(self, {customTrainID}, {pulseWidth}, {pulseVoltages})"
        )

    def setContinuousLoop(self, channel, state):
        print(f"setContinuousLoop(self, {channel}, {state})")

    def triggerOutputChannels(self, channel1, channel2, channel3, channel4):
        print(
            f"triggerOutputChannels(self, {channel1}, {channel2}, {channel3}, {channel4})"
        )

    def abortPulseTrains(self):
        print(f"abortPulseTrains(self)")

    def __del__(self):
        print(f"__del__()")


def discover_ports(pattern="Arduino"):
    ports = serial.tools.list_ports.grep(pattern)
    return list(ports)


class PulsePalChannelWidget(QWidget):
    amplitudeGroupBox: QGroupBox
    baselineVoltageSpinBox: ScienDSpinBox
    phase1VoltageSpinBox: ScienDSpinBox
    phase2VoltageSpinBox: ScienDSpinBox

    burstModeGroupBox: QGroupBox
    burstDurationSpinBox: ScienDSpinBox
    interBurstIntervalSpinBox: ScienDSpinBox

    customTrainGroupBox: QGroupBox
    customTrain1RadioButton: QRadioButton
    customTrain2RadioButton: QRadioButton
    loadCustomTrain1PushButton: QPushButton
    loadCustomTrain2PushButton: QPushButton

    interPhaseIntervalSpinBox: ScienDSpinBox
    phase1DurationSpinBox: ScienDSpinBox
    phase2DurationSpinBox: ScienDSpinBox
    pulseIntervalSpinBox: ScienDSpinBox
    trainDelaySpinBox: ScienDSpinBox
    trainDurationSpinBox: ScienDSpinBox

    softTriggerPushButton: QPushButton
    trigger1CheckBox: QCheckBox
    trigger2CheckBox: QCheckBox

    outputModeGroupBox: QGroupBox
    outputModeBiphasicRadioButton: QRadioButton
    outputModeMonophasicRadioButton: QRadioButton

    customTrainButtonGroup: QButtonGroup
    outputModeButtonGroup: QButtonGroup

    schemaLabel: QLabel

    def __init__(self, channel: PulsePalOutputChannel):
        super().__init__()
        # noinspection SpellCheckingInspection
        uic.loadUi("channelwidget.ui", self)
        self.__channel = channel
        self.__phase2_widgets = [
            self.phase2VoltageSpinBox,
            self.phase2VoltageLabel,
            self.phase2DurationSpinBox,
            self.phase2DurationLabel,
            self.interPhaseIntervalSpinBox,
            self.interPhaseIntervalLabel,
        ]

        # SLOTS
        self.outputModeButtonGroup.buttonToggled.connect(self.__toggle_output_mode)
        self.burstModeGroupBox.toggled.connect(self.__toggle_burst_mode)
        self.trigger1CheckBox.toggled.connect(self.__toggle_trigger1_source)
        self.trigger2CheckBox.toggled.connect(self.__toggle_trigger2_source)
        self.softTriggerPushButton.clicked.connect(self.__do_soft_trigger)

        self.baselineVoltageSpinBox.valueChanged.connect(self.__update_baseline_voltage)
        self.phase1VoltageSpinBox.valueChanged.connect(self.__update_phase1_voltage)
        self.phase2VoltageSpinBox.valueChanged.connect(self.__update_phase2_voltage)
        self.trainDelaySpinBox.valueChanged.connect(self.__update_train_delay)
        self.trainDurationSpinBox.valueChanged.connect(self.__update_train_duration)
        self.phase1DurationSpinBox.valueChanged.connect(self.__update_phase1_duration)
        self.phase2DurationSpinBox.valueChanged.connect(self.__update_phase2_duration)
        self.interPhaseIntervalSpinBox.valueChanged.connect(
            self.__update_interphase_interval
        )
        self.pulseIntervalSpinBox.valueChanged.connect(
            self.__update_interpulse_interval
        )
        self.burstDurationSpinBox.valueChanged.connect(self.__update_burst_duration)
        self.interBurstIntervalSpinBox.valueChanged.connect(
            self.__update_interburst_interval
        )

        # self.softTriggerPushButton.setIcon(QIcon(':/icons/lightning.png'))
        self.update_all_content()

    def update_all_content(self):
        self.baselineVoltageSpinBox.setValue(self.__channel.baseline_voltage)
        self.phase1VoltageSpinBox.setValue(self.__channel.phase1_voltage)
        self.phase2VoltageSpinBox.setValue(self.__channel.phase2_voltage)

        self.burstModeGroupBox.setChecked(self.__channel.is_burst)
        self.burstDurationSpinBox.setValue(self.__channel.burst_duration)
        self.interBurstIntervalSpinBox.setValue(self.__channel.interburst_interval)

        self.interPhaseIntervalSpinBox.setValue(self.__channel.interphase_interval)
        self.phase1DurationSpinBox.setValue(self.__channel.phase1_duration)
        self.phase2DurationSpinBox.setValue(self.__channel.phase2_duration)
        self.pulseIntervalSpinBox.setValue(self.__channel.interpulse_interval)
        self.trainDelaySpinBox.setValue(self.__channel.train_delay)
        self.trainDurationSpinBox.setValue(self.__channel.train_duration)

        self.trigger1CheckBox.setChecked(
            PulsePalTriggerChannel.TRIGGER1 in self.__channel.trigger_source
        )
        self.trigger2CheckBox.setChecked(
            PulsePalTriggerChannel.TRIGGER2 in self.__channel.trigger_source
        )

        self.outputModeBiphasicRadioButton.setChecked(self.__channel.is_biphasic)
        self.outputModeMonophasicRadioButton.setChecked(not self.__channel.is_biphasic)
        self.__update_schema()

    def __update_schema(self):
        if not self.__channel.is_biphasic:
            if not self.__channel.is_burst:
                self.schemaLabel.setPixmap(
                    QPixmap(":/pixmaps/PulseSchemaMonopolarNoBurst.png")
                )
            else:
                self.schemaLabel.setPixmap(
                    QPixmap(":/pixmaps/PulseSchemaMonopolarBurst.png")
                )
        else:
            if not self.__channel.is_burst:
                self.schemaLabel.setPixmap(
                    QPixmap(":/pixmaps/PulseSchemaBipolarNoBurst.png")
                )
            else:
                self.schemaLabel.setPixmap(
                    QPixmap(":/pixmaps/PulseSchemaBipolarBurst.png")
                )

    # noinspection PyUnusedLocal
    def __toggle_output_mode(self, btn, checked):
        self.__channel.is_biphasic = self.outputModeBiphasicRadioButton.isChecked()
        for widget in self.__phase2_widgets:
            widget.setEnabled(self.outputModeBiphasicRadioButton.isChecked())
            # this ensures the values are propagated to the channel when the widget becomes enabled.
            # Not sure that this is truly needed
            if widget.isEnabled() and "valueChanged" in widget.__dir__():
                widget.valueChanged.emit(widget.value())
        self.__update_schema()

    def __toggle_burst_mode(self, checked):
        self.__channel.is_burst = checked
        self.__update_schema()

    def __toggle_trigger1_source(self, checked):
        if checked:
            self.__channel.enable_trigger_source(PulsePalTriggerChannel.TRIGGER1)
        else:
            self.__channel.disable_trigger_source(PulsePalTriggerChannel.TRIGGER1)

    def __toggle_trigger2_source(self, checked):
        if checked:
            self.__channel.enable_trigger_source(PulsePalTriggerChannel.TRIGGER2)
        else:
            self.__channel.disable_trigger_source(PulsePalTriggerChannel.TRIGGER2)

    def __do_soft_trigger(self):
        self.__channel.do_soft_trigger()

    def __update_baseline_voltage(self, value):
        self.__channel.baseline_voltage = value

    def __update_phase1_voltage(self, value):
        self.__channel.phase1_voltage = value

    def __update_phase2_voltage(self, value):
        self.__channel.phase2_voltage = value

    def __update_train_delay(self, value):
        self.__channel.train_delay = value

    def __update_train_duration(self, value):
        self.__channel.train_duration = value

    def __update_phase1_duration(self, value):
        self.__channel.phase1_duration = value

    def __update_phase2_duration(self, value):
        self.__channel.phase2_duration = value

    def __update_interphase_interval(self, value):
        self.__channel.interphase_interval = value

    def __update_interpulse_interval(self, value):
        self.__channel.interpulse_interval = value

    def __update_burst_duration(self, value):
        self.__channel.burst_duration = value

    def __update_interburst_interval(self, value):
        self.__channel.interburst_interval = value


class MainWindow(QMainWindow):
    channelsTabWidget: QTabWidget
    trigger1ModeComboBox: QComboBox
    trigger2ModeComboBox: QComboBox
    channel1TriggerCheckBox: QCheckBox
    channel2TriggerCheckBox: QCheckBox
    channel3TriggerCheckBox: QCheckBox
    channel4TriggerCheckBox: QCheckBox
    softTriggerPushButton: QPushButton
    customTrain1LoadPulsesToolButton: QToolButton
    customTrain2LoadPulsesToolButton: QToolButton
    customTrain1LoadWaveformToolButton: QToolButton
    customTrain2LoadWaveformToolButton: QToolButton
    customTrain1LoadedLabel: QLabel
    customTrain2LoadedLabel: QLabel

    action_Connect: QAction
    action_Quit: QAction
    action_About: QAction
    action_Abort: QAction

    def __init__(self, pulsepal: PulsePalObject):
        super().__init__()
        # noinspection SpellCheckingInspection
        uic.loadUi("mainwindow.ui", self)

        self.pulsepal = pulsepal
        for ch_id in range(N_OUTPUT_CHANNELS):
            ch = PulsePalOutputChannel(ch_id + 1, pulsepal)
            widget = PulsePalChannelWidget(ch)
            self.channelsTabWidget.addTab(widget, f"Channel {ch.channel_id}")

        self.layout().setSizeConstraint(QLayout.SetFixedSize)  # FIXME

        self.action_Connect.triggered.connect(self.__action_connect)
        self.action_Quit.triggered.connect(self.__action_quit)
        self.action_About.triggered.connect(self.__action_about)
        self.action_Abort.triggered.connect(self.__action_abort)
        self.trigger1ModeComboBox.currentIndexChanged.connect(
            self.__trigger1_mode_changed
        )
        self.trigger2ModeComboBox.currentIndexChanged.connect(
            self.__trigger2_mode_changed
        )
        self.softTriggerPushButton.clicked.connect(self.__do_soft_trigger)

    # noinspection PyUnusedLocal
    def __action_quit(self, checked):
        self.close()

    def __action_connect(self, checked):
        pass

    def __action_about(self, checked):
        pass

    # noinspection PyUnusedLocal
    def __action_abort(self, checked):
        self.pulsepal.abortPulseTrains()

    def __trigger1_mode_changed(self, index: int):
        self.pulsepal.programTriggerChannelParam("triggerMode", 1, index)

    def __trigger2_mode_changed(self, index: int):
        mode = PulsePalTriggerMode(index)
        self.pulsepal.programTriggerChannelParam("triggerMode", 2, mode)

    def __do_soft_trigger(self, checked):
        channels = [
            int(self.channel1TriggerCheckBox.isChecked()),
            int(self.channel2TriggerCheckBox.isChecked()),
            int(self.channel3TriggerCheckBox.isChecked()),
            int(self.channel4TriggerCheckBox.isChecked()),
        ]
        self.pulsepal.triggerOutputChannels(*channels)
