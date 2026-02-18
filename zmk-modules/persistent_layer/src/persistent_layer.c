/*
 * Persists the active layer across deep sleep by saving it to settings storage
 * on sleep and restoring it on boot. Deep sleep clears RAM, so without this
 * the keyboard always wakes on layer 0.
 */

#include <zephyr/init.h>
#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

#include <zmk/activity.h>
#include <zmk/event_manager.h>
#include <zmk/events/activity_state_changed.h>
#include <zmk/keymap.h>

LOG_MODULE_REGISTER(persistent_layer, LOG_LEVEL_INF);

/* The layer index that was last written to flash. Initialized to 0 to match
 * the hardware default on first boot, avoiding a spurious write. Updated by
 * the settings set callback so subsequent boots skip writes when unchanged. */
static zmk_keymap_layer_index_t last_persisted = 0;

#if IS_ENABLED(CONFIG_SETTINGS)

#include <zephyr/settings/settings.h>

static zmk_keymap_layer_index_t saved_layer = 0;

static int persistent_layer_settings_set(const char *name, size_t length,
                                         settings_read_cb read_cb, void *cb_arg) {
    const char *next;
    if (settings_name_steq(name, "active", &next) && !next) {
        if (length != sizeof(saved_layer)) {
            return -EINVAL;
        }
        int rc = read_cb(cb_arg, &saved_layer, sizeof(saved_layer));
        if (rc >= 0) {
            last_persisted = saved_layer;
        }
        return MIN(rc, 0);
    }
    return -ENOENT;
}

static int persistent_layer_settings_commit(void) {
    LOG_INF("Restoring layer %d", saved_layer);
    return zmk_keymap_layer_to(saved_layer);
}

SETTINGS_STATIC_HANDLER_DEFINE(persistent_layer, "persistent_layer", NULL,
                                persistent_layer_settings_set, persistent_layer_settings_commit,
                                NULL);

#endif /* IS_ENABLED(CONFIG_SETTINGS) */

static int persistent_layer_event_listener(const zmk_event_t *eh) {
    if (!as_zmk_activity_state_changed(eh)) {
        return -ENOTSUP;
    }

    if (zmk_activity_get_state() != ZMK_ACTIVITY_SLEEP) {
        return 0;
    }

#if IS_ENABLED(CONFIG_SETTINGS)
    zmk_keymap_layer_index_t current = zmk_keymap_highest_layer_active();
    if (current == last_persisted) {
        return 0;
    }

    LOG_INF("Saving layer %d before sleep", current);
    int rc = settings_save_one("persistent_layer/active", &current, sizeof(current));
    if (rc == 0) {
        last_persisted = current;
    } else {
        LOG_ERR("Failed to save layer: %d", rc);
    }
#endif /* IS_ENABLED(CONFIG_SETTINGS) */

    return 0;
}

ZMK_LISTENER(persistent_layer, persistent_layer_event_listener);
ZMK_SUBSCRIPTION(persistent_layer, zmk_activity_state_changed);
