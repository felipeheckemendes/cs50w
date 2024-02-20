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

    console.log(lecture_list)

    category_section = document.createDocumentFragment()

    for (i=0; i<category_list.length; i++){
        category = buildCategoryHTML(category_list[i])
        course_section = document.createDocumentFragment()
        for (j=0; j<course_list.length; j++){
            course = buildCourseHTML(course_list[j])
            course_section.append(course)
        }
        category = addCollapse(category, course_section)
        category_section.append(category)
    }

    document.querySelector('#coursesexample').append(category_section)

    document.querySelector('#coursesexample').append(buildCourseSectionHTML(lecture_list[0]))

    //THIS COMMENTED CODE CREATES ONE OBJECT OF EACH MODEL
    /*
    let category_id = null
    let term_id = null
    let course_id = null
    let lecture_id = null
    let project_id = null

    await createCategory("======Category 1", "This is category test 1 description")
    .then(result => {console.log(result); category_id=result.id})

    await createTerm("======Term 1", "2024-02-15", "2024-07-15")
    .then(result => {console.log(result); term_id = result.id})

    await createCourse("======Course 1", "www.mit.com", 100, "N", category_id)
    .then(result => {console.log(result); course_id=result.id})

    await createLecture("======Lecture 1", "www.mit.com", "N", course_id)
    .then(result => {console.log(result); lecture_id=result.id})

    await createProject("======Project 1", "www.mit.com", "N", course_id)
    .then(result => {console.log(result); project_id=result.id})

    await createLog('ST', "======Log 1", 120, lecture_id)
    .then(result => console.log(result))
    */


})