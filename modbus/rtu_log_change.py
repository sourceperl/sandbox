#!/usr/bin/env python3

""" Log changes on some RTU terms. """

from dataclasses import dataclass
import logging
import time
from pyModbusTCP.client import ModbusClient


# some class
class Term:
    def __init__(self, address: int, label: str) -> None:
        # public
        self.address = address
        self.label = label
        self.change = None
        # private
        self._cache = None

    def update(self, value: int) -> None:
        raise NotImplemented

    def on_change(self) -> None:
        pass


class TermBoolWord(Term):
    @dataclass
    class Change:
        bit: int
        origin: bool
        new: bool

        @property
        def ts(self):
            return 16 - self.bit

    def update(self, value: int) -> None:
        # at first run just update cache
        if self._cache is None:
            self._cache = value
            return
        # track any bit update
        if self._cache != value:
            diff_mask = self._cache ^ value
            for bit in range(15, -1, -1):
                if diff_mask & 1 << bit:
                    self._on_bit_change(bit, origin=bool(self._cache & 1 << bit), new=bool(value & 1 << bit))
            self._cache = value

    def _on_bit_change(self, bit: int, origin: bool, new: bool):
        self.change = self.Change(bit=bit, origin=origin, new=new)
        self.on_change()


class TermsBank:
    def __init__(self) -> None:
        self._terms_d = {}

    def add(self, term: Term) -> None:
        # set callback
        term.on_change = lambda: self.on_change(term)
        # keep ref to this term
        self._terms_d[term.address] = term

    def delete(self, address: int) -> None:
        del self._terms_d[address]

    def update(self, address: int, value: int) -> None:
        try:
            self._terms_d[address].update(value)
        except KeyError:
            pass

    def on_change(self, term: Term) -> None:
        if type(term) is TermBoolWord:
            logging.info(f'{term.label} TS{term.change.ts:02d} (@{term.address:d},'
                         f'{term.change.bit:d}): {term.change.origin} -> {term.change.new}')


if __name__ == '__main__':
    # modbus server
    host = '10.8.10.1'
    port = 502
    unit_id = 1
    timeout = 1.0
    debug = False
    terms_start_addr = 20608
    terms_size = 89
    skip_terms = ((20629, 20690), )

    # build terms dict
    terms_bank = TermsBank()
    terms_bank.add(TermBoolWord(address=terms_start_addr+2, label='Mot d\'état'))
    for offset, address in enumerate(range(terms_start_addr+3, terms_start_addr+terms_size)):
        # check if this address must be ignored or not
        skip = False
        for start, end in skip_terms:
            if start <= address <= end:
                skip = True
        # add term to bank
        if not skip:
            term_id = offset + 1
            terms_bank.add(TermBoolWord(address, label=f'T{term_id:02d}'))

    # logging setup
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG if debug else logging.INFO)
    logging.info('start')

    # init modbus client
    mbus_cli = ModbusClient(host=host, port=port, unit_id=unit_id, timeout=timeout, debug=debug)

    # main loop
    while True:
        try:
            ret_l = mbus_cli.read_holding_registers(reg_addr=terms_start_addr, reg_nb=terms_size)
            if not ret_l:
                raise RuntimeError('modbus error')
            for idx, value in enumerate(ret_l):
                terms_bank.update(terms_start_addr + idx, value)
            time.sleep(1.0)
        except RuntimeError as e:
            logging.error(f'{e} (retry after 5s)')
            time.sleep(5.0)
