class FSM:
    def __init__(self, final_states: set, states: list = None):
        if states is None:
            self.states = [dict()]
        else:
            self.states = states
        self.final_states = final_states

    def add_word(self, word):
        cur_state = self.states[0]
        for i, x in enumerate(word):
            next_state = cur_state.get(x)
            if next_state is None:
                cur_state[x] = len(self.states)
                self.states.append(dict())
                next_state = -1
            cur_state = self.states[next_state]

    def analyze_word(self, word):
        res = []
        cur_state = self.states[0]
        for i, x in enumerate(word):
            for short_id in self.final_states & cur_state.keys():
                for b in self.states[cur_state[short_id]].keys():
                    res.append((i, b, short_id))
            next_state = cur_state.get(x)
            if next_state is None:
                return res
            cur_state = self.states[next_state]
        for short_id in self.final_states & cur_state.keys():
            for b in self.states[cur_state[short_id]].keys():
                res.append((len(word), b, short_id))
        return res

    def to_dict(self):
        return {"states": self.states, "final_states": list(self.final_states)}

    @classmethod
    def from_dict(cls, d: dict):
        return cls(final_states=set(d["final_states"]), states=d["states"])
