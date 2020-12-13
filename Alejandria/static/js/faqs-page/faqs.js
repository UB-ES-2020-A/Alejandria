$(document).ready(function() {
    load_defaults();
    state_apply();
    const option_select = document.getElementById("inputGroupOp");
    option_select.addEventListener("change",function () {
        const question_select = document.getElementById("questionSelect")
        const category_select = document.getElementById("category")
        const question_text = document.getElementById("question")
        const answer_text = document.getElementById("answer")
        let value = $(this).val()
        switch(value) {
            case '1':
                question_select.disabled = true;
                category_select.disabled = false;
                question_text.disabled = false;
                question_text.value = "";
                answer_text.disabled = false;
                answer_text.value = "";
                break;
            case '2':
                question_select.disabled = false;
                category_select.disabled = false;
                question_text.disabled = false;
                question_text.value = "";
                answer_text.disabled = false;
                answer_text.value = "";
                break;
            case '3':
                question_select.disabled = false;
                category_select.disabled = true;
                question_text.disabled = true;
                question_text.value = "Disabled";
                answer_text.disabled = true;
                answer_text.value = "Disabled";
                break;
            default:
                load_defaults();
                break;
        }
    })

    const apply = document.getElementById("apply_btn")
    apply.addEventListener("click", function () {
        const operation_select = document.getElementById("inputGroupOp")
        const question_select = document.getElementById("questionSelect")
        const category_select = document.getElementById("category")
        const question_text = document.getElementById("question")
        const answer_text = document.getElementById("answer")

        var url = window.location.origin;
        setCSRF();

        let value = operation_select.value
        switch(value) {
            case '1':
                url = url + '/addfaq/'
                console.log(category_select.options[category_select.selectedIndex].text)
                $.ajax(url, {
                    method: "POST", //TODO: Do every ajax to modify faqs page.
                    data: {
                        category: category_select.options[category_select.selectedIndex].text,
                        question: question_text.value,
                        answer: answer_text.value
                    },
                    ContentType: 'application/x-www-form-urlencode',
                    success: function (response) {
                        if (!response.error) {
                            Swal.fire({
                                icon: 'success',
                                title: 'Added Succesfully',
                                text: 'Your FAQ was added succesfully',
                            })
                            $(".swal2-confirm").click(function () {
                                window.location.href = "";
                            });
                        }
                    },
                    error: function () {
                        Swal.fire({
                                icon: 'error',
                                title: 'Oops...',
                                text: 'Something went wrong!',
                        })
                        $(".swal2-confirm").click(function () {
                            window.location.href = "";
                        });
                    }
                })
                break;
            case '2':
                url = url + '/modifyfaq/'
                $.ajax(url, {
                    method: "POST", //TODO: Do every ajax to modify faqs page.
                    data: {
                        original: question_select.options[question_select.selectedIndex].text,
                        category: category_select.options[category_select.selectedIndex].text,
                        question: question_text.value,
                        answer: answer_text.value
                    },
                    ContentType: 'application/x-www-form-urlencode',
                    success: function (response) {
                        if (response.error) {
                            Swal.fire({
                                icon: 'error',
                                title: 'Oops...',
                                text: 'Something went wrong!',
                            })
                        } else {
                            Swal.fire({
                                icon: 'success',
                                title: 'Modified Succesfully',
                                text: 'Your FAQ was modified succesfully',
                            })
                            $(".swal2-confirm").click(function () {
                                window.location.href = "";
                            });
                        }
                    },
                    error: function () {
                        Swal.fire({
                                icon: 'error',
                                title: 'Oops...',
                                text: 'Something went wrong!',
                        })
                        $(".swal2-confirm").click(function () {
                            window.location.href = "";
                        });
                    }
                })
                break;
            case '3':
                url = url + '/deletefaq/'
                $.ajax(url, {
                    method: "POST",
                    data: {
                        original: question_select.options[question_select.selectedIndex].text,
                    },
                    ContentType: 'application/x-www-form-urlencode',
                    success: function (response) {
                        if (response.error) {
                            Swal.fire({
                                icon: 'error',
                                title: 'Oops...',
                                text: 'Something went wrong!',
                            })
                        } else {
                            Swal.fire({
                                icon: 'success',
                                title: 'Deleted Succesfully',
                                text: 'Your FAQ was deleted succesfully',
                            })
                            $(".swal2-confirm").click(function () {
                                window.location.href = "";
                            });
                        }
                    },
                    error: function () {
                        Swal.fire({
                                icon: 'error',
                                title: 'Oops...',
                                text: 'Something went wrong!',
                        })
                        $(".swal2-confirm").click(function () {
                            window.location.href = "";
                        });
                    }
                })
                break;
            default:
                load_defaults();
                break;
        }

    })

    const check = document.getElementById("checkbox1");
    check.addEventListener("click", function () {state_apply();})

    function load_defaults(){
        const operation_select = document.getElementById("inputGroupOp")
        const question_select = document.getElementById("questionSelect")
        const category_select = document.getElementById("category")
        const question_text = document.getElementById("question")
        const answer_text = document.getElementById("answer")

        const check = document.getElementById("checkbox1");

        category_select.disabled = false;
        category_select.selectedIndex = '0';
        operation_select.selectedIndex = '0';
        question_select.selectedIndex = '0';
        question_select.disabled = false;
        question_text.disabled = false;
        question_text.value = "";
        answer_text.disabled = false;
        answer_text.value = "";

        check.checked = false;
    }

    function state_apply(){
        const applybtn = document.getElementById("apply_btn");
        const check = document.getElementById("checkbox1");
        applybtn.disabled = !check.checked;
    }

})
