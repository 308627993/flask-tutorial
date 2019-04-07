$(function() {
	var category = $("#category");
	var teacher = $("#teacher");
	var student = $("#student");
	var pre_category = "<option value=\"\">选择科目</option>";
	var pre_teacher = "<option value=\"\">选择老师</option>";
	var pre_student = "<option value=\"\">选择学员</option>";

	//初始化
	category.html(pre_category);
	teacher.html(pre_teacher);
	student.html(pre_student);

	$.ajax({
		type : "GET",
		url : "/api/category",
		cache:false,
		success:function(data){$.each(data,function(){category.append("<option  value=" + this.name + ">" + this.name + "</option>");})}
		})

		category.change(function() {
			if (category.val() != "") {
				teacher.html(pre_teacher);
				console.log(category.val());
				$.ajax({
					type : "GET",
					url : "/",
					cache:false,
					success : function(){}
				});

			}
		});

	}	)
