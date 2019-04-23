var sections = new Array();
var postform = $("#postform");
var teacher = $("#teacher");
var student = $("#student");
var category = $("#category");
var startday = $("startday");
var endday = $("endday");

function test(){console.log('test')}



function change_status(element){
	var course_infos = $("#course_infos");
	if (element.className != "btn btn-primary"){
		element.className = "btn btn-primary" ;
		sections.push(element.id);
	}
	else{
		element.className = "btn btn-outline-dark";
		id = sections.indexOf(element.id);
		sections.splice(id,1);
		console.log(element.id,id)}
	console.log(sections);
	course_infos.val(sections.join(','));
	if (teacher.val() != "" & student.val() != ""){
		if(sections.length == 0){
			postform.html("");postform.removeAttr("class")}
		else{
				postform.addClass('btn btn-success');
				postform.html('保存变更');
				postform.attr("onclick","test();")}
		 }
		}

$(function() {


	var workout = $("#workout");

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
		success:function(data){$.each(data,function(){category.append("<option  value=" + this.id + ">" + this.name + "</option>");})}
		})


	category.change(function() {
		if (category.val() != "") {
			teacher.html(pre_teacher);
			student.html(pre_student);
			$.ajax({
				type : "GET",
				url : "/api/people/" + category.val() ,
				cache:false,
				success : after_select_category })}})
	 function after_select_category(data){
		 postform.html("");
		 var teachers = data[0];
		 var students = data[1];
		 while(teachers.length != 0){t=teachers.pop();teacher.append("<option  value=" + t.id + ">" + t.name + "</option>")};
		 while(students.length != 0){s=students.pop();student.append("<option  value=" + s.id + ">" + s.name + "</option>")};
		 }
	 student.change(people_change);
	 teacher.change(people_change);

	 function people_change(){
		 var student_id = student.val();
		 var teacher_id = teacher.val();
		 var date = new Date;
		 if (student_id != "" & teacher_id !=""){console.log('2ea');



 			$.ajax({
 				type : "GET",
 				url : "/api/workout/"+date.getFullYear() +"/"+ (date.getMonth()+1) +"/"+ teacher_id+"/"+student_id ,
 				cache:false,
 				success : function(data){workout.html(data.data)} })}
			else if (student_id == "" & teacher_id !=""){console.log('teacher');
				postform.html("");
  			$.ajax({
  				type : "GET",
  				url : "/api/workout/"+date.getFullYear() +"/"+ (date.getMonth()+1) +"/teacher/"+ teacher_id ,
  				cache:false,
  				success : function(data){workout.html(data.data)} })}
			else if (student_id != "" & teacher_id ==""){console.log('student');
				postform.html("");
				$.ajax({
					type : "GET",
					url : "/api/workout/"+date.getFullYear() +"/"+ (date.getMonth()+1) +"/student/"+ student_id ,
					cache:false,
					success : function(data){workout.html(data.data)} })}
			else if (student_id == "" & teacher_id ==""){console.log('0ea');
				postform.html("");
				$.ajax({
					type : "GET",
					url : "/api/workout/"+date.getFullYear() +"/"+ (date.getMonth()+1) ,
					cache:false,
					success : function(data){workout.html(data.data)} })}
			}

	 })
