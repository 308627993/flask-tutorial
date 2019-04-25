var sections = new Array();
var teacher = $("#teacher");
var student = $("#student");
var category = $("#category");
var startday = $("#startday");
var endday = $("#endday");
var weekday = $("#weekday");
var section = $("#section");
var exist_result = $("#exist_result");//显示已经存在的对象
var create_result = $("#create_result");//显示新创建的对象
var error_result = $("#error_result");
var error_ids = new Array();//用于记录已经存在的对象的id
var fields = new Array('category','teacher','student','weekday','section','startday','endday')

var pre_category = "<option value=\"\">选择科目</option>";
var pre_teacher = "<option value=\"\">选择老师</option>";
var pre_student = "<option value=\"\">选择学员</option>";

function create_course(){
	var all_data_ok = true;
	for(i in fields){
		if(eval(fields[i]+".val() == ''")){
			eval(fields[i] + ".parent().children('label').css('color','red')");
			all_data_ok = false;
		}
	}
	if (all_data_ok == true){
		var data = {'category':category.val(),'teacher':teacher.val(),'student':student.val(),'weekday':weekday.val(),'section':section.val(),'startday':startday.val(),'endday':endday.val()};
		$.ajax({
			type : "POST",
			data : data,
			url : "/api/course_arrange",
			cache:false,
			success:after_submit,
			//dataType:"json",
			})
	}
}

function after_submit(data){
	$("#exampleModal").modal('hide');
	exist_result.html('');
	create_result.html('');
	error_result.html('');
	var data = JSON.parse(data);
	var exist_data = data.exist_data;
	var create_data = data.create_data;
	var error_teacher_data = data.error_teacher_data;
	var error_student_data = data.error_student_data;
	if (exist_data.length != 0){
		var html = "<table class='table table-bordered'><tr><th colspan='5'>如下课程之前已经创建：</th></tr><tr><td>老师</td> <td>学生</td> <td>日期</td> <td>课时</td><td>ID</td></tr>"
		$.each(exist_data,function(){
			html += ("<tr><td>"+this.teacher+"</td> <td>"+this.student +"</td> <td>"+this.date+"</td> <td>"+this.section+"</td><td>"+this.id+"</td></tr>");
			});
		html += '</table>';
		exist_result.html(html);
	}
	if (create_data.length != 0){
		var html = "<table class='table table-bordered'><tr><th colspan='5'>新创建课程如下：</th></tr><tr><td>老师</td> <td>学生</td> <td>日期</td> <td>课时</td><td>ID</td></tr>"
		$.each(create_data,function(){html += ("<tr><td>"+this.teacher+"</td> <td>"+this.student +"</td> <td>"+this.date+"</td> <td>"+this.section+"</td><td>"+this.id+"</td></tr>")});
		html += '</table>';
		create_result.html(html);
	}
	if (error_teacher_data.length != 0 || error_student_data.length !=0){
		error_ids = [];//清空已经查询到的存在的对象的id
		var html = "<table class='table table-bordered'><tr><th colspan='5'>有冲突的课程如下：<div id='delete_btn' class='btn btn-danger' data-toggle='modal' data-target='#exampleModal' onclick='delete_exist()'>删除全部</div></th></tr><tr><td>老师</td> <td>学生</td> <td>日期</td> <td>课时</td><td>ID</td></tr>"
		if (error_teacher_data.length != 0){
			$.each(error_teacher_data,function(){html += ("<tr><td>"+this.teacher+"</td> <td style='color:red'>"+this.student +"</td> <td>"+this.date+"</td> <td>"+this.section+"</td><td>"+this.id+"</td></tr>");
				error_ids.push(this.id);});
		}
		if (error_student_data.length != 0){
			$.each(error_student_data,function(){html += ("<tr><td style='color:red'>"+this.teacher+"</td> <td>"+this.student +"</td> <td>"+this.date+"</td> <td>"+this.section+"</td><td>"+this.id+"</td></tr>");
				error_ids.push(this.id);});
		}
		html += '</table>';
		error_result.html(html);
		console.log(html);
	}
}

function delete_exist(){
	$.ajax({
		type : "POST",
		data : JSON.stringify({ids:error_ids}),
		url : "/api/course_delete",
		cache:false,
		success:after_delete,
		//dataType:"json",
		})
}

function after_delete(data){
	error_result.html('data删除完毕')
}

//function add_category(){
		//显示弹出框Modal
	//	$('#new_category_Modal').modal('show')
		//如果关闭按钮没有的话，增加一个
	//	if ($('#closebutton_create_category_id').length ==0){
		//	var close_button_html ="<button type='button' id='closebutton_create_category_id' class='btn btn-secondary' data-dismiss='modal' onclick='close_create_category()'>Close</button>";
		//	$('#category_form_id').append(close_button_html);
//		}
//}

//function close_create_category(){
	//点击关闭按钮时：首先隐藏弹出框，然后category的值清空
//	$('#new_category_Modal').modal('hide');//隐藏
//	category.val("");//清空category的值
//	$('#name').val("");
//}

//function create_category(){
//	console.log(1);
//}

function after_select_category(data){
	var teachers = data[0];
	var students = data[1];
	while(teachers.length != 0){t=teachers.pop();teacher.append("<option  value=" + t.id + ">" + t.name + "</option>")};
	while(students.length != 0){s=students.pop();student.append("<option  value=" + s.id + ">" + s.name + "</option>")};
	}

function change_label_color(field){
	if (eval(field + ".val()") != ""){
		eval(field + ".parent().children('label').css('color','black')");
	}
	else{
		eval(field + ".parent().children('label').css('color','red')");
	}
}

function create_category_success(data){
			var info = JSON.parse(data).info; // show response from the php script.
			var result = JSON.parse(data).result;
			if(result != 'fail'){
				//表示category创建成功，把新创建的category添加到select选项中
				category.append("<option  value=" + result[0] + ">" + result[1] + "</option>");
				$('#teacher_form_id_categorys').append("<option  value=" + result[0] + ">" + result[1] + "</option>");
				$('#student_form_id_categorys').append("<option  value=" + result[0] + ">" + result[1] + "</option>");
				$('#name').val("");
				alert(info);
			}
			else{
				//创建失败：
				alert(info)
			}

}
$(function() {
	category.html(pre_category);//初始化
	teacher.html(pre_teacher);//初始化
	student.html(pre_student);//初始化
	$.ajax({//通过获取category的list，添加到类目的选项
		type : "GET",
		url : "/api/category",
		cache:false,
		success:function(data){
			$.each(data,function(){
				category.append("<option  value=" + this.id + ">" + this.name + "</option>");
				$('#teacher_form_id_categorys').append("<option  value=" + this.id + ">" + this.name + "</option>");
				$('#student_form_id_categorys').append("<option  value=" + this.id + ">" + this.name + "</option>");
			})
		}
	})

	category.change(function() {//当category的值发生变化时候，查询出对应的学生和老师。
		change_label_color('category');
		if (category.val() != "") {
			teacher.html(pre_teacher);
			student.html(pre_student);
			$.ajax({
				type : "GET",
				url : "/api/people/" + category.val() ,
				cache:false,
				success : after_select_category });
		}})

	 $("#category_form_id").submit(function(e) {//当category form表单提交时，禁用跳转，通过ajax方式进行与后台通讯
    e.preventDefault(); // avoid to execute the actual submit of the form.
    var form = $(this);
    var url = form.attr('action');
    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: create_category_success,
         });
       });
	 for (i in fields){
 		 if (fields[i] != 'category'){
 			eval(fields[i] + ".change(function(){change_label_color('"+ fields[i] + "')})" );
 		 }
 	 }
})
