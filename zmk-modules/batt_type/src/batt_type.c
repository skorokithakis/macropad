#define DT_DRV_COMPAT zmk_behavior_batt_type

#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/sensor.h>
#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/sys/util.h>

#include <drivers/behavior.h>
#include <zmk/behavior_queue.h>
#include <zmk/keymap.h>

#include <dt-bindings/zmk/keys.h>

#define ZMK_CHOSEN_BATTERY DT_CHOSEN(zmk_battery)

#if !DT_NODE_EXISTS(ZMK_CHOSEN_BATTERY)
#error "No /chosen zmk,battery found. Your board/shield must define it."
#endif

static const struct device *bat = DEVICE_DT_GET(ZMK_CHOSEN_BATTERY);
static const char *kp_behavior = DEVICE_DT_NAME(DT_NODELABEL(kp));

/* Convenience: enqueue a tap of &kp <keycode> */
static int enqueue_kp_tap(uint32_t keycode, struct zmk_behavior_binding_event ev) {
    struct zmk_behavior_binding b = {
        .behavior_dev = kp_behavior,
        .param1 = keycode,
        .param2 = 0,
    };

    /* tap == press then release; the queue API takes "pressed" bool and wait time */
    int rc = zmk_behavior_queue_add(&ev, b, true, 0);
    if (rc) return rc;
    return zmk_behavior_queue_add(&ev, b, false, 0);
}

static int enqueue_ascii(char c, struct zmk_behavior_binding_event ev) {
    switch (c) {
    case '0': return enqueue_kp_tap(N0, ev);
    case '1': return enqueue_kp_tap(N1, ev);
    case '2': return enqueue_kp_tap(N2, ev);
    case '3': return enqueue_kp_tap(N3, ev);
    case '4': return enqueue_kp_tap(N4, ev);
    case '5': return enqueue_kp_tap(N5, ev);
    case '6': return enqueue_kp_tap(N6, ev);
    case '7': return enqueue_kp_tap(N7, ev);
    case '8': return enqueue_kp_tap(N8, ev);
    case '9': return enqueue_kp_tap(N9, ev);
    case '.': return enqueue_kp_tap(DOT, ev);
    case ':': return enqueue_kp_tap(LS(SEMI), ev);
    case 'a': return enqueue_kp_tap(A, ev);
    case 'e': return enqueue_kp_tap(E, ev);
    case 'r': return enqueue_kp_tap(R, ev);
    case 't': return enqueue_kp_tap(T, ev);
    case 'y': return enqueue_kp_tap(Y, ev);
    case 'B': return enqueue_kp_tap(LS(B), ev);
    case 'V': return enqueue_kp_tap(LS(V), ev);
    case ' ': return enqueue_kp_tap(SPACE, ev);
    default:  return 0;
    }
}

static int batt_type_pressed(struct zmk_behavior_binding *binding,
                             struct zmk_behavior_binding_event event) {
    ARG_UNUSED(binding);

    if (!device_is_ready(bat)) {
        const char *msg = "Battery: 0.00V";
        for (const char *p = msg; *p; p++) enqueue_ascii(*p, event);
        return ZMK_BEHAVIOR_OPAQUE;
    }

    int rc = sensor_sample_fetch_chan(bat, SENSOR_CHAN_GAUGE_VOLTAGE);
    if (rc) {
        const char *msg = "Battery: 0.00V";
        for (const char *p = msg; *p; p++) enqueue_ascii(*p, event);
        return ZMK_BEHAVIOR_OPAQUE;
    }

    struct sensor_value v = {0};
    rc = sensor_channel_get(bat, SENSOR_CHAN_GAUGE_VOLTAGE, &v);
    if (rc) {
        const char *msg = "Battery: 0.00V";
        for (const char *p = msg; *p; p++) enqueue_ascii(*p, event);
        return ZMK_BEHAVIOR_OPAQUE;
    }

    /* v is in volts as (val1 + val2 * 1e-6). Format as X.XXV */
    int32_t microvolts = (int32_t)v.val1 * 1000000 + v.val2;
    int32_t centivolts = (microvolts + 5000) / 10000;
    int32_t whole = centivolts / 100;
    int32_t frac = centivolts % 100;

    char out[20];
    int n = snprintk(out, sizeof(out), "Battery: %d.%02dV", whole, frac);
    for (int i = 0; i < n; i++) {
        enqueue_ascii(out[i], event);
    }

    return ZMK_BEHAVIOR_OPAQUE;
}

static const struct behavior_driver_api batt_type_api = {
    .binding_pressed = batt_type_pressed,
    .binding_released = NULL,
};

BEHAVIOR_DT_INST_DEFINE(0, NULL, NULL, NULL, NULL, POST_KERNEL,
                        CONFIG_KERNEL_INIT_PRIORITY_DEFAULT, &batt_type_api);
