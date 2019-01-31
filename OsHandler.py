import subprocess
from ctypes import CDLL
import time


class OsHandler(object):

    def get_idle_time(self):
        io_stats = subprocess.Popen(["ioreg", "-c", "IOHIDSystem"], stdout=subprocess.PIPE)
        result = subprocess.Popen(["grep", "HIDIdleTime"], stdin=io_stats.stdout, stdout=subprocess.PIPE)

        io_stats.stdout.close()
        out = result.communicate()[0].decode('utf-8')
        line = out.split('\n')[0]

        nano_seconds = int(line.split('=')[-1])
        seconds = nano_seconds / 10 ** 9
        return seconds

    def lock_screen(self):
        CDLL('/System/Library/PrivateFrameworks/login.framework/Versions/Current/login').SACLockScreenImmediate()

    def is_screen_locked(self):
        # log show --style syslog --debug --info --last 15m | grep SACLockScreenImmediate
        recent_lock_event_date = self._get_last_screen_lock_event_date()
        recent_unlock_event_date = self._get_last_screen_unlock_event_date()
        return recent_lock_event_date >= recent_unlock_event_date

    def _get_last_screen_lock_event_date(self):
        io_reg_read = subprocess.Popen(["log", "show", "--style", "syslog", "--debug", "--info", "--last", "1h"],
                                       stdout=subprocess.PIPE)
        result = subprocess.Popen(["grep", "SACLockScreenImmediate"], stdin=io_reg_read.stdout, stdout=subprocess.PIPE)
        io_reg_read.stdout.close()
        le_timestamp = self._parse_last_event_date(result)
        return le_timestamp

    def _get_last_screen_unlock_event_date(self):
        io_reg_read = subprocess.Popen(["log", "show", "--style", "syslog", "--debug", "--info", "--last", "1h"],
                                       stdout=subprocess.PIPE)
        result = subprocess.Popen(["grep", "LUIAuthenticationServiceProvider deactivateWithContext:]_block_invoke"], stdin=io_reg_read.stdout, stdout=subprocess.PIPE)
        io_reg_read.stdout.close()
        le_timestamp = self._parse_last_event_date(result)
        return le_timestamp

    def _parse_last_event_date(self, result):
        lock_events = result.communicate()[0].decode('utf-8').split('\n')
        recent_lock_event = lock_events[-2]  # recent event is always the 2nd from the last
        recent_lock_event_timestamp = recent_lock_event.split(" ")[1]
        recent_lock_event_date = recent_lock_event.split(" ")[0]
        le_timestamp = time.strptime(recent_lock_event_date + " " + recent_lock_event_timestamp,
                                     '%Y-%m-%d %H:%M:%S.%f%z')
        return le_timestamp
