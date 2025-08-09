$(document).ready(function() {

    history.pushState('', document.title, window.location.pathname);

    let winForm = $('.win-form');
	let winPay  = $('.win-pay');

    winForm.on('input', '[name="link"]', function () {
        let input    = $(this);
        let wrapper  = $('#wrapper');
        let link     = winForm.find('.post .link');
        let status   = winForm.find('.post .status');
        let user     = winForm.find('.post .user');
        let counters = winForm.find('.post .counters');
        let settings = winForm.find('.settings');
        let buttons  = winForm.find('.buttons');
        let page     = winForm.is('.winig-form') ? 'winig' : (winForm.is('.wintg-form') ? 'wintg' : 'winvk');
		

        link.addClass('load').find('input').attr('disabled', 'disabled');

        $.ajax({
            url: "/" + page + "/info/",
            data: {link: input.val()},
            success: function(resp) {
                link.removeClass('load').find('input').removeAttr('disabled');

                status.removeClass('show');
                user.removeClass('show');
                counters.removeClass('show');

                if (resp.error && !resp.link.url) {
                    settings.hide();
                    buttons.hide();
                    wrapper.removeClass('wrapper-img').attr('style', '');
                    link.attr('class', 'link default');

                    return false;
                }

                if ((resp.error && !resp.link.valid)
                    || (resp.error && resp.auth.login && !resp.post)
                ) {
                    settings.hide();
                    buttons.hide();
                    wrapper.removeClass('wrapper-img').attr('style', '');
                    link.attr('class', 'link error');
                    status.addClass('show').html(resp.error);

                    return false;
                }

                if (resp.error && !resp.auth.login) {
                    settings.hide();
                    buttons.hide();
                    wrapper.removeClass('wrapper-img').attr('style', '');
                    link.attr('class', 'link warning');
                    status.addClass('show').html(resp.error);

                    return false;
                }

                settings.show();
                buttons.show();
                wrapper.addClass('wrapper-img').css('background-image', 'url(' + resp.post.item.photo.big + ')');

                link.attr('class', 'link success');

                user.addClass('show')
                    .find('.name').text(resp.user.first_name);

                counters.addClass('show')
                    .find('.comments').text(resp.post.item.comments).end()
                    .find('.likes').text(resp.post.item.likes).end()
                    .find('.reposts').text(resp.post.item.reposts);
            }
        });
    });

    if (winForm.find('[name="link"]').val()) {
        winForm.find('[name="link"]').trigger('input');
    }

    winForm.on('click', '.link .fa-times', function () {
        winForm.find('[name="link"]').val('');
        winForm.find('[name="link"]').trigger('input');
    });

    winForm.on('click', '.logout', function () {
        let page = winForm.is('.winig-form') ? 'winig' : (winForm.is('.wintg-form') ? 'wintg' : 'winvk');

        $.ajax({
            url: "/" + page + "/logout/",
            success: function() {
                location.reload();
            }
        });
    });

    winForm.on('change', '[name="filter"]', function () {
        if ($(this).val() !== 'comments') {
            $('.unique').hide();
        } else {
            $('.unique').show();
        }
    });

    winForm.on('change', '[name="count"]', function () {
        let input = $(this);
        let count = winForm.find('.settings .count');
        let value = input.val();

        if (value < parseInt(input.attr('min'))) {
            value = parseInt(input.attr('min'));
            input.val(value);
        }
        if (value > parseInt(input.attr('max'))) {
            value = parseInt(input.attr('max'));
            input.val(value);
        }

        count.find('span').text(
            wordCount(value, count.data('words').split(','))
        );
    });

    function wordCount($n, $words) {
        var $x = ($xx = $n%100)%10;
        return $words[((($xx > 10) && ($xx < 15)) || !$x || (($x > 4) && ($x < 10))) ? 2 : (($x == 1) ? 0 : 1)];
    }

    winForm.find('[name="tz"]').val(new Date().getTimezoneOffset());

    winForm.submit(function() {
        let page = winForm.is('.winig-form') ? 'winig' : (winForm.is('.wintg-form') ? 'wintg' : 'winvk');
		
		
        $('#load-dialog').dialog({
            width: 'auto',
            height: 90,
            modal: true,
            draggable: false,
            closeText: '',
            closeOnEscape : false,
        });
    });

    if (winForm.find('[name="finish"]').val()) {
        winForm.submit();
    }

    winForm.on('change', '[name="end"]', function () {
        let input = $(this);
        if (input.val() == 'time') {
            winForm.find('.settings .time').addClass('show');
        } else {
            winForm.find('.settings .time').removeClass('show')
        }
    });

    winForm.find('[name="time"]').each(function () {
        let input = $(this);
        let dtMin = new Date();
        let dtMax = new Date();
        dtMin.setTime(dtMin.getTime() + (60 * 60 * 1000));
        dtMax.setTime(dtMax.getTime() + (30 * 24 * 60 * 60 * 1000));

        input.datetimepicker({
            minDateTime: dtMin,
            maxDateTime: dtMax
        });

        if (!input.val()) {
            input.datetimepicker('setDate', dtMin);
        }
    });
	
	winPay.on('click', '[name="pay"]', function () {
        let page = winPay.is('.winig-pay') ? 'winig' : (winPay.is('.wintg-pay') ? 'wintg' : 'winvk');

    });
	
	// Окно правил
    $('#winvk-rule').click(function() {
        $('#rule-dialog').dialog({
            width: 'auto',
            modal: true,
            draggable: false,
            closeText: ''
        });
    });
});