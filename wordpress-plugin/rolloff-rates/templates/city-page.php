<?php
/**
 * Template for city-specific pages
 *
 * This template is used to display city-specific dumpster rental information.
 */

if (!defined('ABSPATH')) {
    exit;
}

global $rolloff_city_data;

if (!$rolloff_city_data) {
    wp_redirect(home_url());
    exit;
}

$city = $rolloff_city_data['city'];
$state = $rolloff_city_data['state'];
$companies = $rolloff_city_data['companies'];
$dumpster_sizes = $rolloff_city_data['dumpster_sizes'];
$prices = $rolloff_city_data['prices'];

$title = "Dumpster Rental in {$city}, {$state} - Compare Prices & Book Online";
$description = "Compare dumpster rental prices in {$city}, {$state} from top providers. Find the best deals on roll-off dumpsters and book online today.";

add_filter('pre_get_document_title', function() use ($title) {
    return $title;
});

add_action('wp_head', function() use ($title, $description, $city, $state) {
    echo '<meta name="description" content="' . esc_attr($description) . '">' . "\n";
    
    echo '<meta property="og:title" content="' . esc_attr($title) . '">' . "\n";
    echo '<meta property="og:description" content="' . esc_attr($description) . '">' . "\n";
    echo '<meta property="og:type" content="website">' . "\n";
    echo '<meta property="og:url" content="' . esc_url(home_url("dumpsters/{$city}/{$state}")) . '">' . "\n";
    
    echo '<meta name="twitter:card" content="summary">' . "\n";
    echo '<meta name="twitter:title" content="' . esc_attr($title) . '">' . "\n";
    echo '<meta name="twitter:description" content="' . esc_attr($description) . '">' . "\n";
    
    $schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'Service',
        'name' => "Dumpster Rental in {$city}, {$state}",
        'description' => $description,
        'areaServed' => array(
            '@type' => 'City',
            'name' => $city,
            'address' => array(
                '@type' => 'PostalAddress',
                'addressLocality' => $city,
                'addressRegion' => $state,
                'addressCountry' => 'US'
            )
        ),
        'provider' => array(
            '@type' => 'LocalBusiness',
            'name' => 'RollOff Rates',
            'telephone' => get_option('rolloff_rates_phone', ''),
            'url' => home_url()
        )
    );
    
    echo '<script type="application/ld+json">' . wp_json_encode($schema) . '</script>' . "\n";
});

get_header();
?>

<div class="rolloff-rates-city-page">
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <h1>Dumpster Rental in <?php echo esc_html($city); ?>, <?php echo esc_html($state); ?></h1>
                
                <div class="rolloff-rates-intro">
                    <p>Looking for affordable dumpster rentals in <?php echo esc_html($city); ?>, <?php echo esc_html($state); ?>? Compare prices from top providers and find the best deal for your waste disposal needs. Whether you're renovating your home, cleaning out your garage, or managing a construction project, we have the right dumpster size for you.</p>
                </div>
                
                <h2>Available Dumpster Sizes in <?php echo esc_html($city); ?></h2>
                
                <div class="rolloff-rates-sizes">
                    <?php foreach ($dumpster_sizes as $size): ?>
                        <div class="rolloff-rates-size-card">
                            <h3><?php echo esc_html($size['size']); ?> Yard Dumpster</h3>
                            <p class="rolloff-rates-size-dimensions"><?php echo esc_html($size['dimensions']); ?></p>
                            <p class="rolloff-rates-size-description"><?php echo esc_html($size['description']); ?></p>
                            
                            <?php
                            $lowest_price = null;
                            
                            foreach ($prices as $price) {
                                if ($price['size_id'] === $size['id']) {
                                    if ($lowest_price === null || $price['price'] < $lowest_price) {
                                        $lowest_price = $price['price'];
                                    }
                                }
                            }
                            ?>
                            
                            <?php if ($lowest_price !== null): ?>
                                <p class="rolloff-rates-size-price">Starting at $<?php echo esc_html(number_format($lowest_price, 2)); ?></p>
                            <?php endif; ?>
                            
                            <a href="#rolloff-rates-form" class="rolloff-rates-cta-button">Get a Quote</a>
                        </div>
                    <?php endforeach; ?>
                </div>
                
                <h2>Dumpster Rental Prices in <?php echo esc_html($city); ?>, <?php echo esc_html($state); ?></h2>
                
                <?php echo do_shortcode('[rolloff_table city="' . esc_attr($city) . '" state="' . esc_attr($state) . '"]'); ?>
                
                <div class="rolloff-rates-city-content">
                    <h2>Dumpster Rental Services in <?php echo esc_html($city); ?></h2>
                    
                    <p>When you need a dumpster rental in <?php echo esc_html($city); ?>, <?php echo esc_html($state); ?>, you want a reliable service that offers fair prices and excellent customer service. Our comparison tool helps you find the best dumpster rental companies in your area, with transparent pricing and detailed information about each provider.</p>
                    
                    <h3>Top Dumpster Rental Companies in <?php echo esc_html($city); ?></h3>
                    
                    <?php echo do_shortcode('[rolloff_companies city="' . esc_attr($city) . '" state="' . esc_attr($state) . '" layout="grid"]'); ?>
                    
                    <h3>How to Choose the Right Dumpster Size</h3>
                    
                    <p>Selecting the right dumpster size is crucial for your project. Here's a quick guide to help you choose:</p>
                    
                    <ul>
                        <li><strong>10 Yard Dumpsters:</strong> Ideal for small projects like garage cleanouts or small bathroom renovations.</li>
                        <li><strong>15 Yard Dumpsters:</strong> Perfect for medium-sized projects like deck removal or large garage cleanouts.</li>
                        <li><strong>20 Yard Dumpsters:</strong> Great for home renovations, large deck removals, or small roofing projects.</li>
                        <li><strong>30 Yard Dumpsters:</strong> Suitable for major home renovations, new construction, or large roofing projects.</li>
                        <li><strong>40 Yard Dumpsters:</strong> Best for commercial projects, large-scale construction, or complete home cleanouts.</li>
                    </ul>
                    
                    <h3>Dumpster Rental FAQs for <?php echo esc_html($city); ?>, <?php echo esc_html($state); ?></h3>
                    
                    <div class="rolloff-rates-faqs">
                        <div class="rolloff-rates-faq">
                            <h4>How much does it cost to rent a dumpster in <?php echo esc_html($city); ?>?</h4>
                            <p>Dumpster rental prices in <?php echo esc_html($city); ?>, <?php echo esc_html($state); ?> typically range from $<?php echo esc_html(number_format(min(array_column($prices, 'price')), 2)); ?> to $<?php echo esc_html(number_format(max(array_column($prices, 'price')), 2)); ?>, depending on the size and rental period. Use our comparison tool above to find the best price for your needs.</p>
                        </div>
                        
                        <div class="rolloff-rates-faq">
                            <h4>How long can I keep a rented dumpster?</h4>
                            <p>Most companies in <?php echo esc_html($city); ?> offer rental periods of 7-10 days as standard. Extended rentals are usually available for an additional fee.</p>
                        </div>
                        
                        <div class="rolloff-rates-faq">
                            <h4>What can I put in a dumpster?</h4>
                            <p>You can dispose of most household and construction debris, including furniture, appliances, yard waste, and renovation materials. However, hazardous materials, electronics, tires, and certain other items are typically prohibited.</p>
                        </div>
                        
                        <div class="rolloff-rates-faq">
                            <h4>Do I need a permit to place a dumpster in <?php echo esc_html($city); ?>?</h4>
                            <p>If you're placing the dumpster on your private property, you typically don't need a permit. However, if you need to place it on a public street or sidewalk, you'll likely need a permit from the <?php echo esc_html($city); ?> municipal office.</p>
                        </div>
                    </div>
                </div>
                
                <h2>Get a Dumpster Rental Quote in <?php echo esc_html($city); ?>, <?php echo esc_html($state); ?></h2>
                
                <?php echo do_shortcode('[rolloff_form city="' . esc_attr($city) . '" state="' . esc_attr($state) . '"]'); ?>
            </div>
        </div>
    </div>
</div>

<?php
get_footer();
?>
