import time
import random


class Producer(object):
    def __init__(self, output, span=1):
        self.output = output
        self.span = span

    def run(self):
        with open(self.output, mode='w') as file_:
            print('start produce')
            i = 0
            while True:
                ts = time.time()
                file_.writelines(">>>%s, %s<<<\n" % (ts, random.random()))
                file_.flush()
                if i % 10 == 0:
                    print('produce %s lines' % i)
                i += 1
                time.sleep(self.span)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser("mock log producer.")
    parser.add_argument('-o', '--output', help='output file')
    parser.add_argument('-s', '--span', help='output span second', default=1)
    args = parser.parse_args()

    producer = Producer(args.output, args.span)
    producer.run()
