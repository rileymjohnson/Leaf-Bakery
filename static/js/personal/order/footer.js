var mar = (window.innerHeight - 570) + 104;
            if (mar > 0) {
                if (441 - (document.getElementById('panel').clientHeight - 26) >= 20) {
            document.getElementById('customFooter').style.marginTop = 441 - (document.getElementById('panel').clientHeight - 26) + "px";
            }
            else {
                document.getElementById('customFooter').style.marginTop = "20px;"
            }
            }
            window.onresize = function() {
                var mar = (window.innerHeight - 570) + 104;
                if (mar > 0) {
                    if (441 - (document.getElementById('panel').clientHeight - 26) >= 20) {
            document.getElementById('customFooter').style.marginTop = 441 - (document.getElementById('panel').clientHeight - 26) + "px";
            }
            else {
                document.getElementById('customFooter').style.marginTop = "20px;"
            }
                }
            }