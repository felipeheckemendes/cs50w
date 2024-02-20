// ===================================
// SECTION 0: Initialization code
// ===================================


document.addEventListener('DOMContentLoaded', async function() {
    
    let course_list = await getObjects("Course");
    let category_list = await getObjects("Category");
    let lecture_list = await getObjects("Lecture")
    let project_list = await getObjects("Project")
    let log_list = await getObjects("Log")
    category_list = category_list.results;
    course_list = course_list.results;
    lecture_list = lecture_list.results;
    project_list = project_list.results;
    log_list = log_list.results;
    
    course_id = document.querySelector('#course').dataset.courseId;
    
    lecture_section = document.createDocumentFragment()
    for (i=0; i<lecture_list.length; i++){
        if (lecture_list[i].course == course_id) {
            lecture = buildCourseSectionHTML(lecture_list[i])
            lecture_section.append(lecture)
        }
    }
    document.querySelector('#lectures').append(lecture_section)

    project_section = document.createDocumentFragment()
    for (i=0; i<project_list.length; i++){
        if (project_list[i].course == course_id) {
            project = buildCourseSectionHTML(project_list[i])
            project_section.append(project)
        }
    }
    document.querySelector('#projects').append(project_section)

})