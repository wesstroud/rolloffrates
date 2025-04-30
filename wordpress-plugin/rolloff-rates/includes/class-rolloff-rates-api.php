<?php
/**
 * API client for interacting with the external dumpster data API
 */
class RollOff_Rates_API {
    /**
     * API base URL
     *
     * @var string
     */
    private $api_url;
    
    /**
     * Cache duration in seconds
     *
     * @var int
     */
    private $cache_duration;
    
    /**
     * Constructor
     */
    public function __construct() {
        $this->api_url = get_option('rolloff_rates_api_url', 'https://api.rolloffrates.com');
        $this->cache_duration = get_option('rolloff_rates_cache_duration', 3600);
    }
    
    /**
     * Make an API request
     *
     * @param string $endpoint API endpoint
     * @param array $args Request arguments
     * @return mixed Response data or false on failure
     */
    private function request($endpoint, $args = array()) {
        $url = trailingslashit($this->api_url) . ltrim($endpoint, '/');
        
        if (!empty($args)) {
            $url = add_query_arg($args, $url);
        }
        
        $response = wp_remote_get($url, array(
            'timeout' => 15,
            'headers' => array(
                'Accept' => 'application/json'
            )
        ));
        
        if (is_wp_error($response)) {
            error_log('RollOff Rates API Error: ' . $response->get_error_message());
            return false;
        }
        
        $code = wp_remote_retrieve_response_code($response);
        
        if ($code !== 200) {
            error_log('RollOff Rates API Error: Received response code ' . $code);
            return false;
        }
        
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            error_log('RollOff Rates API Error: Invalid JSON response');
            return false;
        }
        
        return $data;
    }
    
    /**
     * Get all companies
     *
     * @return array Companies data
     */
    public function get_companies() {
        $cache_key = 'rolloff_rates_cache_companies';
        $cached = get_transient($cache_key);
        
        if ($cached !== false) {
            return $cached;
        }
        
        $data = $this->request('companies');
        
        if ($data) {
            set_transient($cache_key, $data, $this->cache_duration);
        }
        
        return $data ?: array();
    }
    
    /**
     * Get all service areas
     *
     * @return array Service areas data
     */
    public function get_service_areas() {
        $cache_key = 'rolloff_rates_cache_service_areas';
        $cached = get_transient($cache_key);
        
        if ($cached !== false) {
            return $cached;
        }
        
        $data = $this->request('service-areas');
        
        if ($data) {
            set_transient($cache_key, $data, $this->cache_duration);
        }
        
        return $data ?: array();
    }
    
    /**
     * Get all dumpster sizes
     *
     * @return array Dumpster sizes data
     */
    public function get_dumpster_sizes() {
        $cache_key = 'rolloff_rates_cache_dumpster_sizes';
        $cached = get_transient($cache_key);
        
        if ($cached !== false) {
            return $cached;
        }
        
        $data = $this->request('dumpster-sizes');
        
        if ($data) {
            set_transient($cache_key, $data, $this->cache_duration);
        }
        
        return $data ?: array();
    }
    
    /**
     * Get all prices
     *
     * @return array Prices data
     */
    public function get_prices() {
        $cache_key = 'rolloff_rates_cache_prices';
        $cached = get_transient($cache_key);
        
        if ($cached !== false) {
            return $cached;
        }
        
        $data = $this->request('prices');
        
        if ($data) {
            set_transient($cache_key, $data, $this->cache_duration);
        }
        
        return $data ?: array();
    }
    
    /**
     * Get all cities
     *
     * @return array Cities data
     */
    public function get_cities() {
        $cache_key = 'rolloff_rates_cache_cities';
        $cached = get_transient($cache_key);
        
        if ($cached !== false) {
            return $cached;
        }
        
        $data = $this->request('cities');
        
        if ($data) {
            set_transient($cache_key, $data, $this->cache_duration);
        }
        
        return $data ?: array();
    }
    
    /**
     * Get data for a specific city
     *
     * @param string $city City name
     * @param string $state State name (optional)
     * @return array|false City data or false if not found
     */
    public function get_city_data($city, $state = null) {
        $cache_key = 'rolloff_rates_cache_city_' . sanitize_title($city);
        
        if ($state) {
            $cache_key .= '_' . sanitize_title($state);
        }
        
        $cached = get_transient($cache_key);
        
        if ($cached !== false) {
            return $cached;
        }
        
        $args = array();
        
        if ($state) {
            $args['state'] = $state;
        }
        
        $data = $this->request('city/' . urlencode($city), $args);
        
        if ($data) {
            set_transient($cache_key, $data, $this->cache_duration);
        }
        
        return $data ?: false;
    }
    
    /**
     * Trigger a data scrape
     *
     * @return bool Success status
     */
    public function trigger_scrape() {
        $response = wp_remote_post(trailingslashit($this->api_url) . 'scrape', array(
            'timeout' => 5,
            'headers' => array(
                'Accept' => 'application/json'
            )
        ));
        
        if (is_wp_error($response)) {
            error_log('RollOff Rates API Error: ' . $response->get_error_message());
            return false;
        }
        
        $code = wp_remote_retrieve_response_code($response);
        
        if ($code !== 200) {
            error_log('RollOff Rates API Error: Received response code ' . $code);
            return false;
        }
        
        $this->clear_cache();
        
        return true;
    }
    
    /**
     * Clear all API caches
     */
    public function clear_cache() {
        global $wpdb;
        $wpdb->query("DELETE FROM $wpdb->options WHERE option_name LIKE '%rolloff_rates_cache%'");
    }
}
