# Copyright 2009 Shikhar Bhushan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from threading import Lock

import logging

logger = logging.getLogger('ncclient.listener')

class Subject:
    
    'Thread-safe abstact class for event-dispatching subjects'
    
    def __init__(self, listeners=[]):
        self._listeners = listeners
        self._lock = Lock()
    
    def has_listener(self, listener):
        with self._lock:
            return (listener in self._listeners)
    
    def add_listener(self, listener):
        with self._lock:
            self._listeners.append(listener)
    
    def remove_listener(self, listener):
        with self._lock:
            try:
                self._listeners.remove(listener)
            except ValueError:
                pass
    
    def dispatch(self, event, *args, **kwds):
        with self._lock:
            for l in self._listeners:
                try:
                    getattr(l, event)(*args, **kwds)
                except Exception as e:
                    logger.warning(e)

if __name__=="__main__":
    
    logging.basicConfig(level=logging.DEBUG)
    
    class Listener:
        def reply(self, data):
            print data
        def error(self, err_info):
            print err_info
    
    subject = Subject()        
    subject.add_listener(Listener())
    
    subject.dispatch('reply', 'hello world')
    subject.dispatch('error', 'bye world')
    subject.dispatch('undefined', 'happy deliverin')