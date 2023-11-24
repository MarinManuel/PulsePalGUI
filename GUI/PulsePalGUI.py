from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QGroupBox, QRadioButton, QPushButton, QComboBox, QButtonGroup

from GUI.scientific_spinbox import ScienDSpinBox
from src.PulsePalHelpers import PulsePalOutputChannel, PulsePalCustomTrainID, PulsePalTriggerSource, PulsePalTriggerMode


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
    trigger1RadioButton: QRadioButton
    trigger2RadioButton: QRadioButton
    triggerModeComboBox: QComboBox
    triggerOffRadioButton: QRadioButton

    outputModeGroupBox: QGroupBox
    outputModeBiphasicRadioButton: QRadioButton
    outputModeMonophasicRadioButton: QRadioButton

    customTrainButtonGroup: QButtonGroup
    outputModeButtonGroup: QButtonGroup
    triggerSourceButtonGroup: QButtonGroup

    def __init__(self, channel: PulsePalOutputChannel):
        super().__init__()
        # noinspection SpellCheckingInspection
        uic.loadUi("GUI/channelwidget.ui", self)
        self.__channel = channel
        self.__phase2_widgets = [self.phase2VoltageSpinBox, self.phase2DurationSpinBox, self.interPhaseIntervalSpinBox]

        # SLOTS
        self.outputModeButtonGroup.buttonToggled.connect(self.__toggle_output_mode)
        self.burstModeGroupBox.toggled.connect(self.__toggle_burst_mode)
        self.triggerSourceButtonGroup.buttonToggled.connect(self.__toggle_trigger_source)
        self.triggerModeComboBox.currentIndexChanged.connect(self.__toggle_trigger_mode)

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

        self.triggerOffRadioButton.setChecked(self.__channel.trigger_source == PulsePalTriggerSource.OFF)
        self.trigger1RadioButton.setChecked(self.__channel.trigger_source == PulsePalTriggerSource.TRIGGER1)
        self.trigger2RadioButton.setChecked(self.__channel.trigger_source == PulsePalTriggerSource.TRIGGER2)
        self.triggerModeComboBox.setCurrentIndex(self.__channel.trigger_mode)

        self.outputModeBiphasicRadioButton.setChecked(self.__channel.is_biphasic)
        self.outputModeMonophasicRadioButton.setChecked(not self.__channel.is_biphasic)

    # noinspection PyUnusedLocal
    def __toggle_output_mode(self, btn, checked):
        for widget in self.__phase2_widgets:
            widget.setEnabled(self.outputModeBiphasicRadioButton.isChecked())

    def __toggle_burst_mode(self, checked):
        self.__channel.is_burst = checked

    def __toggle_trigger_source(self, btn, checked):
        if checked:
            if btn is self.triggerOffRadioButton:
                source = PulsePalTriggerSource.OFF
            elif btn is self.trigger1RadioButton:
                source = PulsePalTriggerSource.TRIGGER1
            elif btn is self.trigger2RadioButton:
                source = PulsePalTriggerSource.TRIGGER2
            else:
                raise ValueError("Could not figure out the trigger source, aborting.")
            self.__channel.trigger_source = source

    def __toggle_trigger_mode(self, selected_id: int):
        self.__channel.trigger_mode = PulsePalTriggerMode(selected_id)
