import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor
from esphome.const import (
    CONF_ID,
    CONF_MOISTURE,
    DEVICE_CLASS_DISTANCE,
    DEVICE_CLASS_MOISTURE,
    STATE_CLASS_MEASUREMENT,
    UNIT_MILLIMETER,
    UNIT_PERCENT,
)

DEPENDENCIES = ["i2c"]

CONF_WATER_LEVEL = "water_level"
CONF_LOW_ADDRESS = "low_address"
CONF_HIGH_ADDRESS = "high_address"
CONF_CAPACITOR_MAX_VALUE = "capacitor_max_value"

grove_water_level_sensor_ns = cg.esphome_ns.namespace("grove_water_level")
GroveWaterLevelI2CComponent = grove_water_level_sensor_ns.class_(
    "GroveWaterLevelI2CComponent", cg.PollingComponent
)


def dual_address_i2c_device_schema(default_low_address, default_high_address):
    """Create a schema for a i2c device that uses two addresses.

    :return: The i2c device schema, `extend` this in your config schema.
    """
    schema = {
        cv.GenerateID(i2c.CONF_I2C_ID): cv.use_id(i2c.I2CBus),
    }
    if default_low_address is None:
        schema[cv.Required(CONF_LOW_ADDRESS)] = cv.i2c_address
    else:
        schema[cv.Optional(CONF_LOW_ADDRESS, default=default_low_address)] = (
            cv.i2c_address
        )
    if default_high_address is None:
        schema[cv.Required(CONF_HIGH_ADDRESS)] = cv.i2c_address
    else:
        schema[cv.Optional(CONF_HIGH_ADDRESS, default=default_high_address)] = (
            cv.i2c_address
        )
    return cv.Schema(schema)


CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.Optional(CONF_WATER_LEVEL): sensor.sensor_schema(
                unit_of_measurement=UNIT_MILLIMETER,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_DISTANCE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_MOISTURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_MOISTURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_CAPACITOR_MAX_VALUE, default=248): cv.int_range(
                min=0, max=255
            ),
        }
    )
    .extend(cv.polling_component_schema("60s"))
    .extend(
        dual_address_i2c_device_schema(
            default_low_address=0x77,
            default_high_address=0x78,
        )
    )
    .extend({cv.GenerateID(): cv.declare_id(GroveWaterLevelI2CComponent)})
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    parent = await cg.get_variable(config[i2c.CONF_I2C_ID])
    cg.add(var.set_i2c_bus(parent))
    cg.add(var.set_low_i2c_address(config[CONF_LOW_ADDRESS]))
    cg.add(var.set_high_i2c_address(config[CONF_HIGH_ADDRESS]))
    cg.add(var.set_capacitor_max_value(config[CONF_CAPACITOR_MAX_VALUE]))

    if level_config := config.get(CONF_WATER_LEVEL):
        sens = await sensor.new_sensor(level_config)
        cg.add(var.set_level_sensor(sens))
    if moisture_config := config.get(CONF_MOISTURE):
        sens = await sensor.new_sensor(moisture_config)
        cg.add(var.set_moisture_sensor(sens))
