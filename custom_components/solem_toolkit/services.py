import logging
from homeassistant.core import HomeAssistant, ServiceCall
import sys
import asyncio
import struct
from bleak import BleakClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
characteristic_uuid = '2fc20002-a5eb-4a8f-8ee2-7075ffce4f5f'

async def async_list_characteristics(call: ServiceCall):
    device_mac = call.data.get("device_mac")
    async with BleakClient(device_mac, timeout=20.0) as client:
        if client.is_connected:
            _LOGGER.debug("Connected: True")
            _LOGGER.debug("Listing services")
            services = client.services
            for service in services:
                _LOGGER.info(f"Service: {service.uuid}")
                for char in service.characteristics:
                    _LOGGER.info(f"  Characteristic: {char.uuid}")

            _LOGGER.debug("Success")
        else:
            _LOGGER.error("Failed connecting!")

async def async_turn_off_permanent(call: ServiceCall):
    device_mac = call.data.get("device_mac")
    async with BleakClient(device_mac, timeout=20.0) as client:
        if client.is_connected:
            _LOGGER.debug("Connected: True")
            _LOGGER.debug("writing command: Turn off permanent")
            command = struct.pack(">HBBBH", 0x3105, 0xc0, 0x00, 0x00, 0x0000)
            await client.write_gatt_char(characteristic_uuid, command)
            
            _LOGGER.debug("committing")
            command = struct.pack(">BB", 0x3b, 0x00)
            await client.write_gatt_char(characteristic_uuid, command)

            _LOGGER.debug("Success")
        else:
            _LOGGER.error("Failed connecting!")

async def async_turn_off_x_days(call: ServiceCall):
    device_mac = call.data.get("device_mac")
    days = call.data.get("days")
    async with BleakClient(device_mac, timeout=20.0) as client:
        if client.is_connected:
            _LOGGER.debug("Connected: True")
            _LOGGER.debug("writing command: Turn off permanent")
            command = struct.pack(">HBBBH", 0x3105, 0xc0, 0x00, days & 0xFF, 0x0000)
            await client.write_gatt_char(characteristic_uuid, command)
            
            _LOGGER.debug("committing")
            command = struct.pack(">BB", 0x3b, 0x00)
            await client.write_gatt_char(characteristic_uuid, command)

            _LOGGER.debug("Success")
        else:
            _LOGGER.error("Failed connecting!")
        
async def async_turn_on(call: ServiceCall):
    device_mac = call.data.get("device_mac")
    async with BleakClient(device_mac, timeout=20.0) as client:
        if client.is_connected:
            _LOGGER.debug("Connected: True")
            _LOGGER.debug("writing command: Turn on")
            command = struct.pack(">HBBBH",0x3105,0xa0,0x00,0x01,0x0000)
            await client.write_gatt_char(characteristic_uuid, command)
            
            _LOGGER.debug("committing")
            command = struct.pack(">BB", 0x3b, 0x00)
            await client.write_gatt_char(characteristic_uuid, command)

            _LOGGER.debug("Success")
        else:
            _LOGGER.error("Failed connecting!")

async def async_sprinkle_station_x_for_y_minutes(call: ServiceCall):
    device_mac = call.data.get("device_mac")
    station = call.data.get("station")
    minutes = call.data.get("minutes")
    async with BleakClient(device_mac, timeout=20.0) as client:
        if client.is_connected:
            _LOGGER.debug("Connected: True")
            _LOGGER.debug(f"writing command: Sprinkle station {station} for {minutes} minutes")
            command = struct.pack(">HBBBH",0x3105,0x12,station & 0xFF,0x00,(minutes * 60) & 0xFFFF)
            await client.write_gatt_char(characteristic_uuid, command)

            _LOGGER.debug("committing")
            command = struct.pack(">BB", 0x3b, 0x00)
            await client.write_gatt_char(characteristic_uuid, command)

            _LOGGER.debug("Success")
        else:
            _LOGGER.error("Failed connecting!")

async def async_sprinkle_all_stations_for_y_minutes(call: ServiceCall):
    device_mac = call.data.get("device_mac")
    minutes = call.data.get("minutes")
    async with BleakClient(device_mac, timeout=20.0) as client:
        if client.is_connected:
            _LOGGER.debug("Connected: True")
            _LOGGER.debug(f"writing command: Sprinkle all stations for {minutes} minutes")
            command = struct.pack(">HBBBH", 0x3105, 0x11, 0x00, 0x00,(minutes * 60) & 0xFFFF)
            await client.write_gatt_char(characteristic_uuid, command)

            _LOGGER.debug("committing")
            command = struct.pack(">BB", 0x3b, 0x00)
            await client.write_gatt_char(characteristic_uuid, command)

            _LOGGER.debug("Success")
        else:
            _LOGGER.error("Failed connecting!")
        
async def async_run_program_x(call: ServiceCall):
    device_mac = call.data.get("device_mac")
    program = call.data.get("program")
    async with BleakClient(device_mac, timeout=20.0) as client:
        if client.is_connected:
            _LOGGER.debug("Connected: True")
            _LOGGER.debug(f"writing command: Run program {program}")
            command = struct.pack(">HBBBH", 0x3105, 0x14, 0x00, program & 0xFF, 0x0000)
            await client.write_gatt_char(characteristic_uuid, command)

            _LOGGER.debug("committing")
            command = struct.pack(">BB", 0x3b, 0x00)
            await client.write_gatt_char(characteristic_uuid, command)

            _LOGGER.debug("Success")
        else:
            _LOGGER.error("Failed connecting!")

async def async_stop_manual_sprinkle(call: ServiceCall):
    device_mac = call.data.get("device_mac")
    async with BleakClient(device_mac, timeout=20.0) as client:
        if client.is_connected:
            _LOGGER.debug("Connected: True")
            _LOGGER.debug("writing command: Stop manual sprinkle")
            command = struct.pack(">HBBBH",0x3105,0x15,0x00,0xff,0x0000)
            await client.write_gatt_char(characteristic_uuid, command)

            _LOGGER.debug("committing")
            command = struct.pack(">BB", 0x3b, 0x00)
            await client.write_gatt_char(characteristic_uuid, command)

            _LOGGER.debug("Success")
        else:
            _LOGGER.error("Failed connecting!")

def async_setup_services(hass: HomeAssistant):
    hass.services.async_register(DOMAIN, "list_characteristics", async_list_characteristics)
    hass.services.async_register(DOMAIN, "turn_off_permanent", async_turn_off_permanent)
    hass.services.async_register(DOMAIN, "turn_off_x_days", async_turn_off_x_days)
    hass.services.async_register(DOMAIN, "turn_on", async_turn_on)
    hass.services.async_register(DOMAIN, "sprinkle_station_x_for_y_minutes", async_sprinkle_station_x_for_y_minutes)
    hass.services.async_register(DOMAIN, "sprinkle_all_stations_for_y_minutes", async_sprinkle_all_stations_for_y_minutes)
    hass.services.async_register(DOMAIN, "run_program_x", async_run_program_x)
    hass.services.async_register(DOMAIN, "stop_manual_sprinkle", async_stop_manual_sprinkle)
