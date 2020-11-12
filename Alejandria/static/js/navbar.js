$(document).ready(function () {
        $("#register_btn").click(function () {
            window.location.href = window.location.origin+"/register";
        });

        $(".navbar-brand").click(function () {
            window.location.href = window.location.origin;
        });

        $("#home_btn").click(function () {
            window.location.href = window.location.origin;
        });

        $("#login_btn").click(function () {
            window.location.href = window.location.origin+"/login";
        });

         $("#buttonSearch").click(function () {
            book_name = document.getElementById('textSearch').value;
            if(book_name!=""){
                var urlname = window.location.origin+"/search";
                var url = new URL(urlname);
                url.searchParams.append('search_book', document.getElementById('textSearch').value);
                window.location.href = url;
                //window.location.href = "/search/" + document.getElementById('textSearch').value; //window.location.origin+"/login";
            }
            else{ //TODO: Falta fer el search buit...
                console.log("NULL");
                window.location.href = "/search";
             }

        });

    }
);