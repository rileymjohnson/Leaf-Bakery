var mar = (window.innerHeight - 480) + 104;
            if (mar > 0) {
                document.getElementById('customFooter').style.marginTop = mar + "px";
            }
            window.onresize = function() {
                var mar = (window.innerHeight - 480) + 104;
                if (mar > 0) {
                    document.getElementById('customFooter').style.marginTop = mar + "px";
                }
            }