window.onload = function createRating(evt, rating){

    alert(id);
    var container = document.getElementById(id);

    var span = document.createElement("SPAN");
    span.className = "score";
    span.style.marginTop = "-5%";

    var div_wrap = document.createElement("DIV");
    div_wrap.className = "score-wrap";

    var span_stars = document.createElement("SPAN");
    span_stars.className = "stars-active";
    span_stars.style.width = rating + '%';

    var star_on = document.createElement("I");
    star_on.className = "fa fa-star";
    star_on.ariaHidden = "true";

    var span_stars_in = document.createElement("SPAN");
    span_stars_in.className = "stars-inactive";

    var star_off = document.createElement("I");
    star_off.className = "fa fa-star-o";
    star_off.ariaHidden = "false";

    span_stars.appendChild(star_on);
    span_stars.appendChild(star_on.cloneNode());
    span_stars.appendChild(star_on.cloneNode());
    span_stars.appendChild(star_on.cloneNode());
    span_stars.appendChild(star_on.cloneNode());

    span_stars_in.appendChild(star_off);
    span_stars_in.appendChild(star_off.cloneNode());
    span_stars_in.appendChild(star_off.cloneNode());
    span_stars_in.appendChild(star_off.cloneNode());
    span_stars_in.appendChild(star_off.cloneNode());

    div_wrap.appendChild(span_stars);
    div_wrap.appendChild(span_stars_in);

    span.appendChild(div_wrap);
    container.appendChild(span);
}