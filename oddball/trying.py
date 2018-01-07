#!/usr/bin/env python3

import oddball

data = oddball.main(None)
print(f'Obtaining memory map of {len(data)} bytes')
oddball.write_coefficients('test.coe', data)
