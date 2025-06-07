from machine import I2C

i2c: I2C

def get_i2c_bus() -> I2C: ...

def i2c_has_addr(i2c_bus: I2C, addr: int) -> bool: ...