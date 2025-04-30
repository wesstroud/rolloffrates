<?php
/**
 * Admin functionality for the RollOff Rates plugin
 */
class RollOff_Rates_Admin {
    /**
     * Initialize the admin functionality
     */
    public function __construct() {
        add_action('admin_menu', array($this, 'add_admin_menu'));
        
        add_action('admin_init', array($this, 'register_settings'));
        
        add_action('wp_ajax_rolloff_rates_trigger_scrape', array($this, 'ajax_trigger_scrape'));
        add_action('wp_ajax_rolloff_rates_clear_cache', array($this, 'ajax_clear_cache'));
        add_action('wp_ajax_rolloff_rates_submit_form', array($this, 'ajax_submit_form'));
        add_action('wp_ajax_nopriv_rolloff_rates_submit_form', array($this, 'ajax_submit_form'));
    }
    
    /**
     * Add admin menu
     */
    public function add_admin_menu() {
        add_menu_page(
            'RollOff Rates',
            'RollOff Rates',
            'manage_options',
            'rolloff-rates',
            array($this, 'display_settings_page'),
            'dashicons-database',
            30
        );
        
        add_submenu_page(
            'rolloff-rates',
            'Settings',
            'Settings',
            'manage_options',
            'rolloff-rates',
            array($this, 'display_settings_page')
        );
        
        add_submenu_page(
            'rolloff-rates',
            'Data Management',
            'Data Management',
            'manage_options',
            'rolloff-rates-data',
            array($this, 'display_data_page')
        );
        
        add_submenu_page(
            'rolloff-rates',
            'Lead Submissions',
            'Lead Submissions',
            'manage_options',
            'rolloff-rates-leads',
            array($this, 'display_leads_page')
        );
    }
    
    /**
     * Register settings
     */
    public function register_settings() {
        register_setting('rolloff_rates_settings', 'rolloff_rates_api_url');
        register_setting('rolloff_rates_settings', 'rolloff_rates_cache_duration', array(
            'type' => 'integer',
            'sanitize_callback' => 'absint',
            'default' => 3600,
        ));
        
        add_settings_section(
            'rolloff_rates_api_settings',
            'API Settings',
            array($this, 'api_settings_section_callback'),
            'rolloff_rates_settings'
        );
        
        add_settings_field(
            'rolloff_rates_api_url',
            'API URL',
            array($this, 'api_url_field_callback'),
            'rolloff_rates_settings',
            'rolloff_rates_api_settings'
        );
        
        add_settings_field(
            'rolloff_rates_cache_duration',
            'Cache Duration (seconds)',
            array($this, 'cache_duration_field_callback'),
            'rolloff_rates_settings',
            'rolloff_rates_api_settings'
        );
    }
    
    /**
     * API settings section callback
     */
    public function api_settings_section_callback() {
        echo '<p>Configure the connection to the RollOff Rates API.</p>';
    }
    
    /**
     * API URL field callback
     */
    public function api_url_field_callback() {
        $api_url = get_option('rolloff_rates_api_url', 'https://api.rolloffrates.com');
        echo '<input type="url" id="rolloff_rates_api_url" name="rolloff_rates_api_url" value="' . esc_attr($api_url) . '" class="regular-text">';
        echo '<p class="description">The URL of the RollOff Rates API server.</p>';
    }
    
    /**
     * Cache duration field callback
     */
    public function cache_duration_field_callback() {
        $cache_duration = get_option('rolloff_rates_cache_duration', 3600);
        echo '<input type="number" id="rolloff_rates_cache_duration" name="rolloff_rates_cache_duration" value="' . esc_attr($cache_duration) . '" class="regular-text">';
        echo '<p class="description">How long to cache API responses, in seconds. Default is 3600 (1 hour).</p>';
    }
    
    /**
     * Display settings page
     */
    public function display_settings_page() {
        if (!current_user_can('manage_options')) {
            return;
        }
        
        ?>
        <div class="wrap">
            <h1><?php echo esc_html(get_admin_page_title()); ?></h1>
            
            <form action="options.php" method="post">
                <?php
                settings_fields('rolloff_rates_settings');
                do_settings_sections('rolloff_rates_settings');
                submit_button('Save Settings');
                ?>
            </form>
            
            <h2>Shortcodes</h2>
            <div class="card">
                <h3>Pricing Table</h3>
                <p><code>[rolloff_table city="Denver" state="CO"]</code></p>
                <p>Displays a table of dumpster rental prices for the specified city.</p>
                <p><strong>Parameters:</strong></p>
                <ul>
                    <li><code>city</code> - City name (required if not on a city page)</li>
                    <li><code>state</code> - State name (required if not on a city page)</li>
                    <li><code>company</code> - Filter by company name</li>
                    <li><code>size</code> - Filter by dumpster size</li>
                    <li><code>show_header</code> - Whether to show the table header (true/false)</li>
                    <li><code>show_company</code> - Whether to show the company column (true/false)</li>
                    <li><code>show_size</code> - Whether to show the size column (true/false)</li>
                    <li><code>show_price</code> - Whether to show the price column (true/false)</li>
                    <li><code>show_rental_period</code> - Whether to show the rental period column (true/false)</li>
                    <li><code>show_weight_limit</code> - Whether to show the weight limit column (true/false)</li>
                    <li><code>show_cta</code> - Whether to show the call-to-action column (true/false)</li>
                    <li><code>cta_text</code> - Text for the call-to-action button</li>
                    <li><code>cta_url</code> - URL for the call-to-action button</li>
                    <li><code>class</code> - Additional CSS classes</li>
                </ul>
            </div>
            
            <div class="card">
                <h3>Companies List</h3>
                <p><code>[rolloff_companies city="Denver" state="CO" layout="grid"]</code></p>
                <p>Displays a list of dumpster rental companies for the specified city.</p>
                <p><strong>Parameters:</strong></p>
                <ul>
                    <li><code>city</code> - City name (required if not on a city page)</li>
                    <li><code>state</code> - State name (required if not on a city page)</li>
                    <li><code>layout</code> - Layout style (list/grid)</li>
                    <li><code>show_logo</code> - Whether to show company logos (true/false)</li>
                    <li><code>show_description</code> - Whether to show company descriptions (true/false)</li>
                    <li><code>show_phone</code> - Whether to show company phone numbers (true/false)</li>
                    <li><code>show_website</code> - Whether to show company website links (true/false)</li>
                    <li><code>class</code> - Additional CSS classes</li>
                </ul>
            </div>
            
            <div class="card">
                <h3>Lead Form</h3>
                <p><code>[rolloff_form city="Denver" state="CO"]</code></p>
                <p>Displays a lead generation form for dumpster rental quotes.</p>
                <p><strong>Parameters:</strong></p>
                <ul>
                    <li><code>city</code> - City name (required if not on a city page)</li>
                    <li><code>state</code> - State name (required if not on a city page)</li>
                    <li><code>title</code> - Form title</li>
                    <li><code>submit_text</code> - Text for the submit button</li>
                    <li><code>success_message</code> - Message to display after successful submission</li>
                    <li><code>class</code> - Additional CSS classes</li>
                </ul>
            </div>
        </div>
        <?php
    }
    
    /**
     * Display data management page
     */
    public function display_data_page() {
        if (!current_user_can('manage_options')) {
            return;
        }
        
        $api = new RollOff_Rates_API();
        $cities = $api->get_cities();
        
        ?>
        <div class="wrap">
            <h1><?php echo esc_html(get_admin_page_title()); ?></h1>
            
            <div class="card">
                <h2>Data Management</h2>
                
                <p>
                    <button id="rolloff-rates-trigger-scrape" class="button button-primary">Trigger Data Scrape</button>
                    <span id="rolloff-rates-scrape-status" style="display: none; margin-left: 10px;"></span>
                </p>
                
                <p>
                    <button id="rolloff-rates-clear-cache" class="button">Clear Cache</button>
                    <span id="rolloff-rates-cache-status" style="display: none; margin-left: 10px;"></span>
                </p>
            </div>
            
            <div class="card">
                <h2>Available Cities</h2>
                
                <?php if (empty($cities)): ?>
                    <p>No cities available. Try triggering a data scrape.</p>
                <?php else: ?>
                    <table class="wp-list-table widefat fixed striped">
                        <thead>
                            <tr>
                                <th>City</th>
                                <th>State</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($cities as $city): ?>
                                <tr>
                                    <td><?php echo esc_html($city['city']); ?></td>
                                    <td><?php echo esc_html($city['state']); ?></td>
                                    <td>
                                        <a href="<?php echo esc_url(admin_url('admin.php?page=rolloff-rates-data&view=city&city=' . urlencode($city['city']) . '&state=' . urlencode($city['state']))); ?>" class="button button-small">View Data</a>
                                    </td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                <?php endif; ?>
            </div>
            
            <?php if (isset($_GET['view']) && $_GET['view'] === 'city' && isset($_GET['city']) && isset($_GET['state'])): ?>
                <?php
                $city = sanitize_text_field($_GET['city']);
                $state = sanitize_text_field($_GET['state']);
                $city_data = $api->get_city_data($city, $state);
                ?>
                
                <?php if ($city_data): ?>
                    <div class="card">
                        <h2>Data for <?php echo esc_html($city); ?>, <?php echo esc_html($state); ?></h2>
                        
                        <h3>Companies</h3>
                        <table class="wp-list-table widefat fixed striped">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Name</th>
                                    <th>Phone</th>
                                    <th>Website</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($city_data['companies'] as $company): ?>
                                    <tr>
                                        <td><?php echo esc_html($company['id']); ?></td>
                                        <td><?php echo esc_html($company['name']); ?></td>
                                        <td><?php echo esc_html($company['phone']); ?></td>
                                        <td><?php echo esc_html($company['website']); ?></td>
                                    </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                        
                        <h3>Dumpster Sizes</h3>
                        <table class="wp-list-table widefat fixed striped">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Size</th>
                                    <th>Dimensions</th>
                                    <th>Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($city_data['dumpster_sizes'] as $size): ?>
                                    <tr>
                                        <td><?php echo esc_html($size['id']); ?></td>
                                        <td><?php echo esc_html($size['size']); ?> yard</td>
                                        <td><?php echo esc_html($size['dimensions']); ?></td>
                                        <td><?php echo esc_html($size['description']); ?></td>
                                    </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                        
                        <h3>Prices</h3>
                        <table class="wp-list-table widefat fixed striped">
                            <thead>
                                <tr>
                                    <th>Company</th>
                                    <th>Size</th>
                                    <th>Price</th>
                                    <th>Rental Period</th>
                                    <th>Weight Limit</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($city_data['prices'] as $price): ?>
                                    <?php
                                    $company_name = '';
                                    $size_name = '';
                                    
                                    foreach ($city_data['companies'] as $company) {
                                        if ($company['id'] === $price['company_id']) {
                                            $company_name = $company['name'];
                                            break;
                                        }
                                    }
                                    
                                    foreach ($city_data['dumpster_sizes'] as $size) {
                                        if ($size['id'] === $price['size_id']) {
                                            $size_name = $size['size'] . ' yard';
                                            break;
                                        }
                                    }
                                    ?>
                                    <tr>
                                        <td><?php echo esc_html($company_name); ?></td>
                                        <td><?php echo esc_html($size_name); ?></td>
                                        <td>$<?php echo esc_html(number_format($price['price'], 2)); ?></td>
                                        <td><?php echo esc_html($price['rental_period']); ?> days</td>
                                        <td><?php echo esc_html(number_format($price['weight_limit'])); ?> lbs</td>
                                    </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                <?php else: ?>
                    <div class="card">
                        <h2>Data for <?php echo esc_html($city); ?>, <?php echo esc_html($state); ?></h2>
                        <p>No data available for this city.</p>
                    </div>
                <?php endif; ?>
            <?php endif; ?>
        </div>
        
        <script>
            jQuery(document).ready(function($) {
                $('#rolloff-rates-trigger-scrape').on('click', function() {
                    var button = $(this);
                    var status = $('#rolloff-rates-scrape-status');
                    
                    button.prop('disabled', true);
                    status.text('Triggering scrape...').show();
                    
                    $.ajax({
                        url: ajaxurl,
                        type: 'POST',
                        data: {
                            action: 'rolloff_rates_trigger_scrape',
                            nonce: '<?php echo wp_create_nonce('rolloff_rates_trigger_scrape'); ?>'
                        },
                        success: function(response) {
                            if (response.success) {
                                status.text('Scrape triggered successfully! This may take a few minutes to complete.');
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
                
                $('#rolloff-rates-clear-cache').on('click', function() {
                    var button = $(this);
                    var status = $('#rolloff-rates-cache-status');
                    
                    button.prop('disabled', true);
                    status.text('Clearing cache...').show();
                    
                    $.ajax({
                        url: ajaxurl,
                        type: 'POST',
                        data: {
                            action: 'rolloff_rates_clear_cache',
                            nonce: '<?php echo wp_create_nonce('rolloff_rates_clear_cache'); ?>'
                        },
                        success: function(response) {
                            if (response.success) {
                                status.text('Cache cleared successfully!');
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
     * Display leads page
     */
    public function display_leads_page() {
        if (!current_user_can('manage_options')) {
            return;
        }
        
        global $wpdb;
        $table_name = $wpdb->prefix . 'rolloff_rates_leads';
        $leads = $wpdb->get_results("SELECT * FROM $table_name ORDER BY created_at DESC", ARRAY_A);
        
        ?>
        <div class="wrap">
            <h1><?php echo esc_html(get_admin_page_title()); ?></h1>
            
            <div class="card">
                <h2>Lead Submissions</h2>
                
                <?php if (empty($leads)): ?>
                    <p>No lead submissions yet.</p>
                <?php else: ?>
                    <table class="wp-list-table widefat fixed striped">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Phone</th>
                                <th>City</th>
                                <th>State</th>
                                <th>Size</th>
                                <th>Date</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($leads as $lead): ?>
                                <tr>
                                    <td><?php echo esc_html($lead['id']); ?></td>
                                    <td><?php echo esc_html($lead['name']); ?></td>
                                    <td><?php echo esc_html($lead['email']); ?></td>
                                    <td><?php echo esc_html($lead['phone']); ?></td>
                                    <td><?php echo esc_html($lead['city']); ?></td>
                                    <td><?php echo esc_html($lead['state']); ?></td>
                                    <td><?php echo esc_html($lead['size']); ?></td>
                                    <td><?php echo esc_html(date('Y-m-d H:i:s', strtotime($lead['created_at']))); ?></td>
                                    <td>
                                        <a href="<?php echo esc_url(admin_url('admin.php?page=rolloff-rates-leads&view=lead&id=' . $lead['id'])); ?>" class="button button-small">View Details</a>
                                    </td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                <?php endif; ?>
            </div>
            
            <?php if (isset($_GET['view']) && $_GET['view'] === 'lead' && isset($_GET['id'])): ?>
                <?php
                $lead_id = intval($_GET['id']);
                $lead = $wpdb->get_row($wpdb->prepare("SELECT * FROM $table_name WHERE id = %d", $lead_id), ARRAY_A);
                ?>
                
                <?php if ($lead): ?>
                    <div class="card">
                        <h2>Lead Details</h2>
                        
                        <table class="form-table">
                            <tr>
                                <th>ID</th>
                                <td><?php echo esc_html($lead['id']); ?></td>
                            </tr>
                            <tr>
                                <th>Name</th>
                                <td><?php echo esc_html($lead['name']); ?></td>
                            </tr>
                            <tr>
                                <th>Email</th>
                                <td><?php echo esc_html($lead['email']); ?></td>
                            </tr>
                            <tr>
                                <th>Phone</th>
                                <td><?php echo esc_html($lead['phone']); ?></td>
                            </tr>
                            <tr>
                                <th>Address</th>
                                <td><?php echo esc_html($lead['address']); ?></td>
                            </tr>
                            <tr>
                                <th>City</th>
                                <td><?php echo esc_html($lead['city']); ?></td>
                            </tr>
                            <tr>
                                <th>State</th>
                                <td><?php echo esc_html($lead['state']); ?></td>
                            </tr>
                            <tr>
                                <th>Size</th>
                                <td><?php echo esc_html($lead['size']); ?></td>
                            </tr>
                            <tr>
                                <th>Message</th>
                                <td><?php echo nl2br(esc_html($lead['message'])); ?></td>
                            </tr>
                            <tr>
                                <th>Date</th>
                                <td><?php echo esc_html(date('Y-m-d H:i:s', strtotime($lead['created_at']))); ?></td>
                            </tr>
                        </table>
                        
                        <p>
                            <a href="<?php echo esc_url(admin_url('admin.php?page=rolloff-rates-leads')); ?>" class="button">Back to Leads</a>
                        </p>
                    </div>
                <?php else: ?>
                    <div class="card">
                        <h2>Lead Details</h2>
                        <p>Lead not found.</p>
                    </div>
                <?php endif; ?>
            <?php endif; ?>
        </div>
        <?php
    }
    
    /**
     * AJAX handler for triggering a data scrape
     */
    public function ajax_trigger_scrape() {
        if (!isset($_POST['nonce']) || !wp_verify_nonce($_POST['nonce'], 'rolloff_rates_trigger_scrape')) {
            wp_send_json_error(array('message' => 'Invalid nonce.'));
        }
        
        if (!current_user_can('manage_options')) {
            wp_send_json_error(array('message' => 'You do not have permission to do this.'));
        }
        
        $api = new RollOff_Rates_API();
        $result = $api->trigger_scrape();
        
        if ($result) {
            wp_send_json_success(array('message' => 'Scrape triggered successfully.'));
        } else {
            wp_send_json_error(array('message' => 'Failed to trigger scrape.'));
        }
    }
    
    /**
     * AJAX handler for clearing the cache
     */
    public function ajax_clear_cache() {
        if (!isset($_POST['nonce']) || !wp_verify_nonce($_POST['nonce'], 'rolloff_rates_clear_cache')) {
            wp_send_json_error(array('message' => 'Invalid nonce.'));
        }
        
        if (!current_user_can('manage_options')) {
            wp_send_json_error(array('message' => 'You do not have permission to do this.'));
        }
        
        $api = new RollOff_Rates_API();
        $api->clear_cache();
        
        wp_send_json_success(array('message' => 'Cache cleared successfully.'));
    }
    
    /**
     * AJAX handler for form submission
     */
    public function ajax_submit_form() {
        if (!isset($_POST['nonce']) || !wp_verify_nonce($_POST['nonce'], 'rolloff_rates_nonce')) {
            wp_send_json_error(array('message' => 'Invalid nonce.'));
        }
        
        parse_str($_POST['formData'], $form_data);
        
        $required_fields = array('name', 'email', 'phone');
        
        foreach ($required_fields as $field) {
            if (empty($form_data[$field])) {
                wp_send_json_error(array('message' => 'Please fill in all required fields.'));
            }
        }
        
        global $wpdb;
        $table_name = $wpdb->prefix . 'rolloff_rates_leads';
        
        $result = $wpdb->insert(
            $table_name,
            array(
                'name' => sanitize_text_field($form_data['name']),
                'email' => sanitize_email($form_data['email']),
                'phone' => sanitize_text_field($form_data['phone']),
                'address' => isset($form_data['address']) ? sanitize_text_field($form_data['address']) : '',
                'city' => isset($form_data['city']) ? sanitize_text_field($form_data['city']) : '',
                'state' => isset($form_data['state']) ? sanitize_text_field($form_data['state']) : '',
                'size' => isset($form_data['size']) ? sanitize_text_field($form_data['size']) : '',
                'message' => isset($form_data['message']) ? sanitize_textarea_field($form_data['message']) : '',
                'created_at' => current_time('mysql'),
            )
        );
        
        if ($result) {
            $to = get_option('admin_email');
            $subject = 'New Dumpster Rental Lead';
            
            $message = "A new dumpster rental lead has been submitted:\n\n";
            $message .= "Name: " . sanitize_text_field($form_data['name']) . "\n";
            $message .= "Email: " . sanitize_email($form_data['email']) . "\n";
            $message .= "Phone: " . sanitize_text_field($form_data['phone']) . "\n";
            
            if (!empty($form_data['address'])) {
                $message .= "Address: " . sanitize_text_field($form_data['address']) . "\n";
            }
            
            if (!empty($form_data['city'])) {
                $message .= "City: " . sanitize_text_field($form_data['city']) . "\n";
            }
            
            if (!empty($form_data['state'])) {
                $message .= "State: " . sanitize_text_field($form_data['state']) . "\n";
            }
            
            if (!empty($form_data['size'])) {
                $message .= "Size: " . sanitize_text_field($form_data['size']) . " yard\n";
            }
            
            if (!empty($form_data['message'])) {
                $message .= "Message: " . sanitize_textarea_field($form_data['message']) . "\n";
            }
            
            wp_mail($to, $subject, $message);
            
            wp_send_json_success(array('message' => 'Form submitted successfully.'));
        } else {
            wp_send_json_error(array('message' => 'Failed to save lead.'));
        }
    }
}

$rolloff_rates_admin = new RollOff_Rates_Admin();
