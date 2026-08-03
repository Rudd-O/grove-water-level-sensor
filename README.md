# ESPHome support for Seeed Studio Grove water level sensor

This project integrates the well-known
[Grove water level sensor](https://wiki.seeedstudio.com/Grove-Water-Level-Sensor/)
from Seeed Studio into ESPHome.

![Photo of the sensor](images/Grove-Water-Level-Sensor-10CM-wiki.jpg)

This sensor is a capacitance-based sensor with a conformal coating
that allows it to be submerged in water without deterioration common
to resistive sensors.

The sensor uses two I2C addresses (0x77 and 0x78) to probe a total of
twenty distinct capacitors across its surface (10 cm of length).

**I discourage the use of this sensor**.  I found two problems with it:

1. On at least the Wemos D1 Mini ESP32, the low device bytes (8) cannot
   be read reliably -- they all come out as 255.  That makes the sensor
   unable to detect any water level below about 40%.  On such devices,
   it may help to set the I2C frequency to 200 kHz to get some data
   readout, but then the readout is unstable.
2. The sensor has a catastrophic design issue -- if the sensor boots up
   submerged in water, then none of the capacitors under water read any
   value above zero, therefore code reading out the level from the sensor
   shows a water level of 0 mm.

## How do I program my ESPHome device to use the sensor?

Use your own version of this sample ESPHome sketch:

```yaml
esphome:
  name: water-level
  friendly_name: Water level

external_components:
  - source:
      type: git
      url: https://github.com/Rudd-O/grove-water-level-sensor
      ref: master
    components:
    - grove_water_level

esp32:
  board: nodemcu-32s
  framework:
    type: esp-idf

# Enable logging
logger:
  level: debug

# Enable Home Assistant API
api:
  encryption:
    key: !secret api_key

ota:
  password: !secret ota_password

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

i2c:
  sda: GPIO21
  scl: GPIO22
  scan: true
  id: bus_a

sensor:
- platform: grove_water_level
  water_level:
    # This indicates the water level by measuring capacitance bottom to top
    # and ignoring capacitance from capacitive cells above the water line,
    # which may read high capacitance due to water droplets.
    name: Water level
  moisture:
    # This indicates moisture by measuring capacitance across all capacitive
    # cells, summing each cell's 0-100% value and dividing by the number of cells.
    name: Moisture
```

## Configuration parameters for sensor platform `grove_water_level`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `i2c_id` | [ID](https://esphome.io/guides/configuration-types#config-id) | (auto) | ID of the I2C bus to use. |
| `low_address` | [I2C Address](https://esphome.io/components/i2c.html) | `0x77` (optional) | Optional low I2C address if not using defaults. |
| `high_address` | [I2C Address](https://esphome.io/components/i2c.html) | `0x78` (optional) | Optional high I2C address if not using defaults. |
| `water_level` | [Sensor Config](https://esphome.io/components/sensor/index.html) | None | Optional sensor entity for water level (unit: mm, device class: distance). |
| `moisture` | [Sensor Config](https://esphome.io/components/sensor/index.html) | None | Optional sensor entity for moisture (unit: %, device class: moisture). |
| `capacitor_max_value` | int | `248` | Maximum capacitor value, range 0–255. See below. |

In addition, this component inherits standard options from ESPHome's [Polling Component](https://esphome.io/components/polling_component) (default update interval: 60s) and [I2C Device](https://esphome.io/components/i2c.html) base configurations.

### Tuning `capacitor_max_value`

To check what is the appropriate value for your sensor, set up your sensor to refresh every 1 second, then submerge the sensor in 10 cm of water while looking at the debug output of your ESP device, and check the values read.  Pick the minimum value across all 20 capacitor values.  The default shipped with this component is 248 which proved to be the smallest capacitance of all of my sensor's capacitors when fully submerged.

## Development

To run Python checks locally:

```bash
pip install ruff
ruff check .
```
