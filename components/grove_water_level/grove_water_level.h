#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/i2c/i2c.h"
#include "esphome/components/i2c/i2c_bus.h"

namespace esphome::grove_water_level
{

    class GroveWaterLevelI2CComponent : public esphome::PollingComponent
    {
    public:
        /// @brief We store the address of the device on the bus
        /// @param address of the device
        void set_low_i2c_address(uint8_t address) { this->low_device_.set_i2c_address(address); }

        /// @brief We store the address of the device on the bus
        /// @param address of the device
        void set_high_i2c_address(uint8_t address) { this->high_device_.set_i2c_address(address); }

        /// @brief Returns the I2C address of the object.
        /// @return the I2C address
        uint8_t get_low_i2c_address() const { return this->low_device_.get_i2c_address(); }

        /// @brief Returns the I2C address of the object.
        /// @return the I2C address
        uint8_t get_high_i2c_address() const { return this->high_device_.get_i2c_address(); }

        /// @brief we store the pointer to the I2CBus to use
        /// @param bus pointer to the I2CBus object
        void set_i2c_bus(esphome::i2c::I2CBus *bus)
        {
            this->low_device_.set_i2c_bus(bus);
            this->high_device_.set_i2c_bus(bus);
        }

        /// @brief we store the pointer to the I2CBus to use
        /// @param bus pointer to the I2CBus object
        void set_capacitor_max_value(uint8_t value)
        {
            this->capacitor_max_value_ = value;
        }

        void set_level_sensor(esphome::sensor::Sensor *level_sensor) { this->level_sensor_ = level_sensor; }
        void set_moisture_sensor(esphome::sensor::Sensor *moisture_sensor) { this->moisture_sensor_ = moisture_sensor; }

        // ========== INTERNAL METHODS ==========
        // (In most use cases you won't need these)
        void dump_config() override;
        void update() override;

    protected:
        /// Calculate the relative humidity in % using the provided i2c values.
        void read_data_();

        esphome::sensor::Sensor *level_sensor_{nullptr};
        esphome::sensor::Sensor *moisture_sensor_{nullptr};

        esphome::i2c::I2CDevice low_device_;
        esphome::i2c::I2CDevice high_device_;

        uint8_t read_data[20];
        uint8_t capacitor_max_value_;
        i2c::ErrorCode read_status;
    };

} // namespace esphome::grove_water_level
