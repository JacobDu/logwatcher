import threading
import time


class Watcher(threading.Thread):
    start_flag = False
    lock = threading.Lock()
    queue = []

    def __init__(self, target, span=1):
        super(Watcher, self).__init__()
        self.log_segment = []
        self.target = target
        self.span = span
        self.daemon = True

    def run(self):
        with open(self.target, mode='r') as file_:
            print('watcher started! target=%s' % self.target)
            # move to the end of file
            file_.seek(0, 2)
            while True:
                line = file_.readline()
                if line:
                    self.parse_logs(line)
                else:
                    time.sleep(1)

    def parse_logs(self, line):
        # comments
        if line.startswith('#'):
            return
        # segment start
        if line.startswith('>>>'):
            self.start_flag = True
            self.log_segment = []
        # data
        self.log_segment.append(line)
        if line.strip().endswith('<<<') and self.start_flag:
            self.start_flag = False
            self.parse_segment()

    def parse_segment(self):
        data = {}
        split = self.log_segment[0].strip().strip('<<<').strip('>>>').split(',')
        data['ts'] = int(float(split[0])) * 1000
        data['value'] = float(split[1].strip())
        if self.lock.acquire(1):
            if len(self.queue) > 30:
                self.queue.pop(0)
            self.queue.append(data)
            self.lock.release()

    def fetch(self, timestamp):
        result = []
        if self.lock.acquire(1):
            for data in self.queue:
                if data['ts'] > timestamp:
                    result.append(data)
            self.lock.release()
        return result


if __name__ == '__main__':
    watcher = Watcher('logs/tmp.log', span=2)
    watcher.start()
