<?php
/**
 * Static page generator for RollOff Rates
 * 
 * This class handles the generation of static HTML pages for city-specific dumpster rental information.
 */
class RollOff_Rates_Static_Generator {
    /**
     * API client instance
     *
     * @var RollOff_Rates_API
     */
    private $api;
    
    /**
     * Output directory for static pages
     *
     * @var string
     */
    private $output_dir;
    
    /**
     * Base URL for static pages
     *
     * @var string
     */
    private $base_url;
    
    /**
     * Constructor
     */
    public function __construct() {
        $this->api = new RollOff_Rates_API();
        $this->output_dir = get_option('rolloff_rates_static_dir', WP_CONTENT_DIR . '/rolloff-rates-static');
        $this->base_url = get_option('rolloff_rates_static_url', home_url('/dumpsters'));
    }
    
    /**
     * Initialize the static generator
     */
    public function init() {
        add_action('admin_menu', array($this, 'add_admin_menu'));
        
        add_action('wp_ajax_rolloff_rates_generate_static', array($this, 'ajax_generate_static'));
        
        add_action('rolloff_rates_generate_static_cron', array($this, 'generate_all_pages'));
    }
    
    /**
     * Add admin menu
     */
    public function add_admin_menu() {
        add_submenu_page(
            'rolloff-rates',
            'Static Generator',
            'Static Generator',
            'manage_options',
            'rolloff-rates-static',
            array($this, 'display_admin_page')
        );
    }
    
    /**
     * Display admin page
     */
    public function display_admin_page() {
        if (!current_user_can('manage_options')) {
            return;
        }
        
        if (isset($_POST['rolloff_rates_static_save']) && check_admin_referer('rolloff_rates_static_settings')) {
            update_option('rolloff_rates_static_dir', sanitize_text_field($_POST['rolloff_rates_static_dir']));
            update_option('rolloff_rates_static_url', sanitize_text_field($_POST['rolloff_rates_static_url']));
            update_option('rolloff_rates_static_cron', isset($_POST['rolloff_rates_static_cron']) ? 1 : 0);
            
            if (isset($_POST['rolloff_rates_static_cron'])) {
                if (!wp_next_scheduled('rolloff_rates_generate_static_cron')) {
                    wp_schedule_event(time(), 'daily', 'rolloff_rates_generate_static_cron');
                }
            } else {
                wp_clear_scheduled_hook('rolloff_rates_generate_static_cron');
            }
            
            echo '<div class="notice notice-success"><p>Settings saved successfully.</p></div>';
        }
        
        $static_dir = get_option('rolloff_rates_static_dir', WP_CONTENT_DIR . '/rolloff-rates-static');
        $static_url = get_option('rolloff_rates_static_url', home_url('/dumpsters'));
        $static_cron = get_option('rolloff_rates_static_cron', 0);
        
        ?>
        <div class="wrap">
            <h1><?php echo esc_html(get_admin_page_title()); ?></h1>
            
            <div class="card">
                <h2>Static Page Generator Settings</h2>
                
                <form method="post" action="">
                    <?php wp_nonce_field('rolloff_rates_static_settings'); ?>
                    
                    <table class="form-table">
                        <tr>
                            <th scope="row"><label for="rolloff_rates_static_dir">Output Directory</label></th>
                            <td>
                                <input type="text" id="rolloff_rates_static_dir" name="rolloff_rates_static_dir" value="<?php echo esc_attr($static_dir); ?>" class="regular-text">
                                <p class="description">The directory where static HTML files will be generated. Must be writable by the web server.</p>
                            </td>
                        </tr>
                        <tr>
                            <th scope="row"><label for="rolloff_rates_static_url">Base URL</label></th>
                            <td>
                                <input type="text" id="rolloff_rates_static_url" name="rolloff_rates_static_url" value="<?php echo esc_attr($static_url); ?>" class="regular-text">
                                <p class="description">The base URL where static pages will be accessible.</p>
                            </td>
                        </tr>
                        <tr>
                            <th scope="row">Automatic Generation</th>
                            <td>
                                <label for="rolloff_rates_static_cron">
                                    <input type="checkbox" id="rolloff_rates_static_cron" name="rolloff_rates_static_cron" value="1" <?php checked($static_cron, 1); ?>>
                                    Generate static pages automatically once per day
                                </label>
                            </td>
                        </tr>
                    </table>
                    
                    <p class="submit">
                        <input type="submit" name="rolloff_rates_static_save" class="button button-primary" value="Save Settings">
                    </p>
                </form>
            </div>
            
            <div class="card">
                <h2>Generate Static Pages</h2>
                
                <p>Click the button below to generate static HTML pages for all cities in the database.</p>
                
                <p>
                    <button id="rolloff-rates-generate-static" class="button button-primary">Generate Static Pages</button>
                    <span id="rolloff-rates-generate-status" style="display: none; margin-left: 10px;"></span>
                </p>
            </div>
        </div>
        
        <script>
            jQuery(document).ready(function($) {
                $('#rolloff-rates-generate-static').on('click', function() {
                    var button = $(this);
                    var status = $('#rolloff-rates-generate-status');
                    
                    button.prop('disabled', true);
                    status.text('Generating static pages...').show();
                    
                    $.ajax({
                        url: ajaxurl,
                        type: 'POST',
                        data: {
                            action: 'rolloff_rates_generate_static',
                            nonce: '<?php echo wp_create_nonce('rolloff_rates_generate_static'); ?>'
                        },
                        success: function(response) {
                            if (response.success) {
                                status.text('Static pages generated successfully! ' + response.data.count + ' pages generated.');
                            } else {
                                status.text('Error: ' + response.data.message);
                            }
                        },
                        error: function() {
                            status.text('An error occurred. Please try again later.');
                        },
                        complete: function() {
                            button.prop('disabled', false);
                        }
                    });
                });
            });
        </script>
        <?php
    }
    
    /**
     * AJAX handler for generating static pages
     */
    public function ajax_generate_static() {
        if (!isset($_POST['nonce']) || !wp_verify_nonce($_POST['nonce'], 'rolloff_rates_generate_static')) {
            wp_send_json_error(array('message' => 'Invalid nonce.'));
        }
        
        if (!current_user_can('manage_options')) {
            wp_send_json_error(array('message' => 'You do not have permission to do this.'));
        }
        
        $count = $this->generate_all_pages();
        
        if ($count !== false) {
            wp_send_json_success(array('count' => $count));
        } else {
            wp_send_json_error(array('message' => 'Failed to generate static pages.'));
        }
    }
    
    /**
     * Generate static HTML pages for all cities
     *
     * @return int|false Number of pages generated or false on failure
     */
    public function generate_all_pages() {
        $cities = $this->api->get_cities();
        
        if (!$cities) {
            return false;
        }
        
        if (!file_exists($this->output_dir)) {
            if (!mkdir($this->output_dir, 0755, true)) {
                error_log('RollOff Rates: Failed to create output directory: ' . $this->output_dir);
                return false;
            }
        }
        
        $count = 0;
        
        foreach ($cities as $city_data) {
            $city = $city_data['city'];
            $state = $city_data['state'];
            
            $result = $this->generate_city_page($city, $state);
            
            if ($result) {
                $count++;
            }
        }
        
        $this->generate_sitemap($cities);
        
        return $count;
    }
    
    /**
     * Generate static HTML page for a specific city
     *
     * @param string $city City name
     * @param string $state State name
     * @return bool Success status
     */
    public function generate_city_page($city, $state) {
        $city_data = $this->api->get_city_data($city, $state);
        
        if (!$city_data) {
            return false;
        }
        
        $city_slug = sanitize_title($city);
        $state_slug = sanitize_title($state);
        $city_dir = $this->output_dir . '/' . $city_slug . '-' . $state_slug;
        
        if (!file_exists($city_dir)) {
            if (!mkdir($city_dir, 0755, true)) {
                error_log('RollOff Rates: Failed to create city directory: ' . $city_dir);
                return false;
            }
        }
        
        $html = $this->generate_city_html($city_data);
        
        $file_path = $city_dir . '/index.html';
        $result = file_put_contents($file_path, $html);
        
        if ($result === false) {
            error_log('RollOff Rates: Failed to write HTML file: ' . $file_path);
            return false;
        }
        
        return true;
    }
    
    /**
     * Generate HTML content for a city page
     *
     * @param array $city_data City data
     * @return string HTML content
     */
    private function generate_city_html($city_data) {
        
        return '<!DOCTYPE html>
<html lang="en">
<head>
    <!-- SEO metadata and styling -->
</head>
<body>
    <!-- City page content with pricing tables, company info, and lead form -->
</body>
</html>';
    }
    
    /**
     * Generate XML sitemap for all city pages
     *
     * @param array $cities List of cities
     * @return bool Success status
     */
    public function generate_sitemap($cities) {
        $xml = '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
        $xml .= '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
        
        foreach ($cities as $city_data) {
            $city = $city_data['city'];
            $state = $city_data['state'];
            $city_slug = sanitize_title($city);
            $state_slug = sanitize_title($state);
            
            $url = $this->base_url . '/' . $city_slug . '-' . $state_slug . '/';
            
            $xml .= '  <url>' . "\n";
            $xml .= '    <loc>' . esc_url($url) . '</loc>' . "\n";
            $xml .= '    <changefreq>weekly</changefreq>' . "\n";
            $xml .= '    <priority>0.8</priority>' . "\n";
            $xml .= '  </url>' . "\n";
        }
        
        $xml .= '</urlset>';
        
        $file_path = $this->output_dir . '/sitemap.xml';
        $result = file_put_contents($file_path, $xml);
        
        if ($result === false) {
            error_log('RollOff Rates: Failed to write sitemap file: ' . $file_path);
            return false;
        }
        
        return true;
    }
}
