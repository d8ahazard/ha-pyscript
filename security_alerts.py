FRONT_LIGHTS = ["light.front_door_east", "light.front_door_west"]


@service
def front_door_alert():
    """Alert for front door motion."""

    notify.ephemeral_notifications_group(title="Front door motion", message="There is motion at the front door.")
    pyscript.flash_lights(
        entity_ids=[
            "light.tree_lamp_left",
            "light.table_north",
            "light.office_fan_ne",
            "light.monitor_backsplash_left",
            "light.monitor_backsplash_right"
        ],
        rgb_color=[255, 50, 0]
    )


@service
def back_yard_alert():
    """Alert for back yard motion."""

    notify.ephemeral_notifications_group(title="Backyard motion", message="There is motion in the back yard.")
    pyscript.flash_lights(
        entity_ids=[
            "light.tree_lamp_left",
            "light.table_north",
            "light.office_fan_ne",
            "light.monitor_backsplash_left",
            "light.monitor_backsplash_right"
        ],
        rgb_color=[77, 0, 255]
    )


@service
def front_door_flood():
    """Turn on front door lights if off."""

    if light.outside == "off":
        def color_lights(rgb_color):
            for light_entity in FRONT_LIGHTS:
                light.turn_on(entity_id=light_entity, rgb_color=rgb_color, brightness=255)
            task.sleep(2)
        color_lights([255, 253, 253])
        color_lights([255, 45, 43])
        color_lights([255, 253, 253])


@service
def front_door_end_flood():
    """Turn off front door lights if flooding."""

    # Make list of booleans indicating whether each front door light has the flood color. Note that
    # the RGB value is slightly different here b/c this is what HA reads back after flood lighting
    # has been turned on. Apparently, there's some value fitting going on. :-/
    lights_flooding = [
        state.get(f"{light}.rgb_color") == (255, 252, 252)
        if state.get(light) == "on" else False
        for light in FRONT_LIGHTS
    ]
    # If all front door lights are in the flood state, turn them off.
    if light.outside == "on" and all(lights_flooding):
        light.turn_off(entity_id="light.outside")
