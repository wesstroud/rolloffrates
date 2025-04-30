<?php
/**
 * Fired during plugin activation
 *
 * This class handles the activation of the RollOff Rates plugin,
 * including database table creation and initial settings.
 */
class RollOff_Rates_Activator {
    /**
     * Activate the plugin
     *
     * Create database tables and set default options.
     */
    public static function activate() {
        self::create_tables();
        self::set_default_options();
        
        flush_rewrite_rules();
    }
    
    /**
     * Create database tables
     */
    private static function create_tables() {
        global $wpdb;
        
        $charset_collate = $wpdb->get_charset_collate();
        
        $table_name = $wpdb->prefix . 'rolloff_rates_leads';
        
        $sql = "CREATE TABLE $table_name (
            id mediumint(9) NOT NULL AUTO_INCREMENT,
            name varchar(100) NOT NULL,
            email varchar(100) NOT NULL,
            phone varchar(20) NOT NULL,
            address varchar(255) DEFAULT '',
            city varchar(100) DEFAULT '',
            state varchar(50) DEFAULT '',
            size varchar(20) DEFAULT '',
            message text DEFAULT '',
            created_at datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
            PRIMARY KEY  (id)
        ) $charset_collate;";
        
        require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
        dbDelta($sql);
    }
    
    /**
     * Set default options
     */
    private static function set_default_options() {
        if (!get_option('rolloff_rates_api_url')) {
            update_option('rolloff_rates_api_url', 'https://api.rolloffrates.com');
        }
        
        if (!get_option('rolloff_rates_cache_duration')) {
            update_option('rolloff_rates_cache_duration', 3600);
        }
        
        if (!get_option('rolloff_rates_static_dir')) {
            update_option('rolloff_rates_static_dir', WP_CONTENT_DIR . '/rolloff-rates-static');
        }
        
        if (!get_option('rolloff_rates_static_url')) {
            update_option('rolloff_rates_static_url', home_url('/dumpsters'));
        }
        
        if (!get_option('rolloff_rates_static_cron')) {
            update_option('rolloff_rates_static_cron', 0);
        }
    }
}
