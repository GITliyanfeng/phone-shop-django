$("#fileUpload").on('change', function () {

    if (typeof (FileReader) != "undefined") {

        var image_holder = $("#image-holder");
        image_holder.empty();

        var reader = new FileReader();
        reader.onload = function (e) {
            $("<label class='am-form-label'>新头像</label>").appendTo(image_holder);
            $("<img />", {
                "src": e.target.result,
                "class": "thumb-image",
                "width": "105px",
            }).appendTo(image_holder);

        }
        image_holder.show();
        reader.readAsDataURL($(this)[0].files[0]);
    } else {
        alert("你的浏览器不支持FileReader.");
    }
});