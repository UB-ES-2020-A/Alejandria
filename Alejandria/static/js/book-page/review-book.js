{% if user.is_authenticated %}
        {% if form.desired %}
            $('#desired').checked = true;
            console.log('estic true')
            $('#desired-icon').css({'color': '#dc3545'});
        {% else %}
            $('#desired').checked = false;
            $('#desired-icon').css({'color': '#141414'});
        {% endif %}

        {% if form.readed %}
            console.log('llegit');
            $('#readed').checked = true;
            $('#readed-icon').css({'color': '#80471C'});
        {% else %}
         console.log('no llegit');
            $('#readed').checked = false;
            $('#readed-icon').css({'color': '#141414'});
        {% endif %}
    {% endif %}


    function toggleCheckbox(element)
     {
       if(element.checked){
          $('#desired-icon').css({'color': '#dc3545'});
          console.log("like");
       }
       else{
          $('#desired-icon').css({'color': '#141414'});
          console.log("not like");
       }

       $('#properties-form').submit();

     }

     function toggleCheckboxBook(element)
     {
       if(element.checked){
          $('#readed-icon').css({'color': '#80471C'});
          console.log("read");
       }
       else{
          $('#readed-icon').css({'color': '#141414'});
          console.log("not read");
       }
       $('#properties-form').submit();

     }






    var rating = 0;
    var list=['one','two','three','four','five'];
    list.forEach(function(element) {
        document.getElementById(element).addEventListener("click", function(){

            for(let i=0; i < list.length; i++){
                document.getElementById(list[i]).classList.remove("checked");
                document.getElementById(list[i]).classList.add("unchecked");
            }

            for(i=0; i < list.length; i++) {
                if(list[i] !== element) {
                    document.getElementById(list[i]).classList.remove("unchecked");
                    document.getElementById(list[i]).classList.add("checked");
                }else{
                    document.getElementById(list[i]).classList.remove("unchecked");
                    document.getElementById(list[i]).classList.add("checked");
                    rating = i + 1;
                    break;
                }
            }
        });
    });

    $('#review-form').on('submit', function () {
        if(typeof {{ user.id }} == undefined){
            alert("You need to log in to leave a review");
            return false;
        }

        if({{ owned }} == false){
            alert("You need to buy the book first to review it.");
            return false;
        }

        var post_url = '../../review/';

        var form = $('#review-form')[0];
        var formData = new FormData(form);
        var book = "{{ book.ISBN }}";
        var user_id = {{ user.id }};
        formData.append('book', book);
        formData.append('user_id', user_id);
        formData.append('text', document.getElementById('review-text-input').value);
        formData.append('score', rating);
        formData.append('adding', "true");

        $.ajax({
            url: post_url,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success:function(response){
                console.log("response");
                console.log(response.message);
                alert(response.message);
                window.location.reload();
            },
            error:function(response){
                console.log("response");
                console.log(response.responseJSON.message);
                console.log(response.status);
                alert(response.responseJSON.message);
            }
        });

        return false;
    });

    function onSubmitModifyReview(review_id, rating) {
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        var post_url = '../../review/';
        var form = $('#modify-review-form')[0];
        var formData = new FormData(form);
        formData.append('review_id', review_id);
        formData.append('text', document.getElementById('modify-review-text-input').value);
        formData.append('score', rating);
        formData.append('modifying', "true");
        formData.append('csrfmiddlewaretoken', csrf);

        $.ajax({
            url: post_url,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success:function(response){
                console.log("response");
                console.log(response.message);
                alert(response.message);
                window.location.reload();
            },
            error:function(response){
                console.log("response");
                console.log(response.responseJSON.message);
                console.log(response.status);
                alert(response.responseJSON.message);
            }
        });

        return false;
    }

    function onSubmitDeleteReview(review_id){
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        var post_url = '../../review/';
        var form = $('#delete-review-form')[0];
        var formData = new FormData(form);
        formData.append('review_id', review_id);
        formData.append('deleting', "true");
        formData.append('csrfmiddlewaretoken', csrf);

        $.ajax({
            url: post_url,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success:function(response){
                console.log("success");
                console.log(response.message);
                alert(response.message);
                window.location.reload();
            },
            error:function(response){
                console.log("error");
                console.log(response.responseJSON.message);
                console.log(response.status);
                alert(response.responseJSON.message);
            }
        });

        return false;
    }

    function startModifyingReview(review_id){
        $("#review-div-" + review_id).html(
            "<div class=\"container\" style=\"margin-left: 8%; margin-top: 20px;\">\n" +
            "    <form class=\"form-group\" id=\"modify-review-form\" post_url=\"review/\">\n" +
            "        <div class=\"main\">\n" +
            "            <i class=\"fa fa-star unchecked\" id=\"modify-one\"></i>\n" +
            "            <i class=\"fa fa-star unchecked\" id=\"modify-two\"></i>\n" +
            "            <i class=\"fa fa-star unchecked\" id=\"modify-three\"></i>\n" +
            "            <i class=\"fa fa-star unchecked\" id=\"modify-four\"></i>\n" +
            "            <i class=\"fa fa-star unchecked\" id=\"modify-five\"></i>\n" +
            "        </div>\n" +
            "        <textarea id=\"modify-review-text-input\" style=\"height: 100px; margin-top: 20px; margin-bottom: 20px;\" type=\"text\" class=\"form-control mr-sm-2\" placeholder=\"Submit your review here\"></textarea>\n" +
            "        <button type=\"submit\" class=\"btn btn-danger\" onclick=\"cancelModifyingReview(" + review_id + ")\">Cancel</button>\n" +
            "        <button type=\"submit\" class=\"btn btn-danger\" onclick=\"onSubmitModifyReview(" + review_id + ", modifiedRating)\">Submit</button>\n" +
            "    </form>\n" +
            "</div>");

        var textInput = "";
        var modifiedRating = 0;
        var modifyList=['modify-one', 'modify-two', 'modify-three', 'modify-four', 'modify-five']
        modifyList.forEach(function(element) {
            document.getElementById(element).addEventListener("click", function(){
                for(let i=0; i < modifyList.length; i++){
                    document.getElementById(modifyList[i]).classList.remove("checked");
                    document.getElementById(modifyList[i]).classList.add("unchecked");
                }

                for(i=0; i < modifyList.length; i++) {
                    if(modifyList[i] !== element) {
                        document.getElementById(modifyList[i]).classList.remove("unchecked");
                        document.getElementById(modifyList[i]).classList.add("checked");
                    }else{
                        document.getElementById(modifyList[i]).classList.remove("unchecked");
                        document.getElementById(modifyList[i]).classList.add("checked");
                        modifiedRating = i + 1;
                        textInput = document.getElementById("modify-review-text-input").value;
                        $("#review-div-" + review_id).html(
                            "<div class=\"container\" style=\"margin-left: 8%; margin-top: 20px;\">\n" +
                            "    <form class=\"form-group\" id=\"modify-review-form\" post_url=\"review/\">\n" +
                            "        <div class=\"main\">\n" +
                            "            <i class=\"fa fa-star " + document.getElementById(modifyList[0]).classList.item(2) + " id=\"modify-one\"></i>\n" +
                            "            <i class=\"fa fa-star " + document.getElementById(modifyList[1]).classList.item(2) + " id=\"modify-two\"></i>\n" +
                            "            <i class=\"fa fa-star " + document.getElementById(modifyList[2]).classList.item(2) + " id=\"modify-three\"></i>\n" +
                            "            <i class=\"fa fa-star " + document.getElementById(modifyList[3]).classList.item(2) + " id=\"modify-four\"></i>\n" +
                            "            <i class=\"fa fa-star " + document.getElementById(modifyList[4]).classList.item(2) + " id=\"modify-five\"></i>\n" +
                            "        </div>\n" +
                            "        <textarea id=\"modify-review-text-input\" style=\"height: 100px; margin-top: 20px; margin-bottom: 20px;\" type=\"text\" class=\"form-control mr-sm-2\" placeholder=\"Submit your review here\"></textarea>\n" +
                            "        <button type=\"submit\" class=\"btn btn-danger\" onclick=\"cancelModifyingReview(" + review_id + "," + modifiedRating + ")\">Cancel</button>\n" +
                            "        <button type=\"submit\" class=\"btn btn-danger\" onclick=\"onSubmitModifyReview(" + review_id + "," + modifiedRating + ")\">Submit</button>\n" +
                            "    </form>\n" +
                            "</div>");
                        document.getElementById("modify-review-text-input").value = textInput;
                        break;
                    }
                }
            });
        });
    }

    function cancelModifyingReview(review_id){
        $("#review-div-" + review_id).html(
            "<button style=\"height:40px\" type=\"submit\" class=\"btn btn-danger\" onclick=\"startModifyingReview(" + review_id + ")\">Modify</button>\n" +
            "   <form class=\"form-group\" id=\"delete-review-form\" onsubmit=\"return onSubmitDeleteReview(" + review_id + ")\">\n" +
            "       <button style=\"margin-left: 20px; height:40px\" type=\"submit\" class=\"btn btn-danger\">Delete</button>\n" +
            "   </form>");
    }


$(document).ready(function () {


    var itemsMainDiv = ('.MultiCarousel');
    var itemsDiv = ('.MultiCarousel-inner');
    var itemWidth = "";

    $('.leftLst, .rightLst').hover(function () {
        var condition = $(this).hasClass("leftLst");
        if (condition)
            click(0, this);
        else
            click(1, this);

    });

    ResCarouselSize();

    $(window).resize(function () {
        ResCarouselSize();
    });

    //this function define the size of the items
    function ResCarouselSize() {
        var incno = 0;
        var dataItems = ("data-items");
        var itemClass = ('.item');
        var id = 0;
        var btnParentSb = '';
        var itemsSplit = '';
        var sampwidth = $(itemsMainDiv).width();
        var bodyWidth = $('body').width();
        $(itemsDiv).each(function () {
            id = id + 1;
            var itemNumbers = $(this).find(itemClass).length;
            btnParentSb = $(this).parent().attr(dataItems);
            itemsSplit = btnParentSb.split(',');
            $(this).parent().attr("id", "MultiCarousel" + id);


            if (bodyWidth >= 1200) {
                incno = itemsSplit[3];
                itemWidth = sampwidth / (incno*1.75);
            }
            else if (bodyWidth >= 992) {
                incno = itemsSplit[2];
                itemWidth = sampwidth / (incno*1.75);
            }
            else if (bodyWidth >= 768) {
                incno = itemsSplit[1];
                itemWidth = sampwidth / (incno*1.75);
            }
            else {
                incno = itemsSplit[0];
                itemWidth = sampwidth / (incno*1.75);
            }
            itemWidth = 190 /* distancia entre carts */
            $(this).css({ 'transform': 'translateX(0px)', 'width': itemWidth * itemNumbers});
            $(this).find(itemClass).each(function () {
                $(this).outerWidth(itemWidth);
            });

            $(".leftLst").addClass("over");
            $(".rightLst").removeClass("over");

        });
    }


    //this function used to move the items
    function ResCarousel(e, el, s) {
        var leftBtn = ('.leftLst');
        var rightBtn = ('.rightLst');
        var translateXval = '';
        var divStyle = $(el + ' ' + itemsDiv).css('transform');
        var values = divStyle.match(/-?[\d\.]+/g);
        var xds = Math.abs(values[4]);
        if (e === 0) {
            translateXval = parseInt(xds) - parseInt(itemWidth * s);
            $(el + ' ' + rightBtn).removeClass("over");

            if (translateXval <= itemWidth / 2) {
                translateXval = 0;
                $(el + ' ' + leftBtn).addClass("over");
            }
        }
        else if (e == 1) {
            var itemsCondition = $(el).find(itemsDiv).width() - $(el).width();
            translateXval = parseInt(xds) + parseInt(itemWidth * s);
            $(el + ' ' + leftBtn).removeClass("over");

            if (translateXval >= itemsCondition - itemWidth / 2) {
                translateXval = itemsCondition;
                $(el + ' ' + rightBtn).addClass("over");
            }
        }
        $(el + ' ' + itemsDiv).css('transform', 'translateX(' + -translateXval + 'px)');
    }

    //It is used to get some elements from btn
    function click(ell, ee) {
        var Parent = "#" + $(ee).parent().attr("id");
        var slide = $(Parent).attr("data-slide");
        ResCarousel(ell, Parent, slide);
    }

});