from enum import IntEnum
from src.PulsePal import PulsePalObject


def constrain_value(value, min_value, max_value):
    if value > max_value:
        return max_value
    elif value < min_value:
        return min_value
    else:
        return value


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
        self.pulsepal.programOutputChannelParam('isBiphasic', self.channel_id, int(value))

    @property
    def baseline_voltage(self) -> float:
        return self.__baseline_voltage

    @baseline_voltage.setter
    def baseline_voltage(self, value: float):
        self.__baseline_voltage = constrain_value(value, self.MIN_VOLTAGE, self.MAX_VOLTAGE)
        self.pulsepal.programOutputChannelParam('restingVoltage', self.channel_id, self.__baseline_voltage)

    @property
    def phase1_duration(self) -> float:
        return self.__phase1_duration

    @phase1_duration.setter
    def phase1_duration(self, value: float):
        self.__phase1_duration = constrain_value(value, self.MIN_DURATION, self.MAX_DURATION)
        self.pulsepal.programOutputChannelParam('phase1Duration', self.channel_id, self.__phase1_duration)

    @property
    def phase1_voltage(self) -> float:
        return self.__phase1_voltage

    @phase1_voltage.setter
    def phase1_voltage(self, value: float):
        self.__phase1_voltage = constrain_value(value, self.MIN_VOLTAGE, self.MAX_VOLTAGE)
        self.pulsepal.programOutputChannelParam('phase1Voltage', self.channel_id, self.__phase1_voltage)

    @property
    def phase2_voltage(self) -> float:
        return self.__phase2_voltage

    @phase2_voltage.setter
    def phase2_voltage(self, value: float):
        self.__phase2_voltage = constrain_value(value, self.MIN_VOLTAGE, self.MAX_VOLTAGE)
        self.pulsepal.programOutputChannelParam('phase2Voltage', self.channel_id, self.__phase2_voltage)

    @property
    def phase2_duration(self) -> float:
        return self.__phase2_duration

    @phase2_duration.setter
    def phase2_duration(self, value: float):
        self.__phase2_duration = constrain_value(value, self.MIN_DURATION, self.MAX_DURATION)
        self.pulsepal.programOutputChannelParam('phase2Duration', self.channel_id, self.__phase2_duration)

    @property
    def interphase_interval(self) -> float:
        return self.__interphase_interval

    @interphase_interval.setter
    def interphase_interval(self, value):
        self.__interphase_interval = constrain_value(value, self.MIN_DURATION, self.MAX_DURATION)
        self.pulsepal.programOutputChannelParam('interPhaseInterval', self.channel_id, self.__interphase_interval)

    @property
    def interpulse_interval(self) -> float:
        return self.__interpulse_interval

    @interpulse_interval.setter
    def interpulse_interval(self, value):
        self.__interpulse_interval = constrain_value(value, self.MIN_DURATION, self.MAX_DURATION)
        self.pulsepal.programOutputChannelParam('interPulseInterval', self.channel_id, self.__interpulse_interval)

    @property
    def interburst_interval(self) -> float:
        return self.__interburst_interval

    @interburst_interval.setter
    def interburst_interval(self, value):
        self.__interburst_interval = constrain_value(value, self.MIN_DURATION, self.MAX_DURATION)
        self.pulsepal.programOutputChannelParam('interBurstInterval', self.channel_id, self.interburst_interval)

    @property
    def is_burst(self) -> bool:
        return self.__burst_mode

    @is_burst.setter
    def is_burst(self, value: bool):
        self.__burst_mode = value
        if self.is_burst:
            self.pulsepal.programOutputChannelParam('burstDuration', self.channel_id, self.__burst_duration)
        else:
            self.pulsepal.programOutputChannelParam('burstDuration', self.channel_id, 0.0)

    @property
    def burst_duration(self):
        return self.__burst_duration

    @burst_duration.setter
    def burst_duration(self, value):
        self.__burst_duration = constrain_value(value, self.MIN_DURATION, self.MAX_DURATION)
        self.pulsepal.programOutputChannelParam('burstDuration', self.channel_id, self.__burst_duration)

    @property
    def train_delay(self) -> float:
        return self.__train_delay

    @train_delay.setter
    def train_delay(self, value: float):
        self.__train_delay = constrain_value(value, 0., self.MAX_DURATION)
        self.pulsepal.programOutputChannelParam('pulseTrainDelay', self.channel_id, self.__train_delay)

    @property
    def train_duration(self) -> float:
        return self.__train_duration

    @train_duration.setter
    def train_duration(self, value: float):
        self.__train_duration = constrain_value(value, self.MIN_DURATION, self.MAX_DURATION)
        self.pulsepal.programOutputChannelParam('pulseTrainDuration', self.channel_id, self.__train_duration)

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
        self.pulsepal.programOutputChannelParam('linkTriggerChannel1', self.channel_id,
                                                PulsePalTriggerChannel.TRIGGER1 in self.__trigger_source)
        self.pulsepal.programOutputChannelParam('linkTriggerChannel2', self.channel_id,
                                                PulsePalTriggerChannel.TRIGGER2 in self.__trigger_source)

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
        channels = [0]*4
        channels[self.channel_id-1] = 1
        self.pulsepal.triggerOutputChannels(*channels)


# noinspection PyPep8Naming
class DummyPulsePalObject(PulsePalObject):
    # noinspection PyMissingConstructor,PyUnusedLocal
    def __init__(self, PortName):
        pass

    def setFixedVoltage(self, channel, voltage):
        pass

    def programOutputChannelParam(self, paramName, channel, value):
        pass

    def programTriggerChannelParam(self, paramName, channel, value):
        pass

    def syncAllParams(self):
        pass

    def sendCustomPulseTrain(self, customTrainID, pulseTimes, pulseVoltages):
        pass

    def sendCustomWaveform(self, customTrainID, pulseWidth, pulseVoltages):
        pass

    def setContinuousLoop(self, channel, state):
        pass

    def triggerOutputChannels(self, channel1, channel2, channel3, channel4):
        pass

    def abortPulseTrains(self):
        pass

    def __del__(self):
        pass
