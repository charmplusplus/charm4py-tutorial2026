from charm4py import charm, Chare, Array, coro, Channel
import random

class A(Chare):
    
    orig_values = {}
    final_values = {}

    def __init__(self, numchares):
        self.numchares = numchares
        self.idx = self.thisIndex[0]

        # random starting value
        self.value = random.randint(0, 100)
        self.orig = self.value

        # neighbor channels
        self.left = None
        self.right = None

        # initialize channels
        if self.idx > 0:
            left_nb = self.thisProxy[self.idx - 1]
            self.left = Channel(self, remote=left_nb)

        if self.idx < numchares - 1:
            right_nb = self.thisProxy[self.idx + 1]
            self.right = Channel(self, remote=right_nb)
    
    @coro
    def report(self, idx, value, orig):
        self.final_values[idx] = value
        self.orig_values[idx] = orig
        
    def validate(self):
        assert(self.idx == 0)
        
        old_values = sorted(self.orig_values.values())
        new_values = [self.final_values[k] for k in sorted(self.final_values)]
        
        if (old_values == new_values):
            print("Sorting is correct!")
        else:
            print("Incorrect result...")            
            differences = [(i, e1, e2) for i, (e1, e2) in enumerate(zip(old_values, new_values)) if e1 != e2]

            for (i, e1, e2) in differences:
                print("Error at index", i, ":", e2, "(actual) vs", e1, "(solution)" )
        
        
    @coro
    def work(self):
        num_iter = self.numchares
        
        for step in range(num_iter):
            even_phase = (step % 2 == 0)

            partner = None
            is_left = False
            
            # SENDER
            if (self.idx % 2 == step % 2 and self.right):
                partner = self.right
                partner.send(self.value)
                
                # wait for response from right
                for ch in charm.iwait([partner]):
                    self.value = ch.recv() # receive from the left
            
            # RECEIVER
            if (self.idx % 2 != step % 2 and self.left):
                partner = self.left
                for ch in charm.iwait([partner]):
                    other = ch.recv() # receive from the left
                    
                # send response to left
                if (other <= self.value):
                    partner.send(other)
                else:
                    partner.send(self.value)
                    self.value = other

        f = self.thisProxy[0].report(self.idx, self.value, self.orig, awaitable=True)
        f.get()

def main(args):
    numchares = 4
    
    if len(args) > 1:
        numchares = int(args[1])
        
    print("Beginning oddeven with", numchares, "chares.")
    arr = Array(A, numchares, args=[numchares])

    f = arr.work(awaitable=True)
    f.get()
    
    f = arr[0].validate(awaitable=True)
    f.get()
    
    exit()


charm.start(main)
