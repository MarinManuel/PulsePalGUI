from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QGroupBox, QRadioButton, QPushButton, QButtonGroup, QCheckBox, QLabel
import resources.resources as resources
from GUI.scientific_spinbox import ScienDSpinBox
from src.PulsePalHelpers import PulsePalOutputChannel, PulsePalTriggerChannel


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
        uic.loadUi("GUI/channelwidget.ui", self)
        self.__channel = channel
        self.__phase2_widgets = [self.phase2VoltageSpinBox, self.phase2VoltageLabel,
                                 self.phase2DurationSpinBox, self.phase2DurationLabel,
                                 self.interPhaseIntervalSpinBox, self.interPhaseIntervalLabel]

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
        self.interPhaseIntervalSpinBox.valueChanged.connect(self.__update_interphase_interval)
        self.pulseIntervalSpinBox.valueChanged.connect(self.__update_interpulse_interval)
        self.burstDurationSpinBox.valueChanged.connect(self.__update_burst_duration)
        self.interBurstIntervalSpinBox.valueChanged.connect(self.__update_interburst_interval)

        self.softTriggerPushButton.setIcon(QIcon(':/icons/lightning.png'))
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

        self.trigger1CheckBox.setChecked(PulsePalTriggerChannel.TRIGGER1 in self.__channel.trigger_source)
        self.trigger2CheckBox.setChecked(PulsePalTriggerChannel.TRIGGER2 in self.__channel.trigger_source)

        self.outputModeBiphasicRadioButton.setChecked(self.__channel.is_biphasic)
        self.outputModeMonophasicRadioButton.setChecked(not self.__channel.is_biphasic)
        self.__update_schema()

    def __update_schema(self):
        if not self.__channel.is_biphasic:
            if not self.__channel.is_burst:
                self.schemaLabel.setPixmap(QPixmap(':/pixmaps/PulseSchemaMonopolarNoBurst.png'))
            else:
                self.schemaLabel.setPixmap(QPixmap(':/pixmaps/PulseSchemaMonopolarBurst.png'))
        else:
            if not self.__channel.is_burst:
                self.schemaLabel.setPixmap(QPixmap(':/pixmaps/PulseSchemaBipolarNoBurst.png'))
            else:
                self.schemaLabel.setPixmap(QPixmap(':/pixmaps/PulseSchemaBipolarBurst.png'))

    # noinspection PyUnusedLocal
    def __toggle_output_mode(self, btn, checked):
        self.__channel.is_biphasic = self.outputModeBiphasicRadioButton.isChecked()
        for widget in self.__phase2_widgets:
            widget.setEnabled(self.outputModeBiphasicRadioButton.isChecked())
            # this ensures the values are propagated to the channel when the widget becomes enabled.
            # Not sure that this is truly needed
            if widget.isEnabled() and 'valueChanged' in widget.__dir__():
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
