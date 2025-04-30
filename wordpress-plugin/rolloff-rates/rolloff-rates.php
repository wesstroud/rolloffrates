<?php
/**
 * Plugin Name: RollOff Rates
 * Plugin URI: https://rolloffrates.com
 * Description: Display dumpster rental pricing and information from external database
 * Version: 1.0.0
 * Author: RollOff Rates
 * Author URI: https://rolloffrates.com
 * Text Domain: rolloff-rates
 */

if (!defined('ABSPATH')) {
    exit;
}

define('ROLLOFF_RATES_VERSION', '1.0.0');
define('ROLLOFF_RATES_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('ROLLOFF_RATES_PLUGIN_URL', plugin_dir_url(__FILE__));
define('ROLLOFF_RATES_API_URL', get_option('rolloff_rates_api_url', 'https://api.rolloffrates.com'));

require_once ROLLOFF_RATES_PLUGIN_DIR . 'includes/class-rolloff-rates.php';
require_once ROLLOFF_RATES_PLUGIN_DIR . 'includes/class-rolloff-rates-api.php';
require_once ROLLOFF_RATES_PLUGIN_DIR . 'includes/shortcodes.php';
require_once ROLLOFF_RATES_PLUGIN_DIR . 'admin/class-rolloff-rates-admin.php';

function rolloff_rates_init() {
    $plugin = new RollOff_Rates();
    $plugin->init();
}
add_action('plugins_loaded', 'rolloff_rates_init');

register_activation_hook(__FILE__, 'rolloff_rates_activate');
function rolloff_rates_activate() {
    add_option('rolloff_rates_api_url', 'https://api.rolloffrates.com');
    add_option('rolloff_rates_cache_duration', 3600); // 1 hour default
    
    flush_rewrite_rules();
}

register_deactivation_hook(__FILE__, 'rolloff_rates_deactivate');
function rolloff_rates_deactivate() {
    flush_rewrite_rules();
}

register_uninstall_hook(__FILE__, 'rolloff_rates_uninstall');
function rolloff_rates_uninstall() {
    delete_option('rolloff_rates_api_url');
    delete_option('rolloff_rates_cache_duration');
    
    global $wpdb;
    $wpdb->query("DELETE FROM $wpdb->options WHERE option_name LIKE '%rolloff_rates_cache%'");
}
