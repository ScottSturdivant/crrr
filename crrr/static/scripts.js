function faqToggle(obj) {
    if (!document.getElementById(obj).style.display ||
document.getElementById(obj).style.display == "none") {
        document.getElementById(obj).style.display = "block";
    }
    else {
        document.getElementById(obj).style.display = "none";
    }
}

over = function() {
    var sfEls = document.getElementById("nav").getElementsByTagName("LI");
    for (var i=0; i<sfEls.length; i++) {
        sfEls[i].onmouseover=function() {
            this.className+=" over";
        }
        sfEls[i].onmouseout=function() {
            this.className=this.className.replace(new RegExp(" over\\b"), "");
        }
    }
}
if (window.attachEvent) window.attachEvent("onload", over);
