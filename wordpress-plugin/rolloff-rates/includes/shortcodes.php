<?php
/**
 * Shortcode functions for RollOff Rates plugin
 */

/**
 * Shortcode for displaying dumpster rental pricing table
 *
 * @param array $atts Shortcode attributes
 * @return string Shortcode output
 */
function rolloff_rates_table_shortcode($atts) {
    $atts = shortcode_atts(array(
        'city' => '',
        'state' => '',
        'company' => '',
        'size' => '',
        'show_header' => 'true',
        'show_company' => 'true',
        'show_size' => 'true',
        'show_price' => 'true',
        'show_rental_period' => 'true',
        'show_weight_limit' => 'true',
        'show_cta' => 'true',
        'cta_text' => 'Get a Quote',
        'cta_url' => '',
        'class' => '',
    ), $atts, 'rolloff_table');
    
    foreach (['show_header', 'show_company', 'show_size', 'show_price', 'show_rental_period', 'show_weight_limit', 'show_cta'] as $key) {
        $atts[$key] = filter_var($atts[$key], FILTER_VALIDATE_BOOLEAN);
    }
    
    $api = new RollOff_Rates_API();
    
    $city_data = null;
    
    if (!empty($atts['city'])) {
        $city_data = $api->get_city_data($atts['city'], $atts['state']);
    } else {
        global $rolloff_city_data;
        
        if ($rolloff_city_data) {
            $city_data = $rolloff_city_data;
        } else {
            $cities = $api->get_cities();
            
            if (!empty($cities)) {
                $first_city = $cities[0];
                $city_data = $api->get_city_data($first_city['city'], $first_city['state']);
            }
        }
    }
    
    if (!$city_data) {
        return '<p>No dumpster rental data available for the specified city.</p>';
    }
    
    $companies = $city_data['companies'];
    
    if (!empty($atts['company'])) {
        $companies = array_filter($companies, function($company) use ($atts) {
            return strtolower($company['name']) === strtolower($atts['company']);
        });
    }
    
    $sizes = $city_data['dumpster_sizes'];
    
    if (!empty($atts['size'])) {
        $sizes = array_filter($sizes, function($size) use ($atts) {
            return $size['size'] === $atts['size'];
        });
    }
    
    $output = '<div class="rolloff-rates-table-container ' . esc_attr($atts['class']) . '">';
    $output .= '<table class="rolloff-rates-table">';
    
    if ($atts['show_header']) {
        $output .= '<thead><tr>';
        
        if ($atts['show_company']) {
            $output .= '<th>Company</th>';
        }
        
        if ($atts['show_size']) {
            $output .= '<th>Size</th>';
        }
        
        if ($atts['show_price']) {
            $output .= '<th>Price</th>';
        }
        
        if ($atts['show_rental_period']) {
            $output .= '<th>Rental Period</th>';
        }
        
        if ($atts['show_weight_limit']) {
            $output .= '<th>Weight Limit</th>';
        }
        
        if ($atts['show_cta']) {
            $output .= '<th>Action</th>';
        }
        
        $output .= '</tr></thead>';
    }
    
    $output .= '<tbody>';
    
    $prices = $city_data['prices'];
    $rows_added = 0;
    
    foreach ($companies as $company) {
        foreach ($sizes as $size) {
            $price_data = null;
            
            foreach ($prices as $price) {
                if ($price['company_id'] === $company['id'] && $price['size_id'] === $size['id']) {
                    $price_data = $price;
                    break;
                }
            }
            
            if (!$price_data) {
                continue;
            }
            
            $output .= '<tr>';
            
            if ($atts['show_company']) {
                $output .= '<td>' . esc_html($company['name']) . '</td>';
            }
            
            if ($atts['show_size']) {
                $output .= '<td>' . esc_html($size['size']) . ' yard</td>';
            }
            
            if ($atts['show_price']) {
                $output .= '<td>$' . esc_html(number_format($price_data['price'], 2)) . '</td>';
            }
            
            if ($atts['show_rental_period']) {
                $output .= '<td>' . esc_html($price_data['rental_period']) . ' days</td>';
            }
            
            if ($atts['show_weight_limit']) {
                $output .= '<td>' . esc_html(number_format($price_data['weight_limit'])) . ' lbs</td>';
            }
            
            if ($atts['show_cta']) {
                $cta_url = !empty($atts['cta_url']) ? $atts['cta_url'] : '#rolloff-rates-form';
                $output .= '<td><a href="' . esc_url($cta_url) . '" class="rolloff-rates-cta-button">' . esc_html($atts['cta_text']) . '</a></td>';
            }
            
            $output .= '</tr>';
            $rows_added++;
        }
    }
    
    if ($rows_added === 0) {
        $output .= '<tr><td colspan="6">No dumpster rental data available for the specified criteria.</td></tr>';
    }
    
    $output .= '</tbody>';
    $output .= '</table>';
    $output .= '</div>';
    
    return $output;
}

/**
 * Shortcode for displaying dumpster rental companies
 *
 * @param array $atts Shortcode attributes
 * @return string Shortcode output
 */
function rolloff_rates_companies_shortcode($atts) {
    $atts = shortcode_atts(array(
        'city' => '',
        'state' => '',
        'layout' => 'list', // list, grid
        'show_logo' => 'true',
        'show_description' => 'true',
        'show_phone' => 'true',
        'show_website' => 'true',
        'class' => '',
    ), $atts, 'rolloff_companies');
    
    foreach (['show_logo', 'show_description', 'show_phone', 'show_website'] as $key) {
        $atts[$key] = filter_var($atts[$key], FILTER_VALIDATE_BOOLEAN);
    }
    
    $api = new RollOff_Rates_API();
    
    $city_data = null;
    
    if (!empty($atts['city'])) {
        $city_data = $api->get_city_data($atts['city'], $atts['state']);
    } else {
        global $rolloff_city_data;
        
        if ($rolloff_city_data) {
            $city_data = $rolloff_city_data;
        } else {
            $cities = $api->get_cities();
            
            if (!empty($cities)) {
                $first_city = $cities[0];
                $city_data = $api->get_city_data($first_city['city'], $first_city['state']);
            }
        }
    }
    
    if (!$city_data || empty($city_data['companies'])) {
        return '<p>No dumpster rental companies available for the specified city.</p>';
    }
    
    $companies = $city_data['companies'];
    
    $container_class = 'rolloff-rates-companies-' . esc_attr($atts['layout']);
    $output = '<div class="rolloff-rates-companies ' . $container_class . ' ' . esc_attr($atts['class']) . '">';
    
    foreach ($companies as $company) {
        $output .= '<div class="rolloff-rates-company">';
        
        if ($atts['show_logo'] && !empty($company['logo_url'])) {
            $output .= '<div class="rolloff-rates-company-logo">';
            $output .= '<img src="' . esc_url($company['logo_url']) . '" alt="' . esc_attr($company['name']) . ' Logo">';
            $output .= '</div>';
        }
        
        $output .= '<h3 class="rolloff-rates-company-name">' . esc_html($company['name']) . '</h3>';
        
        if ($atts['show_description'] && !empty($company['description'])) {
            $output .= '<div class="rolloff-rates-company-description">' . wp_kses_post($company['description']) . '</div>';
        }
        
        if ($atts['show_phone'] && !empty($company['phone'])) {
            $output .= '<div class="rolloff-rates-company-phone">';
            $output .= '<a href="tel:' . esc_attr($company['phone']) . '">' . esc_html($company['phone']) . '</a>';
            $output .= '</div>';
        }
        
        if ($atts['show_website'] && !empty($company['website'])) {
            $output .= '<div class="rolloff-rates-company-website">';
            $output .= '<a href="' . esc_url($company['website']) . '" target="_blank" rel="noopener">Visit Website</a>';
            $output .= '</div>';
        }
        
        $output .= '</div>';
    }
    
    $output .= '</div>';
    
    return $output;
}

/**
 * Shortcode for displaying lead generation form
 *
 * @param array $atts Shortcode attributes
 * @return string Shortcode output
 */
function rolloff_rates_form_shortcode($atts) {
    $atts = shortcode_atts(array(
        'city' => '',
        'state' => '',
        'title' => 'Get a Dumpster Rental Quote',
        'submit_text' => 'Submit',
        'success_message' => 'Thank you for your submission! We will contact you shortly.',
        'class' => '',
    ), $atts, 'rolloff_form');
    
    $city = $atts['city'];
    $state = $atts['state'];
    
    if (empty($city) || empty($state)) {
        global $rolloff_city_data;
        
        if ($rolloff_city_data) {
            $city = $rolloff_city_data['city'];
            $state = $rolloff_city_data['state'];
        }
    }
    
    $output = '<div id="rolloff-rates-form" class="rolloff-rates-form-container ' . esc_attr($atts['class']) . '">';
    
    if (!empty($atts['title'])) {
        $output .= '<h3 class="rolloff-rates-form-title">' . esc_html($atts['title']) . '</h3>';
    }
    
    $output .= '<form class="rolloff-rates-form" method="post">';
    $output .= wp_nonce_field('rolloff_rates_form_nonce', 'rolloff_rates_nonce', true, false);
    
    if (!empty($city)) {
        $output .= '<input type="hidden" name="city" value="' . esc_attr($city) . '">';
    }
    
    if (!empty($state)) {
        $output .= '<input type="hidden" name="state" value="' . esc_attr($state) . '">';
    }
    
    $output .= '<div class="rolloff-rates-form-field">';
    $output .= '<label for="rolloff-rates-name">Name <span class="required">*</span></label>';
    $output .= '<input type="text" id="rolloff-rates-name" name="name" required>';
    $output .= '</div>';
    
    $output .= '<div class="rolloff-rates-form-field">';
    $output .= '<label for="rolloff-rates-email">Email <span class="required">*</span></label>';
    $output .= '<input type="email" id="rolloff-rates-email" name="email" required>';
    $output .= '</div>';
    
    $output .= '<div class="rolloff-rates-form-field">';
    $output .= '<label for="rolloff-rates-phone">Phone <span class="required">*</span></label>';
    $output .= '<input type="tel" id="rolloff-rates-phone" name="phone" required>';
    $output .= '</div>';
    
    $output .= '<div class="rolloff-rates-form-field">';
    $output .= '<label for="rolloff-rates-address">Address</label>';
    $output .= '<input type="text" id="rolloff-rates-address" name="address">';
    $output .= '</div>';
    
    if (empty($city)) {
        $output .= '<div class="rolloff-rates-form-field">';
        $output .= '<label for="rolloff-rates-city">City <span class="required">*</span></label>';
        $output .= '<input type="text" id="rolloff-rates-city" name="city" required>';
        $output .= '</div>';
    }
    
    if (empty($state)) {
        $output .= '<div class="rolloff-rates-form-field">';
        $output .= '<label for="rolloff-rates-state">State <span class="required">*</span></label>';
        $output .= '<input type="text" id="rolloff-rates-state" name="state" required>';
        $output .= '</div>';
    }
    
    $output .= '<div class="rolloff-rates-form-field">';
    $output .= '<label for="rolloff-rates-size">Dumpster Size</label>';
    $output .= '<select id="rolloff-rates-size" name="size">';
    $output .= '<option value="">Select a size</option>';
    $output .= '<option value="10">10 yard</option>';
    $output .= '<option value="15">15 yard</option>';
    $output .= '<option value="20">20 yard</option>';
    $output .= '<option value="30">30 yard</option>';
    $output .= '<option value="40">40 yard</option>';
    $output .= '</select>';
    $output .= '</div>';
    
    $output .= '<div class="rolloff-rates-form-field">';
    $output .= '<label for="rolloff-rates-message">Message</label>';
    $output .= '<textarea id="rolloff-rates-message" name="message" rows="4"></textarea>';
    $output .= '</div>';
    
    $output .= '<div class="rolloff-rates-form-field">';
    $output .= '<button type="submit" class="rolloff-rates-submit-button">' . esc_html($atts['submit_text']) . '</button>';
    $output .= '</div>';
    
    $output .= '</form>';
    
    $output .= '<div class="rolloff-rates-form-success" style="display: none;">';
    $output .= '<p>' . esc_html($atts['success_message']) . '</p>';
    $output .= '</div>';
    
    $output .= '</div>';
    
    $output .= '<script>
        jQuery(document).ready(function($) {
            $(".rolloff-rates-form").on("submit", function(e) {
                e.preventDefault();
                
                var form = $(this);
                var formData = form.serialize();
                
                $.ajax({
                    url: rolloffRatesData.ajaxUrl,
                    type: "POST",
                    data: {
                        action: "rolloff_rates_submit_form",
                        nonce: rolloffRatesData.nonce,
                        formData: formData
                    },
                    success: function(response) {
                        if (response.success) {
                            form.hide();
                            form.siblings(".rolloff-rates-form-success").show();
                        } else {
                            alert("Error: " + response.data.message);
                        }
                    },
                    error: function() {
                        alert("An error occurred. Please try again later.");
                    }
                });
            });
        });
    </script>';
    
    return $output;
}
