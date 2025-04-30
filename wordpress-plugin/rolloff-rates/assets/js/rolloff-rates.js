/**
 * RollOff Rates Plugin JavaScript
 */

(function($) {
    'use strict';

    $(document).ready(function() {
        initFormSubmission();
    });

    /**
     * Initialize form submission handling
     */
    function initFormSubmission() {
        $('.rolloff-rates-form').on('submit', function(e) {
            e.preventDefault();
            
            var form = $(this);
            var formData = form.serialize();
            var submitButton = form.find('.rolloff-rates-submit-button');
            
            submitButton.prop('disabled', true).text('Submitting...');
            
            $.ajax({
                url: rolloffRatesData.ajaxUrl,
                type: 'POST',
                data: {
                    action: 'rolloff_rates_submit_form',
                    nonce: rolloffRatesData.nonce,
                    formData: formData
                },
                success: function(response) {
                    if (response.success) {
                        form.hide();
                        form.siblings('.rolloff-rates-form-success').show();
                    } else {
                        alert('Error: ' + response.data.message);
                        submitButton.prop('disabled', false).text('Submit');
                    }
                },
                error: function() {
                    alert('An error occurred. Please try again later.');
                    submitButton.prop('disabled', false).text('Submit');
                }
            });
        });
    }

})(jQuery);
