#
# Copyright 2021-2023 Picovoice Inc.
#
# You may not use this file except in compliance with the license. A copy of the license is located in the "LICENSE"
# file accompanying this source.
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#

import argparse
import sys
import struct
import wave
from threading import Thread

import pvcobra
from pvrecorder import PvRecorder
from PyQt6.QtCore import QObject, QThread, pyqtSignal, Qt, QTimer

class CobraDemo(QObject):
    """
    Microphone Demo for Cobra voice activity detection engine.
    """
    voiceCapture = pyqtSignal(object)
    def __init__(
            self,
            library_path,
            access_key,
            output_path=None,
            input_device_index=None):
        """
        Constructor.

        :param library_path: Absolute path to Cobra's dynamic library.
        :param access_key AccessKey obtained from Picovoice Console.
        :param output_path: If provided recorded audio will be stored in this location at the end of the run.
        :param input_device_index: Optional argument. If provided, audio is recorded from this input device. Otherwise,
        the default audio input device is used.
        """

        super().__init__()

        self._library_path = library_path
        self._access_key = access_key
        self._input_device_index = input_device_index
        self._output_path = output_path

    def run(self):
        """
         Creates an input audio stream, instantiates an instance of Cobra object, and monitors the audio stream for
         voice activities.
         """

        recorder = None
        wav_file = None

        try:
            cobra = pvcobra.create(access_key=self._access_key, library_path=self._library_path)
        except pvcobra.CobraInvalidArgumentError as e:
            print(e)
            raise e
        except pvcobra.CobraActivationError as e:
            print("AccessKey activation error")
            raise e
        except pvcobra.CobraActivationLimitError as e:
            print("AccessKey '%s' has reached it's temporary device limit" % self._access_key)
            raise e
        except pvcobra.CobraActivationRefusedError as e:
            print("AccessKey '%s' refused" % self._access_key)
            raise e
        except pvcobra.CobraActivationThrottledError as e:
            print("AccessKey '%s' has been throttled" % self._access_key)
            raise e
        except pvcobra.CobraError as e:
            print("Failed to initialize Cobra")
            raise e

        print("Cobra version: %s" % cobra.version)

        try:
            recorder = PvRecorder(frame_length=512, device_index=self._input_device_index)
            recorder.start()

            if self._output_path is not None:
                wav_file = wave.open(self._output_path, "w")
                wav_file.setparams((1, 2, 16000, 512, "NONE", "NONE"))

            print("Listening...")
            while True:
                pcm = recorder.read()

                if wav_file is not None:
                    wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

                voice_probability = cobra.process(pcm)
                percentage = voice_probability * 100
                bar_length = int((percentage / 10) * 3)
                empty_length = 30 - bar_length
                if percentage >25:
                    self.voiceCapture.emit(1)
                else:
                    self.voiceCapture.emit(0)
                # sys.stdout.flush()

        except KeyboardInterrupt:
            print('Stopping ...')
        finally:
            if cobra is not None:
                cobra.delete()

            if wav_file is not None:
                wav_file.close()

            if recorder is not None:
                recorder.delete()

    # @classmethod
    # def show_available_devices(cls):
    #     devices = PvRecorder.get_available_devices()
    #     for i in range(len(devices)):
    #         print('index: %d, device name: %s' % (i, devices[i]))


def main():

    CobraDemo(
        library_path=None,
        access_key="4H7XExZ76UQe2E4SFAM7vsItIZgSLrbmvA2A0psSaM/eLi9mvIPGgQ==",
        output_path=None,
        input_device_index=-1).run()


if __name__ == '__main__':
    main()
