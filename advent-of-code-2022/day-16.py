from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List
import re
import time # RM ME


@dataclass
class Valve:
    name: str
    rate: int
    tunnels: List[str]
    is_open: bool


@dataclass
class State:
    current: str
    minutes: int
    valves: Dict[str, Valve]

    def flow(self) -> int:
        return sum([v.rate * int(v.is_open) for v in self.valves.values()])

MAX_MINUTES = 30

def dfs(state: State) -> int:
    #time.sleep(0.2)
    result = state.flow()
    print("DFS:", state)

    # Max time reached.
    if state.minutes == MAX_MINUTES:
        print(f"\tMax time reached @ name={state.current}, flow={result}")
        return result

    # All usable valves are open.
    open_valves = [v for v in state.valves.values() if v.is_open]
    flow_valves = [v for v in state.valves.values() if v.rate != 0]
    if len(open_valves) == len(flow_valves):
        print(f"\tAll usable valves open @ time={state.minutes} min, name={state.current}, flow={result}")
        return result * (MAX_MINUTES - state.minutes)

    # Action opening the current valve.
    if not state.valves[state.current].is_open and state.valves[state.current].rate != 0:
        print(f"\tOpen {state.current}...")
        next = deepcopy(state)
        next.minutes += 1
        next.valves[next.current].is_open = True
        result = max(result, result + dfs(next))

    # Actions moving to other valves.
    for name in state.valves[state.current].tunnels:
        print(f"\tMove to {name}...")
        next = deepcopy(state)
        next.minutes += 1
        next.current = name
        result = max(result, result + dfs(next))

    return result


def main():
    with open("day-16.input") as f:
        lines = f.readlines();
    lines = [s.strip() for s in lines]

    LINE_RE = re.compile("^Valve (\S\S) has flow rate=(\d+); tunnels? leads? to valves? (.*)$")
    valves = dict()
    for line in lines:
        print(line)
        match = LINE_RE.match(line)
        name = match[1]
        rate = int(match[2])
        tunnels = match[3].split(", ")
        valves[name] = Valve(name, rate, tunnels, False)

    state = State(LINE_RE.match(lines[0])[1], 0, valves)
    print("INITIAL:", state)
    print(dfs(state))


if __name__ == "__main__":
    main()
