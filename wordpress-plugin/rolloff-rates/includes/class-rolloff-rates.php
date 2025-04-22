<?php
/**
 * Main plugin class
 */
class RollOff_Rates {
    /**
     * API client instance
     *
     * @var RollOff_Rates_API
     */
    private $api;
    
    /**
     * Initialize the plugin
     */
    public function init() {
        $this->api = new RollOff_Rates_API();
        
        $this->register_shortcodes();
        
        add_action('init', array($this, 'register_rewrite_rules'));
        
        add_filter('query_vars', array($this, 'register_query_vars'));
        
        add_filter('template_include', array($this, 'city_page_template'));
        
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
    }
    
    /**
     * Register shortcodes
     */
    private function register_shortcodes() {
        add_shortcode('rolloff_table', 'rolloff_rates_table_shortcode');
        add_shortcode('rolloff_companies', 'rolloff_rates_companies_shortcode');
        add_shortcode('rolloff_form', 'rolloff_rates_form_shortcode');
    }
    
    /**
     * Register rewrite rules for city pages
     */
    public function register_rewrite_rules() {
        add_rewrite_rule(
            'dumpsters/([^/]+)/?$',
            'index.php?rolloff_city=$matches[1]',
            'top'
        );
        
        add_rewrite_rule(
            'dumpsters/([^/]+)/([^/]+)/?$',
            'index.php?rolloff_city=$matches[1]&rolloff_state=$matches[2]',
            'top'
        );
    }
    
    /**
     * Register query vars
     */
    public function register_query_vars($vars) {
        $vars[] = 'rolloff_city';
        $vars[] = 'rolloff_state';
        return $vars;
    }
    
    /**
     * Load city page template
     */
    public function city_page_template($template) {
        if (get_query_var('rolloff_city')) {
            $city = get_query_var('rolloff_city');
            $state = get_query_var('rolloff_state');
            
            $city_data = $this->api->get_city_data($city, $state);
            
            if ($city_data) {
                global $rolloff_city_data;
                $rolloff_city_data = $city_data;
                
                $theme_template = locate_template('rolloff-rates/city-page.php');
                
                if ($theme_template) {
                    return $theme_template;
                } else {
                    return ROLLOFF_RATES_PLUGIN_DIR . 'templates/city-page.php';
                }
            }
        }
        
        return $template;
    }
    
    /**
     * Enqueue scripts and styles
     */
    public function enqueue_scripts() {
        wp_enqueue_style(
            'rolloff-rates-styles',
            ROLLOFF_RATES_PLUGIN_URL . 'assets/css/rolloff-rates.css',
            array(),
            ROLLOFF_RATES_VERSION
        );
        
        wp_enqueue_script(
            'rolloff-rates-scripts',
            ROLLOFF_RATES_PLUGIN_URL . 'assets/js/rolloff-rates.js',
            array('jquery'),
            ROLLOFF_RATES_VERSION,
            true
        );
        
        wp_localize_script(
            'rolloff-rates-scripts',
            'rolloffRatesData',
            array(
                'ajaxUrl' => admin_url('admin-ajax.php'),
                'nonce' => wp_create_nonce('rolloff-rates-nonce')
            )
        );
    }
}
