document.body.style.backgroundImage = "url('images/img1.jpg')";
$(document).ready(function() {
                var img_array = [1, 2, 3],
                    newIndex = 0,
                    index = 0,
                    interval = 30000;
                (function changeBg() {

                    index = (index + 1) % img_array.length;

                    $('body').css('backgroundImage', function() {
                        $('#fullPage').animate({
                            backgroundColor: 'transparent'
                        }, 1000, function() {
                            setTimeout(function() {
                                $('#fullPage').animate({
                                    backgroundColor: 'rgb(255,255,255)'
                                }, 1000);
                            }, 3000);
                        });
                        return 'url(images/background/img' + img_array[index] + '.jpg)';
                    });
                    setTimeout(changeBg, interval);
                })();
            });