$(document).ready(function() {

    let circle = $('#wheel .circle');
    let values = $('#wheel .values');

    function splitCircle()
    {
        let lines = values.val().split(/\r?\n|\r|\n/g);
        let slices = lines.length;

        if (slices > 180) {
            $('#wheel .error').show();
            return;
        } else {
            $('#wheel .error').hide();
        }

        (slices < 2) ? circle.addClass('single') : circle.removeClass('single');
        (slices > 40) ? circle.addClass('sm') : circle.removeClass('sm');
        (slices > 80) ? circle.addClass('xs') : circle.removeClass('xs');
        (slices > 120) ? circle.addClass('xxs') : circle.removeClass('xxs');

        let sliceDeg = 360/slices;

        circle.html('');
        for (let i = 0; i < slices; i ++) {
            let li = $('<li><div><span>' + lines[i] + '</span></div></li>');

            let addDeg = (slices > 4) ? 1*sliceDeg/4 : 3*sliceDeg/4;

            li.css({
                'clip-path': 'polygon(0 -100px, 500px 50%, calc(300px * cos(' + sliceDeg + 'deg - 90deg)) calc(50% + 300px * sin(' + sliceDeg + 'deg - 90deg)), 0 50%)',
                'transform': 'rotate(' + (i*sliceDeg) + 'deg) translateZ(0)',
                'background': 'hsla(' + (i*sliceDeg + addDeg) + ', 100%, 45%, 1)'
            });
            li.find('div').css({
                'transform': 'rotate(-' + (90-sliceDeg/2) + 'deg)'
            });

            circle.append(li);
        }
    }
    splitCircle();

    values.on('keydown', function () {
        if (circle.is('.spin')) return false;
    });
    values.on('keyup', function () {
        splitCircle();
    });
    $('#wheel .presets a').on('click', function () {
        if (circle.is('.spin')) return;

        let data = $(this).data('values');
        data = data.replaceAll('/', "\n");
        values.val(data);
        splitCircle();
    });
    $('#wheel .clear span').on('click', function () {
        if (circle.is('.spin')) return;

        values.val('');
        splitCircle();
    });

    let min = 720;
    let max = 1980;
    let start = 0;
    let stop = 0;

    $('#button.wheel').on('click', function() {
		if ((circle.find('li').length == 1) && (circle.text() == '')) return;
        if (circle.is('.spin')) return;
		
        circle.addClass('spin');

        stop = start + Math.random() * (max - min + 1) + min;

        $({deg: start}).animate({deg: stop}, {
            duration: 3000,
            easing: 'easeOutCubic',
            step: function(now){
                circle.css({
                    'transform': 'rotate(' + now + 'deg)'
                });
            },
            complete: function() {
                let circleDeg = (stop - 90) % 360;
                let slices = $('#wheel .circle').find('li').length;
                let sliceDeg = 360/slices;
                let value = slices - Math.floor(circleDeg/sliceDeg);

                $('h1').text($('h1').data('title') + circle.find('li:nth-child(' + value + ')').text());
                circle.removeClass('spin');
            }
        });

        start = stop;

        if ($(window).scrollTop() > $('h1').offset().top) {
            $('html, body').animate({scrollTop: $('h1').offset().top - 5}, 'slow');
        }
    });
	
	$('#wheel .dot').on('click', function() {
		$('#button.wheel').click();
	});

});