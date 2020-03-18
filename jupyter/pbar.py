class Pbar:

    def __init__(self, it, length=None, refresh_rate=None, pbar_width=50, action_names=None):
        self.it = iter(it)
        self.length = length or len(it)
        self.pbar_width = pbar_width
        self.refresh_rate = refresh_rate or self.length // pbar_width or 1

        if action_names is not None and len(action_names) != self.length:
            raise RuntimeError('invalid configuration')
        else:
            self.action_names = action_names

        self.iteration = 0

        self.show_progress()

    def show_progress(self):
        threshold = (self.iteration / self.length) * self.pbar_width

        output = '['
        for i in range(self.pbar_width):
            if i < threshold:
                output += '='
            else:
                output += ' '
        output += ']'

        if self.iteration != self.length and self.action_names is not None:
            output += f' (processing: {self.action_names[self.iteration]})'

        output += f' -- {self.iteration} / {self.length}'

        if self.iteration == self.length:
            output += ' -- (finished)\n'

        print('\r' + output, end='')

    def __iter__(self):
        return self

    def __next__(self):
        if self.iteration % self.refresh_rate == 0 or self.iteration == self.length:
            self.show_progress()

        self.iteration += 1
        return next(self.it)
